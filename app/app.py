import logging
import random
import logstash
from flask import Flask, request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


app = Flask(__name__)
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
# app.logger.addHandler(logstash.LogstashHandler('logstash', 5044, version=1))
logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)


sentry_sdk.init(
    dsn="https://2ba4ee28b0dc46cfb1615f16f6487124@o476876.ingest.sentry.io/4503896328241152",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')


@app.route('/')
def index():
    result = random.randint(1, 50)
    app.logger.info(f'User get number {result}')
    return f"Ваше число {result}!"
