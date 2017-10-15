import os
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from oauth2client.client import GoogleCredentials

'''Set the Credentials'''
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "CMSC323-edf53f65e546.json")
credentials = GoogleCredentials.get_application_default()


def parse_syntax(text):
    '''
    Method to parse the syntax from a sentence
    :param text: Text of a sentence
    :return: response from Google Natural Language API Syntax Parser
    '''
    client = language.LanguageServiceClient()           # Instantiate a new Language Client

    if isinstance(text, six.binary_type):               # Make sure the format is correct
        text = text.decode('utf-8')

    document = types.Document(                          # Set the document type
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    tokens = client.analyze_syntax(document).tokens     # Response from Google Natural Language API

    return tokens


def parse_entities(text):
    '''
    Method to parse the entities from a sentence
    :param text: Text of a sentence
    :return: response from Google Natural Language API Syntax Parser
    '''
    client = language.LanguageServiceClient()               # Instantiate a new Language Client

    if isinstance(text, six.binary_type):                   # Make sure the format is correct
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(                              # Set the document type
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document).entities   # Response from Google Natural Language API

    return entities
