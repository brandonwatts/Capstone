import re
import spacy
from api.natural_search.Models.ApiResponse import ApiResponse
from api.natural_search.Models.Schemas.ApiSchema import ApiSchema

nlp = spacy.load("en")

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
    doc = nlp(request)
    states = extract_states(doc.ents)
    city = extract_city(doc.ents)
    zip_code = extract_zip(request)
    api_response = ApiResponse(states=states, city=city, zip_code=zip_code)
    schema = ApiSchema()
    return schema.dump(api_response)


def extract_states(ents):
    return list(filter(lambda ent: ent.label_ == "GPE" and ent.text in us_states, ents))


def extract_city(ents):
    return list(filter(lambda ent: ent.label_ == "GPE" and ent.text not in us_states, ents))


def extract_zip(text):
    zip_regex = re.compile('\\b\d{5}\\b')
    return zip_regex.findall(text)
