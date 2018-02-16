from flask import Flask
from flask_restplus import Resource, Api, reqparse
from Api.NLP import NLP
from Api.Models.Apartments.ApartmentsAPICreator import ApartmentsAPICreator
import requests
import json
import re

app = Flask(__name__)
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app, version='1.0', title='CoStar NLP API', description='CoStar API powering NLP-Based Applications')
parser = reqparse.RequestParser()
parser.add_argument('request', type=str, required=True)
nlp = NLP()
pattern = re.compile("(^[a-z0-9]*(?=|))|((?<=[0-9]~)[a-z0-9]*(?=|))")

@api.route('/nlp')
class NlpEndpoints(Resource):

    @api.expect(parser, validate=True)
    def get(self):
        args = parser.parse_args()
        request = args['request']
        nlp_results = nlp.parse(request)
        apiCreator = ApartmentsAPICreator(nlp_results)
        Apartments_API = apiCreator.create()
        Apartment_IDS, Search_Criteria = self.callSearchEndpointWith(Apartments_API)
        results = self.callInfoEndpointWith(Apartment_IDS, Search_Criteria)
        return results


    def callSearchEndpointWith(self, data):
        data = json.dumps(data.data)
        headers = {'Content-Type': 'application/json'}
        result = requests.post("https://www.apartments.com/services/search/", data=data, headers=headers)
        search_criteria = json.loads(result.text)["SearchCriteria"]
        result = self.cleanResult(result)
        return result, search_criteria

    def callInfoEndpointWith(self, apartment_keys, search_criteria):
        apartment_results = {}
        apartments = []
        for key in apartment_keys:

            call = {}
            call['ListingKeys'] = [str(key)]
            call['SearchCriteria'] = search_criteria
            data = json.dumps(call)
            headers = {'Content-Type': 'application/json'}
            result = requests.post("https://www.apartments.com/services/property/infoCardData", data=data, headers=headers)
            apartment_instance = json.loads(result.text)
            apartments.append(apartment_instance)

        apartment_results['aparments'] = apartments
        return apartment_results

    def cleanResult(self, result):
        result = json.loads(result.text)
        cl = result['PinsState']['cl']
        ids = re.findall(pattern, cl)
        ids_list = [ids[0][0]] + [id[1] for id in ids[1:]]
        return ids_list


if __name__ == '__main__':
    app.run()
