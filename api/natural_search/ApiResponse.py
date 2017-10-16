"""APIResponse.py is the response the the api/nlp endpoint"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

class ApiResponse(object):
    def __init__(self, tokens, POSTags):
        self.tokens = tokens
        self.POSTags = POSTags
