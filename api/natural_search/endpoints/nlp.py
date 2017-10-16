import logging
from flask_restplus import Resource
from api.restplus import api
from flask_restplus import reqparse

ns = api.namespace('nlp', description='Operations related to Natural Language Processing')
log = logging.getLogger(__name__)           # Logger
query_arguments = reqparse.RequestParser()  # Arguements

query_arguments.add_argument('request', type=str, required=True)    # We are expecting an arguement called request that
                                                                    # is a string. (WILL EVENTLY TAKE A JSON OBJECT)


@ns.route('/')
class NlpEndpoints(Resource):

    @api.expect(query_arguments, validate=True)
    def get(self):
        args = query_arguments.parse_args()
        return args['request']
