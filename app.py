from flask import Flask
from flask_restplus import Resource, Api, reqparse
from Api.NLP import NLP
from Api.Models.Apartments.ApartmentsAPICreator import ApartmentsAPICreator
import requests
import json

app = Flask(__name__)
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app, version='1.0', title='CoStar NLP API', description='CoStar API powering NLP-Based Applications')
parser = reqparse.RequestParser()
parser.add_argument('request', type=str, required=True)
nlp = NLP()

@api.route('/nlp')
class NlpEndpoints(Resource):

    @api.expect(parser, validate=True)
    def get(self):
        args = parser.parse_args()
        request = args['request']
        nlp_results = nlp.parse(request)
        apiCreator = ApartmentsAPICreator(nlp_results)
        Apartments_API_Call = apiCreator.create()
        headers = {'Content-Type': 'application/json'}
        Apartments_API_Call_Result = requests.post("https://www.apartments.com/services/search/",
                                                   data=json.dumps(Apartments_API_Call.data), headers=headers)
        return Apartments_API_Call

        # our_call = parse("Show me all.")
        # j = json.dumps(our_call.data)
        # print(r.headers)
        # print(r.text)


if __name__ == '__main__':
    app.run()
