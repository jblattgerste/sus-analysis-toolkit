// Lets the Dash frontend talk to the Dash app running with Pyodide in a web worker (worker.js) instead of a server.
// Has to be loaded before the Dash renderer, so it can take over the renderer's requests to the Dash API.
(function () {
  const script = document.currentScript;
  const basePath = script.dataset.basePath;
  const worker = new Worker(new URL('worker.js', script.src));
  const pending = new Map();
  let nextRequestId = 0;

  // Loading screen (loading.html), shown until the Dash renderer has rendered the toolkit
  const progress = { step: 'Loading…', downloadedBytes: 0, totalBytes: 0, error: null };

  function showProgress() {
    const loading = document.getElementById('static-site-loading');
    if (!loading) {
      return;
    }
    const megabytes = (bytes) => (bytes / 1e6).toFixed(1);
    const downloaded = Math.min(progress.downloadedBytes, progress.totalBytes);
    loading.querySelector('.static-site-loading-step').textContent = progress.error || progress.step;
    loading.querySelector('.static-site-loading-size').textContent = progress.totalBytes
      ? `${megabytes(downloaded)} of ${megabytes(progress.totalBytes)} MB` : '';
    loading.querySelector('.static-site-loading-bar-fill').style.width = progress.totalBytes
      ? `${(100 * downloaded / progress.totalBytes).toFixed(1)}%` : '0';
    loading.classList.toggle('static-site-loading-failed', Boolean(progress.error));
  }

  document.addEventListener('DOMContentLoaded', () => {
    showProgress();
    const loading = document.getElementById('static-site-loading');
    const entryPoint = document.getElementById('react-entry-point');
    const observer = new MutationObserver(() => {
      // On errors the loading screen stays, showing the error
      if (!progress.error && entryPoint.firstElementChild && !entryPoint.querySelector('._dash-loading')) {
        observer.disconnect();
        loading.classList.add('static-site-loading-done');
        setTimeout(() => loading.remove(), 500);
      }
    });
    observer.observe(entryPoint, { childList: true, subtree: true });
  });

  worker.onmessage = ({ data }) => {
    if ('progress' in data) {
      Object.assign(progress, data.progress);
      showProgress();
      return;
    }
    const { resolve, reject } = pending.get(data.id);
    pending.delete(data.id);
    if (data.error) {
      reject(new Error(data.error));
    } else {
      resolve(data);
    }
  };

  function callPython(method, path, headers, body) {
    const id = nextRequestId++;
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      worker.postMessage({ id, method, path, headers, body });
    });
  }

  const originalFetch = window.fetch.bind(window);

  window.fetch = async function (input, init) {
    const request = new Request(input, init);
    const url = new URL(request.url);
    if (url.origin !== location.origin || !url.pathname.startsWith(basePath + '_dash-')) {
      return originalFetch(input, init);
    }
    const body = ['GET', 'HEAD'].includes(request.method) ? null : await request.text();
    const path = '/' + url.pathname.slice(basePath.length) + url.search;
    const response = await callPython(request.method, path, Object.fromEntries(request.headers), body);
    let responseBody = response.body;
    if (path.startsWith('/_dash-update-component') && response.status === 200) {
      responseBody = await renderImages(responseBody);
    }
    return new Response([204, 304].includes(response.status) ? null : responseBody, {
      status: response.status,
      headers: { 'Content-Type': response.headers['Content-Type'] || 'application/json' },
    });
  };

  // Image downloads: bootstrap.py replaces plotly's server-side image export (kaleido) with a description of the
  // requested image. These are rendered here with plotly.js, before the Dash renderer triggers the download.
  const IMAGE_MARKER = new TextEncoder().encode('PYODIDE-PLOTLY-IMAGE\n');
  const IMAGE_MARKER_BASE64 = btoa('PYODIDE-PLOTLY-IMAGE\n');

  async function renderImages(responseBody) {
    if (!responseBody.includes(IMAGE_MARKER_BASE64) && !responseBody.includes('.zip"')) {
      return responseBody;
    }
    const payload = JSON.parse(responseBody);
    const downloads = [];
    (function findDownloads(value) {
      if (value && typeof value === 'object') {
        if (typeof value.content === 'string' && value.base64 === true) {
          downloads.push(value);
        } else {
          Object.values(value).forEach(findDownloads);
        }
      }
    })(payload);
    for (const download of downloads) {
      if (download.content.startsWith(IMAGE_MARKER_BASE64)) {
        download.content = bytesToBase64(await renderImage(base64ToBytes(download.content)));
      } else if (String(download.filename).endsWith('.zip')) {
        download.content = await renderImagesInZip(download.content);
      }
    }
    return JSON.stringify(payload);
  }

  async function renderImagesInZip(zipBase64) {
    await loadScript(new URL('jszip.min.js', script.src).href, () => window.JSZip);
    const zip = await JSZip.loadAsync(zipBase64, { base64: true });
    let changed = false;
    for (const file of Object.values(zip.files)) {
      const bytes = await file.async('uint8array');
      if (startsWithMarker(bytes)) {
        zip.file(file.name, await renderImage(bytes));
        changed = true;
      }
    }
    return changed ? zip.generateAsync({ type: 'base64', compression: 'DEFLATE' }) : zipBase64;
  }

  async function renderImage(bytes) {
    const text = new TextDecoder().decode(bytes.subarray(IMAGE_MARKER.length));
    const newline = text.indexOf('\n');
    const spec = JSON.parse(text.slice(0, newline));
    const figure = JSON.parse(text.slice(newline + 1));
    const layout = figure.layout || {};
    await loadScript(basePath + '_dash-component-suites/plotly/package_data/plotly.min.js', () => window.Plotly);
    // Same defaults as plotly.py's image export
    const dataUrl = await Plotly.toImage({ data: figure.data || [], layout }, {
      format: spec.format,
      width: spec.width || layout.width || 700,
      height: spec.height || layout.height || 500,
      scale: spec.scale || 1,
    });
    const separator = dataUrl.indexOf(',');
    const data = dataUrl.slice(separator + 1);
    return dataUrl.slice(0, separator).endsWith(';base64')
      ? base64ToBytes(data)
      : new TextEncoder().encode(decodeURIComponent(data));
  }

  function startsWithMarker(bytes) {
    return bytes.length >= IMAGE_MARKER.length && IMAGE_MARKER.every((byte, i) => bytes[i] === byte);
  }

  function loadScript(src, isLoaded) {
    if (isLoaded()) {
      return Promise.resolve();
    }
    return new Promise((resolve, reject) => {
      const element = document.createElement('script');
      element.src = src;
      element.onload = resolve;
      element.onerror = () => reject(new Error('Could not load ' + src));
      document.head.appendChild(element);
    });
  }

  function base64ToBytes(base64) {
    return Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));
  }

  function bytesToBase64(bytes) {
    let binary = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    return btoa(binary);
  }
})();
