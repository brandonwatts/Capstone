import re
import spacy
from api.natural_search.Models.ApiResponse import ApiResponse
from api.natural_search.Models.Schemas.ApiSchema import ApiSchema
from spacy.strings import StringStore

nlp = spacy.load("en")

us_states = StringStore([
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
])


def response(request):
    doc = nlp(request)
    states = extract_states(doc)
    city = extract_city(doc)
    zip_code = extract_zip(doc)
    sq_ft = extract_square_footage(doc)
    price = extract_price(doc)
    address = extract_address(doc)
    api_response = ApiResponse(states=states, city=city, zip_code=zip_code, sq_ft=sq_ft, price=price, address=address)
    schema = ApiSchema()
    return schema.dump(api_response)


def extract_states(doc):
    return list(filter(lambda token: token.ent_type_ == "GPE" and token.text in us_states, doc))


def extract_city(doc):
    return list(filter(lambda token: token.ent_type_ == "GPE" and token.text not in us_states, doc))


"""
Extracts money and currency values (entities labelled as MONEY) and checks the
dependency tree to find the noun they are referring to. 
***** Will eventually check that it is referring to some type of housing ****
"""
def extract_price(doc):

    for span in [*list(doc.ents), *list(doc.noun_chunks)]:
        span.merge()

    relations = []
    for money in filter(lambda token: token.ent_type_ == 'MONEY', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [token for token in money.head.lefts if token.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))
    return relations


def extract_square_footage(doc):
    return list(filter(lambda token: token.ent_type_ == "QUANTITY", doc))


def extract_zip(doc):
    for number in filter(lambda token: token.ent_type_ == "CARDINAL" or token.ent_type_ == "DATE", doc):
        if re.match('\d{5}', number.text):
            return number.text
    return ""


def extract_address(doc):
    return list(filter(lambda token: token.ent_type_ == "FAC", doc))
