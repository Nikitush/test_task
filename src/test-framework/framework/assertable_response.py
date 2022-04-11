import sys
import logging
from json.decoder import JSONDecodeError


logger = logging.getLogger('test_logger')
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)


class AssertableResponse:

    def __init__(self, response):
        try:
            logger.info('Request: method={} url={} body={}\n'.format(response.request.method, response.request.url,
                                                                     response.request.body))
            self.status_code = response.status_code
            self.body = response.json()
            logger.info('Response: status_code={} body={}\n'.format(self.status_code, self.body))
        except JSONDecodeError:
            logger.error('Response contain non JSON data')

    def status_code_should_be(self, code):
        logger.info('Check that status code should be {}\n'.format(code))
        return self.status_code == code

    def body_should_be(self, body):
        logger.info('Check that body should be {}\n'.format(body))
        return self.body == body
