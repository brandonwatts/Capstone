import logging
from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='CoStar NLP API',
          description='CoStar API powering NLP-Based Applications')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
