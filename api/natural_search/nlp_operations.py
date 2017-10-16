import nlp_api as gNLP
import speech_api as gSpeech
import nltk
from ApiResponse import ApiResponse
from ApiSchema import ApiSchema

'''nlp_operations.py contains all the operations that are used to transform a request to an CoStar API request '''

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


def response(request):
    tokens = nltk.word_tokenize(request)
    tagged = nltk.pos_tag(tokens)
    api_response = ApiResponse(tokens=tokens, POSTags=tagged)
    schema = ApiSchema()
    return schema.dump(api_response)
