from smartsearch.model import nlp

referencers = {}


def register():
    """This is a helper method to add all functions that have the @register decorator to the referencers dict"""
    def decorator(func):
        referencers[func.__name__] = func

    return decorator


def contains_reference(doc, reference, threshold=0.60):
    """This method iterates through all the tokens in a doc object and checks their word vector similarity.

        Note:
            Since we are using the small pre-trained word vectors there may be some edge cases where words are so close
            in vector space that they trip other references. For example "dog friendly" and "cat friendly" are so
            similar of topics there are cases where they can both be true when the intention that only one of them is.

        Args:
            doc (doc): This is a spacy doc object.
            reference (string): word or group of words you are comparing to
            threshold (float): This is the "threshold" of the match. The closer to 1, the more exact the match must be
                               and the closer to 0, the more false positives begin to match.

        Returns:
            (bool): True if text contains a reference, False otherwise.

        """
    ref = nlp(reference)
    for token in doc:
        if token.similarity(ref) > threshold:
            return True
    return False


def extract_references(doc, extractions):
    for field in referencers:
        extractions[field] = referencers[field](doc)


@register()
def dog_friendly(doc):
    return contains_reference(doc, reference="dog")


@register()
def cat_friendly(doc):
    return contains_reference(doc, reference="cat")


@register()
def has_pool(doc):
    return contains_reference(doc, reference="pool")


@register()
def has_elevator(doc):
    return contains_reference(doc, reference="elevator")


@register()
def has_fitness_center(doc):
    return contains_reference(doc, reference="fitness") or contains_reference(doc, reference="gym")


@register()
def has_wheelchair_access(doc):
    return contains_reference(doc, reference="wheelchair") or contains_reference(doc, reference='handicapped')


@register()
def has_dishwasher(doc):
    return contains_reference(doc, reference="dishwasher")


@register()
def has_air_conditioning(doc):
    return contains_reference(doc, reference="air conditioning")


@register()
def has_parking(doc):
    return contains_reference(doc, reference="parking")


@register()
def furnished(doc):
    return contains_reference(doc, reference="furnished") or contains_reference(doc, reference="furniture")


@register()
def has_laundry_facilities(doc):
    return (contains_reference(doc, reference="laundry") or contains_reference(doc, reference="washer") \
           or contains_reference(doc, reference="dryer"))
