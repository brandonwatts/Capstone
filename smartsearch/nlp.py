import re

from smartsearch.matcher import field_matcher, phrase_matcher
from smartsearch.model import extractions, nlp
from smartsearch.referencer import extract_references


def static_args(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_args(squarefoot=re.compile(r"(?<!\w)(square|sq(\.)?)(\s)?(feet|foot|ft(\.)?)(?!\w)", re.I))
def preprocess(text):
    return preprocess.squarefoot.sub("squarefoot", text)


def parse(text):
    extractions.clear()
    doc = nlp(preprocess(text))

    for span in [doc[head:tail] for (match_id, head, tail) in phrase_matcher(doc)]:
        try:
            span.merge()
        except IndexError:
            pass
    
    field_matcher(doc)
    extract_references(doc, extractions)
    
    if is_negated(doc):
        negate(extractions)
    
    return extractions

def is_negated(doc):
    token = doc[0]
    while token != token.head:
        token = token.head
    
    children = [i.text.lower() for i in token.children]
    negations = ["no", "not", "n't", "nothing", "nowhere"]
    
    if any(i in children for i in negations):
        return True
    
    # this could be improved using what's in references
    topics = ["house", "apartment", "building", "anywhere", "place"]
    
    for i in token.children:
        if i.text.lower() in topics:
            grandchildren = [j.text.lower() for j in i.children]
            if any(j in grandchildren for j in negations):
                return True
    
    return False

def negate(extractions):
    if extractions.get("max_price") and not extractions.get("min_price"):
        extractions["min_price"] = extractions["max_price"]
        extractions["max_price"] = None
    if extractions.get("min_price") and not extractions.get("max_price"):
        extractions["max_price"] = extractions["min_price"]
        extractions["min_price"] = None

    if extractions.get("max_sqft") and not extractions.get("min_sqft"):
        extractions["min_sqft"] = extractions["max_sqft"]
        extractions["max_sqft"] = None
    if extractions.get("min_sqft") and not extractions.get("max_sqft"):
        extractions["max_sqft"] = extractions["min_sqft"]
        extractions["min_sqft"] = None
        
    if extractions.get("max_bed") and not extractions.get("min_bed"):
        extractions["min_bed"] = extractions["max_bed"]
        extractions["max_bed"] = None
    if extractions.get("min_bed") and not extractions.get("max_bed"):
        extractions["max_bed"] = extractions["min_bed"]
        extractions["min_bed"] = None
    
    if extractions.get("dog_friendly"):
        extractions.get["dog_friendly"] = False
    if extractions.get("cat_friendly"):
        extractions.get["cat_friendly"] = False
