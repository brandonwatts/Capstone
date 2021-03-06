from spacy.matcher import Matcher

from smartsearch.model import *

# phrase matchers

def patterns(phrases):
    return [[{"LOWER": word} for word in phrase.split()] for phrase in phrases]

phrase_matcher = Matcher(nlp.vocab)
phrase_matcher.add("city", None, *patterns(CITIES))
phrase_matcher.add("state", None, *patterns(STATES))
phrase_matcher.add("max_header", None, *patterns(set(MAX_SQFT_HEADERS + MAX_PRICE_HEADERS + MAX_BED_HEADERS)))
phrase_matcher.add("min_header", None, *patterns(set(MIN_SQFT_HEADERS + MIN_PRICE_HEADERS + MIN_BED_HEADERS)))

FIRST_TOKEN = 0
LAST_TOKEN = -1
NEXT_TO_LAST_TOKEN = -2

# field matcher

def extract(index):
    def callback(matcher, doc, i, matches):
        match_id, head, tail = matches[i]
        extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]] = doc[head:tail][index].text
    return callback

def extract_range(start, end):
    def callback(matcher, doc, i, matches):
        match_id, head, tail = matches[i]
        extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]] = doc[head:tail][start:end].text
    return callback

def extract_all(matcher, doc, i, matches):
        match_id, head, tail = matches[i]
        extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]] = doc[head:tail].text

def extract_lefts(matcher, doc, i, matches):
        match_id, head, tail = matches[i]
        text = " ".join(token.text for token in doc[head].lefts) + " " + doc[head].text
        extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]] = text

def extract_append(index):
    def callback(matcher, doc, i, matches):
        match_id, head, tail = matches[i]
        if doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN] in extractions:
            extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]].append(doc[head:tail][index].text)
        else:
            extractions[doc.vocab.strings[match_id][:NEXT_TO_LAST_TOKEN]] = [doc[head:tail][index].text]
    return callback

field_matcher = Matcher(nlp.vocab)

# rating patterns

field_matcher.add("star_rating 1", extract_append(FIRST_TOKEN), [{"IS_DIGIT": True}, {"LEMMA": "star"}])

# build year patterns

field_matcher.add("build_year 1", extract(FIRST_TOKEN), [{'LOWER': 'built'}, {'LOWER': 'in'}, {'SHAPE': 'dddd'}])

# sqft patterns

field_matcher.add("max_sqft 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_SQFT_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "squarefoot"}])
field_matcher.add("min_sqft 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_SQFT_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "squarefoot"}])
field_matcher.add("max_sqft 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_SQFT_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "squarefoot"}])
field_matcher.add("min_sqft 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_SQFT_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "squarefoot"}])
field_matcher.add("min_sqft 3", extract(NEXT_TO_LAST_TOKEN), [{IS_MAX_SQFT_HEADER: False, IS_MIN_SQFT_HEADER: False}, {"IS_DIGIT": True}, {"LOWER": "squarefoot"}])

# price patterns

field_matcher.add("max_price 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "dollar"}])
field_matcher.add("min_price 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "dollar"}])
field_matcher.add("max_price 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "dollar"}])
field_matcher.add("min_price 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "dollar"}])
field_matcher.add("max_price 3", extract(NEXT_TO_LAST_TOKEN), [{IS_MAX_PRICE_HEADER: False, IS_MIN_PRICE_HEADER: False}, {"IS_DIGIT": True}, {"LEMMA": "dollar"}])
field_matcher.add("max_price 4", extract(LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_PRICE_HEADER: True}, {"LOWER": "$"}, {"IS_DIGIT": True}])
field_matcher.add("min_price 4", extract(LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_PRICE_HEADER: True}, {"LOWER": "$"}, {"IS_DIGIT": True}])
field_matcher.add("max_price 5", extract(LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_PRICE_HEADER: True}, {"LOWER": "$"}, {"IS_DIGIT": True}])
field_matcher.add("min_price 5", extract(LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_PRICE_HEADER: True}, {"LOWER": "$"}, {"IS_DIGIT": True}])
field_matcher.add("max_price 6", extract(LAST_TOKEN), [{IS_MAX_PRICE_HEADER: False, IS_MIN_PRICE_HEADER: False}, {"LOWER": "$"}, {"IS_DIGIT": True}])
field_matcher.add("max_price 7", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "$"}])
field_matcher.add("min_price 7", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "$"}])
field_matcher.add("max_price 8", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "$"}])
field_matcher.add("min_price 8", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_PRICE_HEADER: True}, {"IS_DIGIT": True}, {"LOWER": "$"}])
field_matcher.add("max_price 9", extract(NEXT_TO_LAST_TOKEN), [{IS_MAX_PRICE_HEADER: False, IS_MIN_PRICE_HEADER: False}, {"IS_DIGIT": True}, {"LOWER": "$"}])

# bedroom patterns

field_matcher.add("max_bed 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bed"}])
field_matcher.add("min_bed 1", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bed"}])
field_matcher.add("max_bed 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bed"}])
field_matcher.add("min_bed 2", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bed"}])
field_matcher.add("min_bed 3", extract(NEXT_TO_LAST_TOKEN), [{IS_MAX_BED_HEADER: False, IS_MIN_BED_HEADER: False}, {"IS_DIGIT": True}, {"LEMMA": "bed"}])
field_matcher.add("max_bed 4", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MAX_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bedroom"}])
field_matcher.add("min_bed 4", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True, "OP": "!"}, {IS_MIN_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bedroom"}])
field_matcher.add("max_bed 5", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MIN_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bedroom"}])
field_matcher.add("min_bed 5", extract(NEXT_TO_LAST_TOKEN), [{IS_NEGATION: True}, {IS_MAX_BED_HEADER: True}, {"IS_DIGIT": True}, {"LEMMA": "bedroom"}])
field_matcher.add("min_bed 6", extract(NEXT_TO_LAST_TOKEN), [{IS_MAX_BED_HEADER: False, IS_MIN_BED_HEADER: False}, {"IS_DIGIT": True}, {"LEMMA": "bedroom"}])

# address patterns

field_matcher.add("address 1", extract_lefts, [{IS_STREET_LABEL: True}])

# state patterns

field_matcher.add("state 1", extract(FIRST_TOKEN), [{IS_CITY: False, IS_STATE: True, "POS": "PROPN"}])
field_matcher.add("state 2", extract(LAST_TOKEN), [{IS_CITY: True}, {"LOWER": ",", "OP": "?"}, {IS_CITY: True, IS_STATE: True, "POS": "PROPN"}])

# city patterns

field_matcher.add("city 1", extract(FIRST_TOKEN), [{IS_CITY: True, IS_STATE: False}, {"LOWER": "city", "OP": "?"}])
field_matcher.add("city 2", extract(FIRST_TOKEN), [{IS_CITY: True, IS_STATE: True}, {"LOWER": "city", "OP": "?"}, {"LOWER": ",", "OP": "?"}, {IS_STATE: True}])

# zip patterns

zip_matcher = Matcher(nlp.vocab)

zip_matcher.add("zip_code 1", extract(FIRST_TOKEN), [{"IS_DIGIT": True, "LENGTH": 5}])
