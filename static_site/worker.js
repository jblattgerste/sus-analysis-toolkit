// Runs the Dash app's Python code with Pyodide in a web worker, so the page stays responsive during callbacks.

function showStep(step) {
  self.postMessage({ progress: { step } });
}

// Progress for the loading screen: loaded bytes (from the network or the browser cache) for the progress bar, and
// the bytes that were actually transferred over the network, as reported by the browser for each finished file
let loadedBytes = 0;
let downloadedBytes = 0;
let lastReport = 0;
const originalFetch = self.fetch.bind(self);

new PerformanceObserver((entries) => {
  for (const entry of entries.getEntries()) {
    downloadedBytes += entry.transferSize || 0;  // not reported by every browser
  }
  reportProgress(true);
}).observe({ type: 'resource', buffered: true });

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
        return;
      }
      loadedBytes += value.byteLength;
      reportProgress(false);
      controller.enqueue(value);
    },
  });
  return new Response(countingStream, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
};

function reportProgress(force) {
  const now = Date.now();
  if (force || now - lastReport > 100) {
    lastReport = now;
    self.postMessage({ progress: { loadedBytes, downloadedBytes } });
  }
}

const ready = (async () => {
  const config = await (await fetch('config.json')).json();
  self.postMessage({ progress: { totalBytes: config.downloadSize } });

  showStep('Loading the Python runtime…');
  const indexURL = new URL('runtime/', self.location).href;
  importScripts(indexURL + 'pyodide.js');
  const pyodide = await loadPyodide({ indexURL });

  showStep('Loading Python packages…');
  await pyodide.loadPackage(config.pyodidePackages);
  const wheelURLs = config.wheels.map((file) => new URL('wheels/' + file, self.location).href);
  pyodide.globals.set('wheels', pyodide.toPy(wheelURLs));
  await pyodide.runPythonAsync('import micropip\nawait micropip.install(wheels, deps=False)');

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
