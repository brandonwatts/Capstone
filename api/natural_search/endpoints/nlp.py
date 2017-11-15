import logging
from flask_restplus import Resource
from api.restplus import api
from flask_restplus import reqparse
import api.natural_search.nlp_operations as nlp

'''nlp.py will define all the endpoints located at /api/nlp'''

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

ns = api.namespace('nlp', description='Operations related to Natural Language Processing')
log = logging.getLogger(__name__)
query_arguments = reqparse.RequestParser()

query_arguments.add_argument('request', type=str, required=True)


@ns.route('/')
class NlpEndpoints(Resource):

    @api.expect(query_arguments, validate=True)
    def get(self):
        args = query_arguments.parse_args()
        request = args['request']
        return nlp.response(request)
