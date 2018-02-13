import re
import spacy
from Api.Models.Schemas.ApiSchema import ApiSchema
from Api.Models.ApiResponseBuilder import ApiResponseBuilder
from spacy.strings import StringStore
from spacy.matcher import Matcher
from spacy.attrs import LEMMA, ENT_TYPE

response_builder = ApiResponseBuilder()
nlp = spacy.load('en_core_web_lg')
us_states = StringStore().from_disk('Api/StringStore/States')
us_state_abbreviations = StringStore().from_disk('Api/StringStore/StateAbbreviations')

def response(request):
    matcher = Matcher(nlp.vocab)
    star_rating_pattern = [{'IS_DIGIT': True}, {'LEMMA': 'star'}]
    search_radius_pattern = [{'IS_DIGIT': True}, {'ENT_TYPE': 'QUANTITY'}]
    matcher.add('StarRating', on_star_rating_match, star_rating_pattern)
    matcher.add('SearchRadius', on_search_radius_match, search_radius_pattern)
    doc = nlp(request)
    matcher(doc)
    schema = ApiSchema()
    define_extraction_points(doc)
    return schema.dump(response_builder.build())

def on_search_radius_match(matcher, doc, id, matches):
    match_id, start, end = matches[id]
    searchRadius = doc[start:end]
    response_builder.add_extraction_point("search_radius", searchRadius)

def on_star_rating_match(matcher, doc, id, matches):
    star_ratings = []
    for match in matches:
        match_id, start, end = match
        starRating = doc[start:end]
        star_ratings.append(starRating.text)
    response_builder.add_extraction_point("star_rating", star_ratings)

def define_extraction_points(doc):

    response_builder.add_extraction_point("state", extract_state(doc))
    response_builder.add_extraction_point("city", extract_city(doc))
    response_builder.add_extraction_point("zip_code", extract_zip_code(doc))
    response_builder.add_extraction_point("min_sqft", extract_min_sqft(doc))
    response_builder.add_extraction_point("max_sqft", extract_max_sqft(doc))
    response_builder.add_extraction_point("min_price", extract_min_price(doc))
    response_builder.add_extraction_point("max_price", extract_max_price(doc))
    response_builder.add_extraction_point("min_bed", extract_min_bed(doc))
    response_builder.add_extraction_point("max_bed", extract_max_bed(doc))
    response_builder.add_extraction_point("pricing_type", extract_pricing_type(doc))
    response_builder.add_extraction_point("address", extract_address(doc))
    response_builder.add_extraction_point("build_year", extract_build_year(doc))
    response_builder.add_extraction_point("dog_friendly", extract_dog_friendly(doc))
    response_builder.add_extraction_point("cat_friendly", extract_cat_friendly(doc))
    response_builder.add_extraction_point("has_pool", extract_has_pool(doc))
    response_builder.add_extraction_point("has_elevator", extract_has_elevator(doc))
    response_builder.add_extraction_point("has_fitness_center", extract_has_fitness_center(doc))
    response_builder.add_extraction_point("has_wheelchair_access", extract_has_wheelchair_access(doc))
    response_builder.add_extraction_point("has_dishwasher", extract_has_dishwasher(doc))
    response_builder.add_extraction_point("has_air_conditioning", extract_has_air_conditioning(doc))
    response_builder.add_extraction_point("has_parking", extract_has_parking(doc))
    response_builder.add_extraction_point("is_furnished", extract_is_furnished(doc))
    response_builder.add_extraction_point("has_laundry_facilities", extract_has_laundry_facilities(doc))
    response_builder.add_extraction_point("property_type", extract_property_type(doc))

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
    max_tags = ("LESS", "UNDER", "BELOW")
    return any(child.text.upper() in max_tags for child in token.children)

def is_state_text(token):
    return token.lemma_.upper() in us_states

def extract_state(doc):
    return [ent.upper() for ent in doc.ents if ent.label_ == 'GPE' and ent.text.upper() in us_states]

def extract_city(doc):
    return [ent.upper() for ent in doc.ents if ent.label_ == 'GPE' and ent.text.upper() not in us_states]

def extract_zip_code(doc):
    return [token.text for token in doc if
            re.match('\d{5}', token.text) and list(token.children) == []]

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

def extract_has_parking(doc):
    return containsReferenceTo(doc=doc, reference="parking")

def extract_is_furnished(doc):
    return containsReferenceTo(doc=doc, reference="furniture")

def extract_has_laundry_facilities(doc):
    return containsReferenceTo(doc=doc, reference="laundry")

def extract_property_type(doc):
    return "pt_industrial, pt_retail, pt_shopping_center, pt_multifamily, pt_specialty, pt_office, pt_health_care," \
           "pt_hospitality, pt_sports_and_entertainment, pt_land, pt_residential_income"

def containsReferenceTo(doc, reference, MATCH_THRESHOLD=0.6):
    containsReference = False
    ref = nlp(reference)
    for token in doc:
        if token.similarity(ref) > MATCH_THRESHOLD:
            containsReference = True
    return containsReference

print(response("Apartments in New York, New York that are dog friendly."))