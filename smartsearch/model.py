import spacy
import us

nlp = spacy.load('en_core_web_lg')

extractions = {}

def member_of(values):
    return lambda value: value.lower() in values

MAX_SQFT_HEADERS = ["at least", "above", "over", "greater than", "more than", "bigger than"]
MIN_SQFT_HEADERS = ["at most", "below", "under", "cheaper than", "less than", "smaller than"]

IS_MIN_SQFT_HEADER = nlp.vocab.add_flag(member_of(MIN_SQFT_HEADERS))
IS_MAX_SQFT_HEADER = nlp.vocab.add_flag(member_of(MAX_SQFT_HEADERS))

MAX_PRICE_HEADERS = ["at least", "above", "over", "greater than", "more than", "more expensive than"]
MIN_PRICE_HEADERS = ["at most", "below", "under", "cheaper than", "less than", "less expensive than"]

IS_MIN_PRICE_HEADER = nlp.vocab.add_flag(member_of(MIN_PRICE_HEADERS))
IS_MAX_PRICE_HEADER = nlp.vocab.add_flag(member_of(MAX_PRICE_HEADERS))

MAX_BED_HEADERS = ["at least", "above", "over", "more than"]
MIN_BED_HEADERS = ["at most", "below", "under", "less than", "fewer than"]

IS_MIN_BED_HEADER = nlp.vocab.add_flag(member_of(MIN_BED_HEADERS))
IS_MAX_BED_HEADER = nlp.vocab.add_flag(member_of(MAX_BED_HEADERS))

IS_NEGATION = nlp.vocab.add_flag(member_of(["no", "not"]))

STREET_LABELS = [label.lower() for label in open("smartsearch/street_labels.txt","r").read().split(",")]

IS_STREET_LABEL = nlp.vocab.add_flag(member_of(STREET_LABELS))

STATES = [state.name.lower() for state in us.states.STATES] + [state.abbr.lower() for state in us.states.STATES]

IS_STATE = nlp.vocab.add_flag(member_of(STATES))

CITIES = [line.split(",")[0].strip().lower() for line in open("smartsearch/cities.txt","r").readlines()]

IS_CITY = nlp.vocab.add_flag(member_of(CITIES))
