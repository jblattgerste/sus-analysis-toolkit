// Runs the Dash app's Python code with Pyodide in a web worker, so the page stays responsive during callbacks.

function showStep(step) {
  self.postMessage({ progress: { step } });
}

// Counts the downloaded bytes, so the loading screen can show the progress of the (large) first download
let downloadedBytes = 0;
let lastReport = 0;
const originalFetch = self.fetch.bind(self);

self.fetch = async (...args) => {
  const response = await originalFetch(...args);
  if (!response.body) {
    return response;
  }
  const reader = response.body.getReader();
  const countingStream = new ReadableStream({
    async pull(controller) {
      const { done, value } = await reader.read();
      if (done) {
        controller.close();
        reportDownload(true);
        return;
      }
      downloadedBytes += value.byteLength;
      reportDownload(false);
      controller.enqueue(value);
    },
  });
  return new Response(countingStream, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
};

function reportDownload(force) {
  const now = Date.now();
  if (force || now - lastReport > 100) {
    lastReport = now;
    self.postMessage({ progress: { downloadedBytes } });
  }
}

const ready = (async () => {
  const config = await (await fetch('config.json')).json();
  self.postMessage({ progress: { totalBytes: config.downloadSize } });

  showStep('Downloading the Python runtime…');
  const indexURL = new URL('runtime/', self.location).href;
  importScripts(indexURL + 'pyodide.js');
  const pyodide = await loadPyodide({ indexURL });

  showStep('Downloading Python packages…');
  await pyodide.loadPackage(config.pyodidePackages);
  pyodide.globals.set('wheels', pyodide.toPy(
    config.wheels.map((wheel) => [wheel.name, new URL('wheels/' + wheel.file, self.location).href])));
  await pyodide.runPythonAsync(`
import micropip
installed = {name.lower().replace('_', '-') for name in micropip.list()}
await micropip.install([url for name, url in wheels if name not in installed], deps=False)
`);

  showStep('Starting the local server…');
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
  showStep('Opening the toolkit…');
  return namespace.get('handle_request');
})();

ready.catch((error) => self.postMessage({ progress: { error: 'The toolkit could not be started: ' + error } }));

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
