import re
import spacy
from api.natural_search.Models.ApiResponse import ApiResponse
from api.natural_search.Models.Schemas.ApiSchema import ApiSchema
from spacy.strings import StringStore

nlp = spacy.load("en")

us_states = StringStore([
    'ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA',
    'COLORADO', 'CONNETICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA',
    'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA',
    'KANSAS', 'KENTUCKY', 'LOISIANA', 'MAINE', 'MARYLAND',
    'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI',
    'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY',
    'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO',
    'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH  CAROLINA',
    'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT',
    'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING'])

"""
us_state_abbreviations = StringStore([
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
"""

def response(request):
    doc = nlp(request)

    api_response = ApiResponse(
        state =        extract_state(doc),
        city =         extract_city(doc),
        zip_code =     extract_zip_code(doc),
        min_sqft =     extract_min_sqft(doc),
        max_sqft =     extract_max_sqft(doc),
        min_price =    extract_min_price(doc),
        max_price =    extract_max_price(doc),
        min_bed =      extract_min_bed(doc),
        max_bed =      extract_max_bed(doc),
        pricing_type = extract_pricing_type(doc),
        address =      extract_address(doc),
        build_year=    extract_build_year(doc),
        dog_friendly = extract_dog_friendly(doc))
    
    schema = ApiSchema()
    return schema.dump(api_response)

def find_head(token, function):
    while token != token.head:
        if function(token):
            return token
        token = token.head

def is_noun(token):
    noun_tags = ('NN', 'NNS', 'NNP', 'NNPS')
    return token.tag_ in noun_tags

def is_min_quantity(token):
    min_tags = ("MORE", "GREATER", "OVER")
    return any(child.text.upper() in min_tags for child in token.children)

def is_max_quantity(token):
    max_tags = ("LESS", "UNDER")
    return any(child.text.upper() in max_tags for child in token.children)

def is_state_text(token):
    return token.lemma_.upper() in us_states

def extract_state(doc):
    return [token.lemma_ for token in doc
            if token.ent_type_ == "GPE" and is_state_text(token)]

def extract_city(doc):
    return [token.text for token in doc
            if token.ent_type_ == "GPE" and not is_state_text(token)]

def extract_zip_code(doc):
    return [token.text for token in doc if
            re.match('\d{5}', token.text) and list(token.children) == []]

def is_price(token):
    return token.ent_type_ == "MONEY" and token.pos_ == "NUM"

def extract_min_price(doc):
    return [token.text
            for token in doc if is_price(token) and not is_max_quantity(token)]

def extract_max_price(doc):
    return [token.text
            for token in doc if is_price(token) and is_max_quantity(token)]

def find_pricing_type(token):
    for child in token.children:
        if child.text.upper() == "PER":
            for pricing in child.children:
                return pricing

def extract_pricing_type(doc):
    types = []
    for token in doc:
        if is_price(token):
            result = find_pricing_type(token)
            if result:
                types.append(result.text)
    return types

def is_sqft(token):
    tags = ('FEET', 'FOOT', 'SQUAREFEET', 'SQUAREFOOT',
            'SQUARE', 'SQFT', 'SQ', 'FT')
    return token.pos_ == "NUM" and token.head.lemma_.upper() in tags

def extract_min_sqft(doc):
    return [token.text for token in doc
            if is_sqft(token) and not is_max_quantity(token)]

def extract_max_sqft(doc):
    return [token.text for token in doc
            if is_sqft(token) and is_max_quantity(token)]

def is_bed(token):
    tags = ('BED', 'ROOM', 'BEDROOM', 'PEOPLE')
    return token.pos_ == "NUM" and token.head.lemma_.upper() in tags

def extract_min_bed(doc):
    return [token.text for token in doc
            if is_bed(token) and not is_max_quantity(token)]

def extract_max_bed(doc):
    return [token.text for token in doc
            if is_bed(token) and is_max_quantity(token)]

def extract_address(doc):
    return [token.text for token in doc if token.ent_type_ == "FAC"]

def extract_build_year(doc):
    return [token.text for token in doc if token.ent_type_ == "DATE"]

def extract_dog_friendly(doc):
    return doc.similarity(nlp(u'dog friendly')) > .50
