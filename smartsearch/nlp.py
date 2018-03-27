import re

import spacy
import us

from smartsearch.fieldmatcher import FieldMatcher


class NLP:
    _nlp = spacy.load('en_core_web_lg')
    _squarefoot = re.compile(r"(?<!\w)(square|sq(\.)?)(\s)?(feet|foot|ft(\.)?)(?!\w)", re.I)
    
    def __init__(self):
        self.extractions = {}
        self._matcher = FieldMatcher(NLP._nlp.vocab, self.extractions)
    
    def parse(self, request):
        self.extractions.clear()
        doc = NLP._nlp(NLP._squarefoot.sub("squarefoot", request))
        self._matcher(doc)
        
        self.extractions["state"] = NLP._extract_state(doc)
        self.extractions["city"] = NLP._extract_city(doc)
        self.extractions["zip_code"] = NLP._extract_zip_code(doc)
        self.extractions["address"] = NLP._extract_address(doc)
        
        self._extract_references(doc)
        return self.extractions
    
    def _extract_references(self, doc):
        mappings = {
            "dog_friendly": NLP._dog_friendly,
            "cat_friendly": NLP._cat_friendly,
            "has_pool": NLP._has_pool,
            "has_elevator": NLP._has_elevator,
            "has_fitness_center": NLP._has_fitness_center,
            "has_wheelchair_access": NLP._has_wheelchair_access,
            "has_dishwasher": NLP._has_dishwasher,
            "has_air_conditioning": NLP._has_air_conditioning,
            "has_parking": NLP._has_parking,
            "furnished": NLP._furnished,
            "has_laundry_facilities": NLP._has_laundry_facilities
        }
        
        for key, value in mappings.items():
            self.extractions[key] = value(doc)
    
    @staticmethod
    def _extract_state(doc):
        for entity in doc.ents:
            if entity.label_ == 'GPE':
                state = us.states.lookup(entity.text)
                if state:
                    return state.abbr
    
    @staticmethod
    def _extract_city(doc):
        for entity in doc.ents:
            if entity.label_ == 'GPE' and us.states.lookup(entity.text) is None:
                return entity.lemma_.title()
    
    @staticmethod
    def _extract_zip_code(doc):
        return [token.text for token in doc if
                re.match('\d{5}', token.text) and list(token.children) == []]
    
    @staticmethod
    def _extract_address(doc):
        return [token.text for token in doc if token.ent_type_ == "FAC"]
    
    @staticmethod
    def _containsReferenceTo(doc, reference, MATCH_THRESHOLD=0.65):
        ref = NLP._nlp(reference)
        for token in doc:
            if token.similarity(ref) > MATCH_THRESHOLD:
                return True
        return False
    
    @staticmethod
    def _dog_friendly(doc):
        return NLP._containsReferenceTo(doc, reference="dog")
    
    @staticmethod
    def _cat_friendly(doc):
        return NLP._containsReferenceTo(doc, reference="cat")
    
    @staticmethod
    def _has_pool(doc):
        return NLP._containsReferenceTo(doc, reference="pool")
    
    @staticmethod
    def _has_elevator(doc):
        return NLP._containsReferenceTo(doc, reference="elevator")
    
    @staticmethod
    def _has_fitness_center(doc):
        return NLP._containsReferenceTo(doc, reference="fitness")
    
    @staticmethod
    def _has_wheelchair_access(doc):
        return NLP._containsReferenceTo(doc, reference="wheelchair") or NLP._containsReferenceTo(doc, reference='handicapped')
    
    @staticmethod
    def _has_dishwasher(doc):
        return NLP._containsReferenceTo(doc, reference="dishwasher")
    
    @staticmethod
    def _has_air_conditioning(doc):
        return NLP._containsReferenceTo(doc, reference="air conditioning")
    
    @staticmethod
    def _has_parking(doc):
        return NLP._containsReferenceTo(doc, reference="parking")
    
    @staticmethod
    def _furnished(doc):
        return NLP._containsReferenceTo(doc, reference="furnished", MATCH_THRESHOLD=0.75)
    
    @staticmethod
    def _has_laundry_facilities(doc):
        return NLP._containsReferenceTo(doc, reference="laundry")
