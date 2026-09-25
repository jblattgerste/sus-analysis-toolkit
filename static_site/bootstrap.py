"""Runs inside the Pyodide web worker: starts the Dash app and answers the requests of the Dash frontend."""
import json

import plotly.basedatatypes

# Image export normally uses kaleido (a headless browser), which cannot run in Pyodide. Instead, the returned
# bytes describe the requested image, and glue.js renders it with plotly.js before handing it to the user.
IMAGE_MARKER = b'PYODIDE-PLOTLY-IMAGE\n'


def to_image(self, format=None, width=None, height=None, scale=None, **kwargs):
    spec = {'format': format or 'png', 'width': width, 'height': height, 'scale': scale}
    return IMAGE_MARKER + json.dumps(spec).encode() + b'\n' + self.to_json().encode()


plotly.basedatatypes.BaseFigure.to_image = to_image

import dashApp  # noqa: E402

client = dashApp.app.server.test_client()


def handle_request(method, path, headers, body):
    response = client.open(path, method=method, headers=json.loads(headers), data=body)
    return response.status_code, json.dumps(dict(response.headers)), response.get_data(as_text=True)
