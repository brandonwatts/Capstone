from flask import Flask
from flask_restplus import Resource, Api, reqparse

from smartsearch import nlp
from smartsearch.models.apartments import apartments
from smartsearch.models.general import general

app = Flask(__name__)
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app, version='1.0', title='CoStar NLP API', description='CoStar API powering NLP-Based Applications')

parser = reqparse.RequestParser()
parser.add_argument('request', type=str, required=True)
parser.add_argument('request_type', type=str, choices=('Apartments', 'General'), required=True)


@api.route('/nlp')
class NlpEndpoints(Resource):
    @api.expect(parser, validate=True)
    def get(self):
        args = parser.parse_args()
        request = args['request']
        request_type = args['request_type']
        
        results = nlp.parse(request)
        
        if request_type == "General":
            return general.call(results)
        elif request_type == "Apartments":
            return apartments.call(results)

if __name__ == '__main__':
    app.run()
