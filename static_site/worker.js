// Runs the Dash app's Python code with Pyodide in a web worker, so the page stays responsive during callbacks.

function showProgress(text) {
  self.postMessage({ progress: text });
}

const ready = (async () => {
  const config = await (await fetch('config.json')).json();

  showProgress('Loading the Python runtime…');
  importScripts(config.pyodideIndexURL + 'pyodide.js');
  const pyodide = await loadPyodide({ indexURL: config.pyodideIndexURL });

  showProgress('Loading Python packages…');
  await pyodide.loadPackage(config.pyodidePackages);
  pyodide.globals.set('wheels', pyodide.toPy(
    config.wheels.map((wheel) => [wheel.name, new URL('wheels/' + wheel.file, self.location).href])));
  await pyodide.runPythonAsync(`
import micropip
installed = {name.lower().replace('_', '-') for name in micropip.list()}
await micropip.install([url for name, url in wheels if name not in installed], deps=False)
`);

  showProgress('Starting the SUS Analysis Toolkit…');
  const appZip = await (await fetch('app.zip')).arrayBuffer();
  pyodide.unpackArchive(appZip, 'zip', { extractDir: '/app' });
  pyodide.globals.set('base_path', config.basePath);
  pyodide.runPython(`
import os, sys
os.environ['DASH_REQUESTS_PATHNAME_PREFIX'] = base_path
os.chdir('/app')
sys.path.insert(0, '/app')
`);
  const namespace = pyodide.toPy({});
  pyodide.runPython(await (await fetch('bootstrap.py')).text(), { globals: namespace });
  showProgress('Loading…');
  return namespace.get('handle_request');
})();

ready.catch((error) => showProgress('The toolkit could not be started: ' + error));

self.onmessage = async ({ data }) => {
  const { id, method, path, headers, body } = data;
  try {
    const handleRequest = await ready;
    const result = handleRequest(method, path, JSON.stringify(headers), body);
    const [responseStatus, responseHeaders, responseBody] = result.toJs();
    result.destroy();
    self.postMessage({ id, status: responseStatus, headers: JSON.parse(responseHeaders), body: responseBody });
  } catch (error) {
    self.postMessage({ id, error: String(error) });
  }
};
