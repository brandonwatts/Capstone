from flask import Flask
from flask_restplus import Resource, Api, reqparse
from Api.NLP import NLP
from Api.Models.Apartments.ApartmentsAPI import ApartmentsAPI
from Api.Models.General.GeneralAPI import GeneralAPI

app = Flask(__name__)
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app, version='1.0', title='CoStar NLP API', description='CoStar API powering NLP-Based Applications')
parser = reqparse.RequestParser()
parser.add_argument('request', type=str, required=True)
parser.add_argument('request_type', type=str, choices=('Apartments', 'General'), required=True)
nlp = NLP()

@api.route('/nlp')
class NlpEndpoints(Resource):
    @api.expect(parser, validate=True)
    def get(self):
        args = parser.parse_args()
        request = args['request']
        request_type = args['request_type']
        nlp_results = nlp.parse(request)

        if request_type == "General":
            API = GeneralAPI(nlp_results)

        elif request_type == "Apartments":
            API = ApartmentsAPI(nlp_results)

        return API.call()

if __name__ == '__main__':
    app.run()
