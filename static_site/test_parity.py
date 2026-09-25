"""Checks that the static (Pyodide) site behaves like the Dash server.

Runs the same user interactions in a headless browser against both versions and compares what they show: the
rendered text, the data and layout of every plotly chart and the downloaded files.

Usage:
  python static_site/test_parity.py --server-url http://127.0.0.1:8050/ \
      --static-url http://127.0.0.1:8000/sus-analysis-toolkit/ --out parity-results
"""
import argparse
import io
import json
import math
import os
import struct
import sys
import time
import zipfile

from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STARTUP_TIMEOUT_MS = 240_000
CALLBACK_TIMEOUT_MS = 60_000

SNAPSHOT_JS = """() => {
    const graphs = {};
    document.querySelectorAll('.js-plotly-plot').forEach((el) => {
        const id = el.parentElement.closest('[id]').id;
        graphs[id] = JSON.parse(JSON.stringify({data: el.data, layout: el.layout}));
    });
    return {text: document.getElementById('react-entry-point').innerText, graphs};
}"""


def wait_until_idle(page):
    """Waits until Dash has no running callbacks (Dash shows 'Updating...' as title while they run)."""
    deadline = time.time() + CALLBACK_TIMEOUT_MS / 1000
    idle_since = None
    while time.time() < deadline:
        if page.title() == 'Updating...':
            idle_since = None
        elif idle_since is None:
            idle_since = time.time()
        elif time.time() - idle_since > 1.5:
            return
        time.sleep(0.1)
    raise TimeoutError('Dash callbacks did not finish')


def select_dropdown(page, dropdown_id, label):
    page.click(f'#{dropdown_id} .Select-control')
    page.click(f'#{dropdown_id} .VirtualizedSelectOption:text-is("{label}")')
    wait_until_idle(page)


def click_tab(page, tab_id):
    page.click(f'#{tab_id}')
    wait_until_idle(page)


def png_size(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'not a PNG file'
    return struct.unpack('>II', data[16:24])


def describe_download(download):
    """Turns a download into comparable data: text files as text, images as their size."""
    with open(download.path(), 'rb') as f:
        data = f.read()
    return describe_file(download.suggested_filename, data)


def describe_file(filename, data):
    if filename.endswith('.png'):
        return {'file': filename, 'png_size': png_size(data)}
    if filename.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            return {'file': filename, 'entries': {name: describe_file(name, zf.read(name)) for name in sorted(zf.namelist())}}
    return {'file': filename, 'text': data.decode('utf-8-sig')}


def download(page, button_id):
    with page.expect_download(timeout=CALLBACK_TIMEOUT_MS) as download_info:
        page.click(f'#{button_id}')
    result = describe_download(download_info.value)
    wait_until_idle(page)
    return result


def open_app(page, url):
    page.goto(url)
    page.wait_for_selector('#start-tool-button', timeout=STARTUP_TIMEOUT_MS)
    wait_until_idle(page)


def run_scenarios(page, url, screenshot_dir):
    """Runs all interactions and returns the observed state after each step."""
    results = {}

    def snapshot(name):
        results[name] = page.evaluate(SNAPSHOT_JS)
        page.screenshot(path=os.path.join(screenshot_dir, f'{name}.png'), full_page=True)

    # Multi-variable analysis with the example data
    open_app(page, url)
    snapshot('landing-page')
    page.click('#start-tool-button')
    page.wait_for_selector('#editable-table', timeout=CALLBACK_TIMEOUT_MS)
    wait_until_idle(page)
    snapshot('multi-raw-data')
    for tab in ['main-plot-tab', 'percentile-plot-tab', 'per-item-tab', 'conclusiveness-tab']:
        click_tab(page, tab)
        page.wait_for_selector('.js-plotly-plot', timeout=CALLBACK_TIMEOUT_MS)
        wait_until_idle(page)
        snapshot(f"multi-{tab}")

    click_tab(page, 'main-plot-tab')
    for dropdown_id, label in [('scale-mainplot', 'Grade Scale'), ('scale-mainplot', 'Industry Benchmark Scale'),
                               ('plotstyle-mainplot', 'Notched Boxplot'), ('plotstyle-mainplot', 'Bar chart'),
                               ('sort-by-mainplot', 'Mean'), ('orientation-mainplot', 'Horizontal')]:
        select_dropdown(page, dropdown_id, label)
        snapshot(f'mainplot-{dropdown_id}-{label}')
    results['download-mainplot-image'] = download(page, 'image-mainplot-button')
    results['download-mainplot-csv'] = download(page, 'csv-mainplot-button')
    results['download-all'] = download(page, 'download-all-mainplot-button')

    click_tab(page, 'percentile-plot-tab')
    results['download-percentile-image'] = download(page, 'image-percentile-button')
    results['download-percentile-csv'] = download(page, 'csv-percentile-button')

    click_tab(page, 'per-item-tab')
    select_dropdown(page, 'plotstyle-per-question-chart', 'Boxplot')
    snapshot('per-item-boxplot')
    results['download-per-item-image'] = download(page, 'image-perquestion-button')
    results['download-per-item-csv'] = download(page, 'csv-per-question-button')

    click_tab(page, 'conclusiveness-tab')
    results['download-conclusiveness-image'] = download(page, 'image-conclusiveness-button')
    results['download-conclusiveness-csv'] = download(page, 'csv-conclusiveness-button')

    click_tab(page, 'editable-table-tab')
    results['download-data-csv'] = download(page, 'csv-data-button')
    page.click('#add-row-button')
    wait_until_idle(page)
    snapshot('multi-added-empty-row')

    # Multi-variable analysis with an uploaded file
    open_app(page, url)
    page.set_input_files('#upload-data-multi input[type=file]', os.path.join(REPO_ROOT, 'assets', 'studyData.csv'))
    page.wait_for_selector('#editable-table', timeout=CALLBACK_TIMEOUT_MS)
    wait_until_idle(page)
    click_tab(page, 'main-plot-tab')
    snapshot('upload-multi-sus-score')

    # Upload of an invalid file
    open_app(page, url)
    page.set_input_files('#upload-data-multi input[type=file]', os.path.join(REPO_ROOT, 'assets', 'BibTex.txt'))
    page.wait_for_selector('text=There was an error processing this file', timeout=CALLBACK_TIMEOUT_MS)
    wait_until_idle(page)
    snapshot('upload-invalid-file')

    # Single-variable analysis with the example data
    open_app(page, url)
    page.click('#start-tool-button-single')
    page.wait_for_selector('#editable-table-single', timeout=CALLBACK_TIMEOUT_MS)
    wait_until_idle(page)
    snapshot('single-raw-data')
    click_tab(page, 'single-study-tab')
    page.wait_for_selector('.js-plotly-plot', timeout=CALLBACK_TIMEOUT_MS)
    wait_until_idle(page)
    snapshot('single-dashboard')
    for preset in ['Preset 2', 'Preset 3', 'Preset 4']:
        select_dropdown(page, 'preset-single-study', preset)
        snapshot(f'single-{preset}')
    results['download-single-image'] = download(page, 'download-single-study-chart-button')
    click_tab(page, 'single-study-editable-table')
    results['download-single-data-csv'] = download(page, 'csv-data-button-single')

    return results


def compare(expected, actual, path='', differences=None):
    """Deep comparison that tolerates tiny floating point differences (e.g. from other numpy builds)."""
    if differences is None:
        differences = []
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in sorted(set(expected) | set(actual)):
            if key not in expected or key not in actual:
                differences.append(f'{path}/{key}: only in {"server" if key in expected else "static site"}')
            else:
                compare(expected[key], actual[key], f'{path}/{key}', differences)
    elif isinstance(expected, list) and isinstance(actual, list) and len(expected) == len(actual):
        for i, (e, a) in enumerate(zip(expected, actual)):
            compare(e, a, f'{path}[{i}]', differences)
    elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)) and not isinstance(expected, bool):
        if not math.isclose(expected, actual, rel_tol=1e-9, abs_tol=1e-9):
            differences.append(f'{path}: server {expected!r} != static site {actual!r}')
    elif expected != actual:
        differences.append(f'{path}: server {str(expected)[:300]!r} != static site {str(actual)[:300]!r}')
    return differences


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--server-url', required=True)
    parser.add_argument('--static-url', required=True)
    parser.add_argument('--out', default='parity-results')
    args = parser.parse_args()

    results = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or None)
        for name, url in [('server', args.server_url), ('static', args.static_url)]:
            screenshot_dir = os.path.join(args.out, name)
            os.makedirs(screenshot_dir, exist_ok=True)
            page = browser.new_page(viewport={'width': 1600, 'height': 1000}, accept_downloads=True)
            page.on('console', lambda message, name=name: print(f'[{name} console] {message.text}'[:500]))
            page.on('pageerror', lambda error, name=name: print(f'[{name} page error] {error}'))
            started = time.time()
            results[name] = run_scenarios(page, url, screenshot_dir)
            print(f'{name}: ran {len(results[name])} steps in {time.time() - started:.0f}s')
            page.close()
            with open(os.path.join(args.out, f'{name}.json'), 'w') as f:
                json.dump(results[name], f, indent=1)
        browser.close()

    differences = compare(results['server'], results['static'])
    if differences:
        print(f'{len(differences)} differences between the server and the static site:')
        for difference in differences[:200]:
            print('  ' + difference)
        sys.exit(1)
    print('The static site behaves like the server in all checked steps.')


if __name__ == '__main__':
    main()
