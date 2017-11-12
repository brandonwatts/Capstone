from nltk import word_tokenize
from nltk.tag import StanfordNERTagger
import re

from ApiResponse import ApiResponse
from ApiSchema import ApiSchema

'''nlp_operations.py contains all the operations that are used to transform a request to an CoStar API request '''

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

st = StanfordNERTagger(
    '/Users/brandonwatts/Desktop/Capstone/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz',
    '/Users/brandonwatts/Desktop/Capstone/stanford-ner-2017-06-09/stanford-ner.jar',
    encoding='utf-8')

us_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine' 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South  Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
    'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming'
]


def response(request):
    states = extract_states(request)
    city = extract_city(request)
    zip_code = extract_zip(request)
    api_response = ApiResponse(states=states, city=city, zip_code=zip_code)
    schema = ApiSchema()
    return schema.dump(api_response)


def city_or_state(location):
    if location in us_states:
        return "State"
    else:
        return "City"


def extract_states(text):
    return map(lambda x: x[0], filter(lambda x: x[1] == "State", extract_locations(text)))


def extract_city(text):
    return map(lambda x: x[0], filter(lambda x: x[1] == "City", extract_locations(text)))


def extract_zip(text):
    zip_regex = re.compile('\\b\d{5}\\b')
    return zip_regex.findall(text)


def extract_locations(text):
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    locations = map(lambda x: (x, city_or_state(x)),
                    map(lambda x: x[0], filter(lambda x: x[1] == "LOCATION", classified_text)))
    return locations
