#!flask/bin/python
import logging.config

from flask import Flask, Blueprint

import settings
from api.natural_search.endpoints.nlp import ns as nlp
from api.restplus import api
from flask import render_template


app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)                                    # Configure the app
    blueprint = Blueprint('api', __name__, url_prefix='/api')   # Set up a blueprint routed to /api
    api.init_app(blueprint)                                     # Initialize the app
    api.add_namespace(nlp)                                      # Add our NLP namespace
    flask_app.register_blueprint(blueprint)                     # Register our blueprint with flask


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()