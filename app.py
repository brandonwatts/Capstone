from flask import Flask
from flask_restplus import Resource, Api, reqparse
from Api.api import response

app = Flask(__name__)
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app, version='1.0', title='CoStar NLP API', description='CoStar API powering NLP-Based Applications')
parser = reqparse.RequestParser()
parser.add_argument('request', type=str, required=True)


@api.route('/nlp')
class NlpEndpoints(Resource):

    @api.expect(parser, validate=True)
    def get(self):
        args = parser.parse_args()
        request = args['request']
        return response(request)


if __name__ == '__main__':
    app.run()
