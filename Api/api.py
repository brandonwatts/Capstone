import re
import spacy
from Api.Models.ApiResponse import ApiResponse
from Api.Models.Schemas.ApiSchema import ApiSchema
from spacy.strings import StringStore

nlp = spacy.load('en_core_web_lg')
us_states = StringStore().from_disk('Api/StringStore/States')
us_state_abbreviations = StringStore().from_disk('Api/StringStore/StateAbbreviations')


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
        dog_friendly = extract_dog_friendly(doc),
        cat_friendly = extract_cat_friendly(doc),
        has_pool =     extract_has_pool(doc),
        has_elevator = extract_has_elevator(doc),
        has_fitness_center = extract_has_fitness_center(doc),
        has_wheelchair_access = extract_has_wheelchair_access(doc),
        has_dishwasher = extract_has_dishwasher(doc),
        has_air_conditioning = extract_has_air_conditioning(doc),
        has_parking = extract_has_parking(doc),
        star_rating = extract_star_rating(doc),
        is_furnished = extract_is_furnished(doc),
        has_laundry_facilities = extract_has_laundry_facilities(doc),
        property_type = extract_property_type(doc),
        search_radius = extract_search_radius(doc))

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
    # TODO Min & Max Year
    return [token.text for token in doc if token.ent_type_ == "DATE"]

def extract_dog_friendly(doc):
    return containsReferenceTo(doc=doc, reference="dog")

def extract_cat_friendly(doc):
    return containsReferenceTo(doc=doc, reference="cat")

def extract_has_pool(doc):
    return containsReferenceTo(doc=doc, reference="pool")

def extract_has_elevator(doc):
    return containsReferenceTo(doc=doc, reference="elevator")

def extract_has_fitness_center(doc):
    return containsReferenceTo(doc=doc, reference="fitness")

def extract_has_wheelchair_access(doc):
    return containsReferenceTo(doc=doc, reference="wheelchair") or containsReferenceTo(doc=doc, reference='handicapped')

def extract_has_dishwasher(doc):
    return containsReferenceTo(doc=doc, reference="dishwasher")

def extract_has_air_conditioning(doc):
    return containsReferenceTo(doc=doc, reference="air conditioning")

def extract_star_rating(doc):
    return -1

def extract_has_parking(doc):
    return containsReferenceTo(doc=doc, reference="parking")

def extract_is_furnished(doc):
    return containsReferenceTo(doc=doc, reference="furniture")

def extract_has_laundry_facilities(doc):
    return containsReferenceTo(doc=doc, reference="laundry")

def extract_property_type(doc):
    return "pt_industrial, pt_retail, pt_shopping_center, pt_multifamily, pt_specialty, pt_office, pt_health_care," \
           "pt_hospitality, pt_sports_and_entertainment, pt_land, pt_residential_income"

def extract_search_radius(doc):
    return "5 miles"

def containsReferenceTo(doc, reference, MATCH_THRESHOLD=0.6):
    containsReference = False
    ref = nlp(reference)
    for token in doc:
        if token.similarity(ref) > MATCH_THRESHOLD:
            containsReference = True
    return containsReference
