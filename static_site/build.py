"""Exports the Dash app as a fully static site that runs its Python callbacks in the browser via Pyodide.

The exported site contains:
  - index.html: the page Dash would serve, plus a small script that routes Dash's API requests into Pyodide
  - _dash-component-suites/...: the JavaScript bundles of Dash and its components
  - assets/...: the app's assets folder
  - pyodide/...: the app's Python sources, the pure-Python wheels it depends on, the worker running Pyodide and
    the Pyodide runtime itself, so the site does not depend on any CDN

Usage:
  python static_site/build.py --out _site --base-path /sus-analysis-toolkit/
"""
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from urllib.parse import urlparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATIC_SITE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pyodide release whose bundled numpy/pandas match requirements.txt (Python 3.12, pandas 2.2.x)
PYODIDE_VERSION = '0.27.7'
# Only used while building: the runtime and the packages are copied into the site
PYODIDE_DOWNLOAD_URL = f'https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/'
PYODIDE_CORE_FILES = ['pyodide.js', 'pyodide.asm.js', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json']
# Used in the browser to create the zip file of "Download complete analysis"
JSZIP_URL = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js'
# Only needed for server-side image export, which the static site does in the browser instead
EXCLUDED_REQUIREMENTS = ['kaleido']

APP_SOURCES = ['Annotations.py', 'ChartLayouts.py', 'Charts.py', 'Helper.py', 'Layouts.py', 'Result.py',
               'SUSDataset.py', 'SUSStud.py', 'SingleStudyCharts.py', 'dashApp.py', 'styles.py']
# Assets read by the Python code at runtime (e.g. the example data)
APP_ASSETS = ['assets/studyData.csv', 'assets/singleStudyData.csv', 'assets/body.css', 'assets/favicon.ico']


def write_file(out_dir, relative_path, data):
    path = os.path.join(out_dir, relative_path.lstrip('/'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def export_dash_frontend(out_dir, base_path):
    """Renders the index page and every component bundle Dash would serve."""
    os.environ['DASH_REQUESTS_PATHNAME_PREFIX'] = base_path
    sys.path.insert(0, REPO_ROOT)
    os.chdir(REPO_ROOT)
    import dashApp
    from dash.fingerprint import build_fingerprint

    app = dashApp.app
    client = app.server.test_client()

    index_html = client.get('/').get_data(as_text=True)

    # Files referenced by the index page (fingerprinted bundles, css, favicon)
    referenced = set()
    for url in re.findall(r'(?:src|href)="([^"]+)"', index_html):
        path = urlparse(html.unescape(url)).path
        if path.startswith(base_path):
            referenced.add(path[len(base_path):])

    # All files Dash registered for its component suites, including the lazily loaded chunks and plotly.js
    fingerprinted_chunks = set()
    for namespace, paths in app.registered_paths.items():
        package_dir = os.path.dirname(sys.modules[namespace].__file__)
        js_paths = [path for path in paths if path.endswith('.js')]
        for path in js_paths:
            referenced.add(f'_dash-component-suites/{namespace}/{path}')
            # Some bundles request their lazy chunks with a fingerprint that is baked into the bundle
            with open(os.path.join(package_dir, path), encoding='utf-8', errors='ignore') as f:
                baked_fingerprints = set(re.findall(r'splice\(1,0,"(v[0-9_]+m[0-9]+)"\)', f.read()))
            for fingerprint in baked_fingerprints:
                for chunk in js_paths:
                    if os.path.dirname(chunk) == os.path.dirname(path):
                        name, extension = chunk.split('.', 1)
                        fingerprinted_chunks.add(f'_dash-component-suites/{namespace}/{name}.{fingerprint}.{extension}')

    for relative_path in sorted(referenced | fingerprinted_chunks):
        if relative_path.startswith('assets/'):
            continue  # the whole assets folder is copied below
        response = client.get('/' + relative_path)
        if response.status_code != 200:
            raise RuntimeError(f'Could not export {relative_path}: HTTP {response.status_code}')
        write_file(out_dir, relative_path, response.get_data())

    shutil.copytree(os.path.join(REPO_ROOT, 'assets'), os.path.join(out_dir, 'assets'), dirs_exist_ok=True)

    return index_html


def download_wheels(wheel_dir):
    """Resolves the requirements like the server installation does.

    Pure-Python wheels are copied into the site. Packages with compiled code (numpy, pandas, ...) are returned
    separately, since they are loaded from the Pyodide distribution, which has them built for WebAssembly.
    """
    with open(os.path.join(REPO_ROOT, 'requirements.txt')) as f:
        requirements = [line.strip() for line in f
                        if line.strip() and not any(line.strip().startswith(x) for x in EXCLUDED_REQUIREMENTS)]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, '-m', 'pip', 'download', '--quiet', '--dest', tmp,
                        '--only-binary=:all:', '--python-version', '3.12',
                        '--platform', 'manylinux2014_x86_64', *requirements], check=True)
        wheels, compiled_packages = [], []
        for filename in sorted(os.listdir(tmp)):
            name = filename.split('-')[0].lower().replace('_', '-')
            if filename.endswith('-none-any.whl'):
                shutil.copy(os.path.join(tmp, filename), wheel_dir)
                wheels.append({'name': name, 'file': filename})
            else:
                compiled_packages.append(name)
    return wheels, compiled_packages


def download(url, path, sha256=None):
    with urllib.request.urlopen(url) as response:
        data = response.read()
    if sha256 is not None and hashlib.sha256(data).hexdigest() != sha256:
        raise RuntimeError(f'Checksum mismatch for {url}')
    with open(path, 'wb') as f:
        f.write(data)


def download_pyodide(runtime_dir, packages):
    """Copies the Pyodide runtime and the given packages (with their dependencies) into the site."""
    os.makedirs(runtime_dir)
    for filename in PYODIDE_CORE_FILES:
        download(PYODIDE_DOWNLOAD_URL + filename, os.path.join(runtime_dir, filename))
    with open(os.path.join(runtime_dir, 'pyodide-lock.json')) as f:
        lock = json.load(f)['packages']
    needed, todo = set(), list(packages)
    while todo:
        name = todo.pop()
        if name not in needed:
            needed.add(name)
            todo.extend(lock[name]['depends'])
    for name in sorted(needed):
        package = lock[name]
        download(PYODIDE_DOWNLOAD_URL + package['file_name'], os.path.join(runtime_dir, package['file_name']),
                 package['sha256'])
    return sorted(needed)


def build(out_dir, base_path):
    if not base_path.startswith('/') or not base_path.endswith('/'):
        raise ValueError('--base-path must start and end with "/"')
    out_dir = os.path.abspath(out_dir)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    index_html = export_dash_frontend(out_dir, base_path)

    pyodide_dir = os.path.join(out_dir, 'pyodide')
    wheel_dir = os.path.join(pyodide_dir, 'wheels')
    os.makedirs(wheel_dir)
    wheels, compiled_packages = download_wheels(wheel_dir)

    pyodide_packages = ['micropip'] + compiled_packages
    runtime_dir = os.path.join(pyodide_dir, 'runtime')
    runtime_packages = download_pyodide(runtime_dir, pyodide_packages)
    download(JSZIP_URL, os.path.join(pyodide_dir, 'jszip.min.js'))
    # Wheels of packages that are already part of the Pyodide distribution are not needed
    for wheel in [wheel for wheel in wheels if wheel['name'] in runtime_packages]:
        os.remove(os.path.join(wheel_dir, wheel['file']))
        wheels.remove(wheel)

    with zipfile.ZipFile(os.path.join(pyodide_dir, 'app.zip'), 'w', zipfile.ZIP_DEFLATED) as zf:
        for relative_path in APP_SOURCES + APP_ASSETS:
            zf.write(os.path.join(REPO_ROOT, relative_path), relative_path)

    for filename in ['worker.js', 'glue.js', 'bootstrap.py', 'loading.css']:
        shutil.copy(os.path.join(STATIC_SITE_DIR, filename), pyodide_dir)

    # Everything the worker fetches when starting (pyodide.js and pyodide.asm.js are loaded as scripts instead)
    fetched_files = ([os.path.join(runtime_dir, f) for f in os.listdir(runtime_dir)
                      if f not in ['pyodide.js', 'pyodide.asm.js']] +
                     [os.path.join(wheel_dir, wheel['file']) for wheel in wheels] +
                     [os.path.join(pyodide_dir, f) for f in ['app.zip', 'bootstrap.py']])
    download_size = sum(os.path.getsize(path) for path in fetched_files)

    config = {
        'basePath': base_path,
        'downloadSize': download_size,
        'pyodidePackages': pyodide_packages,
        'wheels': wheels,
    }
    with open(os.path.join(pyodide_dir, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    # The glue script has to run before the Dash renderer makes its first request
    head_tags = (f'<script src="{base_path}pyodide/glue.js" data-base-path="{base_path}"></script>\n'
                 f'        <link rel="stylesheet" href="{base_path}pyodide/loading.css">')
    index_html = index_html.replace('<head>', '<head>\n        ' + head_tags, 1)
    with open(os.path.join(STATIC_SITE_DIR, 'loading.html'), encoding='utf-8') as f:
        loading_html = f.read().replace('{download_size_mb}', str(round(download_size / 1e6)))
    index_html = index_html.replace('<body>', '<body>\n' + loading_html, 1)
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    # GitHub Pages must not run the site through Jekyll (it would drop files starting with "_")
    open(os.path.join(out_dir, '.nojekyll'), 'w').close()

    print(f'Static site written to {out_dir} (Pyodide {PYODIDE_VERSION} with {len(runtime_packages)} packages, '
          f'{len(wheels)} wheels, base path {base_path})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', default='_site')
    parser.add_argument('--base-path', default='/sus-analysis-toolkit/')
    args = parser.parse_args()
    build(args.out, args.base_path)
