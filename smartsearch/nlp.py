import re

import spacy
import us

from smartsearch.fieldmatcher import FieldMatcher
from smartsearch.referencer import extract_references

nlp = spacy.load('en_core_web_lg')
extractions = {}
matcher = FieldMatcher(NLP._nlp.vocab, extractions)

def static_args(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_args(squarefoot=re.compile(r"(?<!\w)(square|sq(\.)?)(\s)?(feet|foot|ft(\.)?)(?!\w)", re.I))
def preprocess(text):
    return preprocess.squarefoot.sub("squarefoot", request)

def parse(text):
    extractions.clear()
    doc = nlp(preprocess(text))
    matcher(doc)
    
    self.extractions["state"] = extract_state(doc)
    self.extractions["city"] = extract_city(doc)
    self.extractions["zip_code"] = extract_zip_code(doc)
    self.extractions["address"] = extract_address(doc)
    
    extract_references(doc, extractions)
    return extractions

def extract_state(doc):
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            state = us.states.lookup(entity.text)
            if state:
                return state.abbr

def extract_city(doc):
    for entity in doc.ents:
        if entity.label_ == 'GPE' and us.states.lookup(entity.text) is None:
            return entity.lemma_.title()

def extract_zip_code(doc):
    return [token.text for token in doc if
            re.match('\d{5}', token.text) and list(token.children) == []]

def extract_address(doc):
    return [token.text for token in doc if token.ent_type_ == "FAC"]

