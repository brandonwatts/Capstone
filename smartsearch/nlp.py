import re

from smartsearch.matcher import field_matcher, phrase_matcher, zip_matcher
from smartsearch.model import extractions, nlp
from smartsearch.referencer import extract_references


def static_args(**kwargs):
    """
    NEEDS DOC
    # TODO
    """

    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def remove_commas(match):
    match = match.group()
    return re.sub(',', '', match)


@static_args(squarefoot=re.compile(r"(?<!\w)(square|sq(\.)?)(\s)?(feet|foot|ft(\.)?)(?!\w)"),
             numberRE=re.compile(r"\$?\d+,?\d+", re.I))
def preprocess(text):
    """This method is used to preprocess text before any nlp is done on it.

    The method first turns any variation of squarefoot into "squarefoot" so we do not have to check for it later in
    the pipeline. It also removes commas from the numbers as its easier piped into API as an integer.

    Note:
        This method is always called before nlp() is called.

    Args:
        text (str): This is the block of text that we wish to preprocess.

    Returns:
        (str): The text that has been preprocessed.

    """
    sqftSub = preprocess.squarefoot.sub("squarefoot", text)
    numberSub = preprocess.numberRE.sub(remove_commas, sqftSub)
    return numberSub


def parse(text):
    """
        NEEDS DOC
        # TODO
    """
    extractions.clear()
    doc = nlp(preprocess(text))

    for span in [doc[head:tail] for (match_id, head, tail) in phrase_matcher(doc)]:
        try:
            span.merge()
        except IndexError:
            pass
    
    for span in [doc[head:tail] for (match_id, head, tail) in field_matcher(doc)]:
        try:
            span.merge()
        except IndexError:
            pass
    
    zip_matcher(doc)
    extract_references(doc, extractions)

    if is_negated(doc):
        negate(extractions)

    return extractions


def is_negated(doc):
    """This method checks if the sentence has been negated indicating the user wants the opposite of what he/she asked.

    Ex. "Show me all the apartments that are NOT dog friendly". This works by starting at the head of the sentence and
    then navigating through the parse tree looking for a negated target word.

    Args:
        doc (doc): This is a spacy doc object.

    Returns:
        (bool): True if text contains a negation, False otherwise.

    """
    token = doc[0]
    while token != token.head:
        token = token.head

    children = [i.text.lower() for i in token.children]
    negations = ["no", "not", "n't", "nothing", "nowhere"]

    if any(i in children for i in negations):
        return True

    # this could be improved using what's in references
    topics = [
        "home", "homes",
        "house", "houses",
        "apartment", "apartments",
        "building", "buildings",
        "place", "places",
        "residence", "residences",
        "anywhere",
        "anyplace"]

    for i in token.children:
        if i.text.lower() in topics:
            grandchildren = [j.text.lower() for j in i.children]
            print(grandchildren)
            if any(j in grandchildren for j in negations):
                return True

    return False


def negate(extractions):
    """
    NEEDS DOC
    # TODO
    """
    if extractions.get("max_price") and not extractions.get("min_price"):
        extractions["min_price"] = extractions["max_price"]
        extractions["max_price"] = None
    elif extractions.get("min_price") and not extractions.get("max_price"):
        extractions["max_price"] = extractions["min_price"]
        extractions["min_price"] = None

    if extractions.get("max_sqft") and not extractions.get("min_sqft"):
        extractions["min_sqft"] = extractions["max_sqft"]
        extractions["max_sqft"] = None
    elif extractions.get("min_sqft") and not extractions.get("max_sqft"):
        extractions["max_sqft"] = extractions["min_sqft"]
        extractions["min_sqft"] = None

    if extractions.get("max_bed") and not extractions.get("min_bed"):
        extractions["min_bed"] = extractions["max_bed"]
        extractions["max_bed"] = None
    elif extractions.get("min_bed") and not extractions.get("max_bed"):
        extractions["max_bed"] = extractions["min_bed"]
        extractions["min_bed"] = None

    if extractions.get("dog_friendly"):
        extractions.get["dog_friendly"] = False
    if extractions.get("cat_friendly"):
        extractions.get["cat_friendly"] = False
