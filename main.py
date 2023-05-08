import sentry_sdk

from flask import Flask, jsonify, request
from werkzeug.routing import Rule
from localsettings import SENTRY_URL 
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[FlaskIntegration(),],
        traces_sample_rate=1.0
        )

app = Flask(__name__)

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

@app.endpoint("catch_all")
def _404(_404):
    # TODO: Send 404 HTTP status
    return {"404": "Not Found"}

@app.route('/hello', methods=['GET'])
def helloworld():
    data = {"data": "Only GET is supported for now!"}
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
    return jsonify(data)

app.url_map.add(Rule("/", defaults={"_404": ""}, endpoint="catch_all"))
app.url_map.add(Rule("/<path:_404>", endpoint="catch_all"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


