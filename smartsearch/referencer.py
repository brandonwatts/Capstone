from smartsearch import nlp

referencers = {}

def register():
    def decorator(func):
        referencers[func.__name__] = func
    return decorator

def containsReferenceTo(doc, reference, threshold=0.65):
    ref = nlp(reference)
    for token in doc:
        if token.similarity(ref) > threshold:
            return True
    return False

@register()
def dog_friendly(doc):
    return containsReferenceTo(doc, reference="dog")

@register()
def cat_friendly(doc):
    return containsReferenceTo(doc, reference="cat")

@register()
def has_pool(doc):
    return containsReferenceTo(doc, reference="pool")

@register()
def has_elevator(doc):
    return containsReferenceTo(doc, reference="elevator")

@register()
def has_fitness_center(doc):
    return containsReferenceTo(doc, reference="fitness")

@register()
def has_wheelchair_access(doc):
    return containsReferenceTo(doc, reference="wheelchair") or containsReferenceTo(doc, reference='handicapped')

@register()
def has_dishwasher(doc):
    return containsReferenceTo(doc, reference="dishwasher")

@register()
def has_air_conditioning(doc):
    return containsReferenceTo(doc, reference="air conditioning")

@register()
def has_parking(doc):
    return containsReferenceTo(doc, reference="parking")

@register()
def furnished(doc):
    return containsReferenceTo(doc, reference="furnished", threshold=0.75)

@register()
def has_laundry_facilities(doc):
    return containsReferenceTo(doc, reference="laundry") 

def extract_references(doc, extractions):
    for field in referencers:
        extractions[field] = references[field](doc)
