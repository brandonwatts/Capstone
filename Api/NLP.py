import re
import spacy
from spacy.strings import StringStore
from spacy.matcher import Matcher
import us

nlp = spacy.load('en_core_web_lg')
us_states = StringStore().from_disk('Api/StringStore/States')
us_state_abbreviations = StringStore().from_disk('Api/StringStore/StateAbbreviations')


class NLP:
    
    def __init__(self):
        self.extractions = {}
        
    def _addExtraction(self, name, value):
        self.extractions[name] = value
        
    def parse(self, request):
        matcher = Matcher(nlp.vocab)
        star_rating_pattern = [{'IS_DIGIT': True}, {'LEMMA': 'star'}]
        search_radius_pattern = [{'IS_DIGIT': True}, {'ENT_TYPE': 'QUANTITY'}]
        matcher.add('StarRating', self.on_star_rating_match, star_rating_pattern)
        matcher.add('SearchRadius', self.on_search_radius_match, search_radius_pattern)
        doc = nlp(request)
        matcher(doc)
        self.define_extraction_points(doc)
        return self.extractions
    
    def on_search_radius_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        searchRadius = doc[start:end]
        self._addExtraction("search_radius", searchRadius)
    
    def on_star_rating_match(self, matcher, doc, id, matches):
        star_ratings = []
        for match in matches:
            match_id, start, end = match
            starRating = doc[start:end]
            star_ratings.append(starRating.text)
        self._addExtraction("star_rating", star_ratings)
    
    def define_extraction_points(self, doc):
        self._addExtraction("state", self.extract_state(doc))
        self._addExtraction("city", self.extract_city(doc))
        self._addExtraction("zip_code", self.extract_zip_code(doc))
        self._addExtraction("min_sqft", self.extract_min_sqft(doc))
        self._addExtraction("max_sqft", self.extract_max_sqft(doc))
        self._addExtraction("min_price", self.extract_min_price(doc))
        self._addExtraction("max_price", self.extract_max_price(doc))
        self._addExtraction("min_bed", self.extract_min_bed(doc))
        self._addExtraction("max_bed", self.extract_max_bed(doc))
        self._addExtraction("pricing_type", self.extract_pricing_type(doc))
        self._addExtraction("address", self.extract_address(doc))
        self._addExtraction("build_year", self.extract_build_year(doc))
        self._addExtraction("dog_friendly", self.extract_dog_friendly(doc))
        self._addExtraction("cat_friendly", self.extract_cat_friendly(doc))
        self._addExtraction("has_pool", self.extract_has_pool(doc))
        self._addExtraction("has_elevator", self.extract_has_elevator(doc))
        self._addExtraction("has_fitness_center", self.extract_has_fitness_center(doc))
        self._addExtraction("has_wheelchair_access", self.extract_has_wheelchair_access(doc))
        self._addExtraction("has_dishwasher", self.extract_has_dishwasher(doc))
        self._addExtraction("has_air_conditioning", self.extract_has_air_conditioning(doc))
        self._addExtraction("has_parking", self.extract_has_parking(doc))
        self._addExtraction("is_furnished", self.extract_is_furnished(doc))
        self._addExtraction("has_laundry_facilities", self.extract_has_laundry_facilities(doc))
        self._addExtraction("property_type", self.extract_property_type(doc))
    
    def extract_state(self, doc):
        for entity in doc.ents:
            if entity.label_ == 'GPE' and entity.lemma_.upper() in us_states:
                state = self.Utils.abbreviate(entity.lemma_)
        return state

    def extract_city(self, doc):
        return "Richmond"
        #return [ent.lemma_.upper() for ent in doc.ents if ent.label_ == 'GPE' and ent.text.upper() not in us_states]
    
    def extract_zip_code(self, doc):
        return [token.text for token in doc if
                re.match('\d{5}', token.text) and list(token.children) == []]
    
    def is_sqft(self, token):
        tags = ('FEET', 'FOOT', 'SQUAREFEET', 'SQUAREFOOT',
                'SQUARE', 'SQFT', 'SQ', 'FT')
        return token.pos_ == "NUM" and token.head.lemma_.upper() in tags
    
    def extract_min_sqft(self, doc):
        return [token.text for token in doc
                if self.is_sqft(token) and not self.Utils.is_max_quantity(token)]
    
    def extract_max_sqft(self, doc):
        return [token.text for token in doc
                if self.is_sqft(token) and self.Utils.is_max_quantity(token)]

    
    def extract_min_price(self, doc):
        return [token.text
                for token in doc if self.Utils.is_price(token) and not self.Utils.is_max_quantity(token)]
    
    def extract_max_price(self, doc):
        return [token.text
                for token in doc if self.Utils.is_price(token) and self.Utils.is_max_quantity(token)]
    
    def find_pricing_type(self, token):
        for child in token.children:
            if child.text.upper() == "PER":
                for pricing in child.children:
                    return pricing
    
    def extract_pricing_type(self, doc):
        types = []
        for token in doc:
            if self.Utils.is_price(token):
                result = self.find_pricing_type(token)
                if result:
                    types.append(result.text)
        return types
    
    def is_bed(self, token):
        tags = ('BED', 'ROOM', 'BEDROOM', 'PEOPLE')
        return token.pos_ == "NUM" and token.head.lemma_.upper() in tags
    
    def extract_min_bed(self, doc):
        return [token.text for token in doc
                if self.is_bed(token) and not self.Utils.is_max_quantity(token)]
    
    def extract_max_bed(self, doc):
        return [token.text for token in doc
                if self.is_bed(token) and self.Utils.is_max_quantity(token)]
    
    def extract_address(self, doc):
        return [token.text for token in doc if token.ent_type_ == "FAC"]
    
    def extract_build_year(self, doc):
        # TODO Min & Max Year
        return [token.text for token in doc if token.ent_type_ == "DATE"]
    
    def extract_dog_friendly(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="dog")
    
    def extract_cat_friendly(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="cat")
    
    def extract_has_pool(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="pool")
    
    def extract_has_elevator(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="elevator")
    
    def extract_has_fitness_center(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="fitness")
    
    def extract_has_wheelchair_access(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="wheelchair") or self.Utils.containsReferenceTo(doc=doc, reference='handicapped')
    
    def extract_has_dishwasher(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="dishwasher")
    
    def extract_has_air_conditioning(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="air conditioning")
    
    def extract_has_parking(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="parking")
    
    def extract_is_furnished(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="furniture")
    
    def extract_has_laundry_facilities(self, doc):
        return self.Utils.containsReferenceTo(doc=doc, reference="laundry")
    
    def extract_property_type(self, doc):
        return "pt_industrial, pt_retail, pt_shopping_center, pt_multifamily, pt_specialty, pt_office, pt_health_care," \
               "pt_hospitality, pt_sports_and_entertainment, pt_land, pt_residential_income"

    class Utils:

        @staticmethod
        def containsReferenceTo(doc, reference, MATCH_THRESHOLD=0.6):
            containsReference = False
            ref = nlp(reference)
            for token in doc:
                if token.similarity(ref) > MATCH_THRESHOLD:
                    containsReference = True
            return containsReference

        @staticmethod
        def is_price(token):
            return token.ent_type_ == "MONEY" and token.pos_ == "NUM"

        @staticmethod
        def find_head(token, function):
            while token != token.head:
                if function(token):
                    return token
                token = token.head

        @staticmethod
        def is_noun(token):
            noun_tags = ('NN', 'NNS', 'NNP', 'NNPS')
            return token.tag_ in noun_tags

        @ staticmethod
        def is_min_quantity(token):
            min_tags = ("MORE", "GREATER", "OVER")
            return any(child.text.upper() in min_tags for child in token.children)

        @staticmethod
        def is_max_quantity(token):
            max_tags = ("LESS", "UNDER", "BELOW")
            return any(child.text.upper() in max_tags for child in token.children)

        @staticmethod
        def abbreviate(state):
            print("abb", us.states.lookup(state).abbr)
            return us.states.lookup(state).abbr
