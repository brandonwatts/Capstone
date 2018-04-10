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
    return extractions
