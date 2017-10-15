import logging
from flask_restplus import Resource
from api.restplus import api

log = logging.getLogger(__name__)
ns = api.namespace('nlp', description='Operations related to Natural Language Processing')


@ns.route('/')
class NlpEndpoints(Resource):

    def get(self):
        return "RESPONSE"
