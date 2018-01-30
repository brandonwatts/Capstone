#!flask/bin/python
import logging.config

from flask import Flask, Blueprint

from api.Endpoints.nlp import ns as nlp
from api.restplus import api

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = 'localhost:8888'
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    flask_app.config['RESTPLUS_VALIDATE'] = True
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = False
    flask_app.config['ERROR_404_HELP'] = False


def initialize_app(flask_app):
    configure_app(flask_app)                                    # Configure the app
    blueprint = Blueprint('api', __name__, url_prefix='/api')   # Set up a blueprint routed to /api
    api.init_app(blueprint)                                     # Initialize the app
    api.add_namespace(nlp)                                      # Add our NLP namespace
    flask_app.register_blueprint(blueprint)                     # Register our blueprint with flask


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=True)


if __name__ == "__main__":
    main()
