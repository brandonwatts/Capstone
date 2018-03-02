import re
import spacy
from spacy.strings import StringStore
from spacy.matcher import Matcher
import us

nlp = spacy.load('en')
#nlp = spacy.load('en_core_web_lg')

us_states = StringStore().from_disk('Api/StringStore/States')
us_state_abbreviations = StringStore().from_disk('Api/StringStore/StateAbbreviations')

class NLP:
    def __init__(self):
        self.extractions = {}

    def _add_extraction(self, name, value):
        if value:
            self.extractions[name] = value
        
    def parse(self, request):
        self.extractions.clear()
        matcher = self._createMatcher()
        doc = nlp(request)
        matcher(doc)
        self._define_extraction_points(doc)
        return self.extractions

    def _createMatcher(self):
        matcher = Matcher(nlp.vocab)

        # used for defining patterns for the matcher
        IS_SQFT = nlp.vocab.add_flag(Utils.is_sqft)
        IS_MIN_QUANTITY = nlp.vocab.add_flag(Utils.is_min_quantity)
        IS_MAX_QUANTITY = nlp.vocab.add_flag(Utils.is_max_quantity)
        IS_BED = nlp.vocab.add_flag(Utils.is_bed)
        
        star_rating_pattern = [{'IS_DIGIT': True}, {'LEMMA': 'star'}]
        search_radius_pattern = [{'IS_DIGIT': True}, {'ENT_TYPE': 'QUANTITY'}]
        min_sqft_pattern = [{IS_MIN_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'LIKE_NUM': True}, {IS_SQFT: True}]
        max_sqft_pattern = [{IS_MAX_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'LIKE_NUM': True}, {IS_SQFT: True}]
        min_price_pattern = [{IS_MIN_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'ENT_TYPE': 'MONEY'}, {'LIKE_NUM': True}]
        max_price_pattern = [{IS_MAX_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'ENT_TYPE': 'MONEY'}, {'LIKE_NUM': True}]
        min_bed_pattern = [{IS_MIN_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'LIKE_NUM': True}, {IS_BED: True}]
        max_bed_pattern = [{IS_MAX_QUANTITY: True}, {'LOWER': 'than', 'OP': '?'}, {'LIKE_NUM': True}, {IS_BED: True}]
        build_year_pattern = [{'LOWER': 'built'}, {'LOWER': 'in'}, {'ENT_TYPE': 'DATE'}]

        matcher.add('StarRating', self.on_star_rating_match, star_rating_pattern)
        matcher.add('SearchRadius', self.on_search_radius_match, search_radius_pattern)
        matcher.add('MinSqft', self.on_min_sqft_match, min_sqft_pattern)
        matcher.add('MaxSqft', self.on_max_sqft_match, max_sqft_pattern)
        matcher.add('MinPrice', self.on_min_price_match, min_price_pattern)
        matcher.add('MaxPrice', self.on_max_price_match, max_price_pattern)
        matcher.add('MinBed', self.on_min_bed_match, min_bed_pattern)
        matcher.add('MaxBed', self.on_max_bed_match, max_bed_pattern)
        matcher.add('BuildYear', self.on_build_year_match, build_year_pattern)

        return matcher
    
    def on_search_radius_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        searchRadius = doc[start:end]
        self._add_extraction("search_radius", searchRadius)

    def on_build_year_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        build_year = doc[start:end]
        for token in build_year:
            if token.like_num:
                value = token
        self._add_extraction("build_year", token)
    
    def on_star_rating_match(self, matcher, doc, id, matches):
        star_ratings = []
        for match in matches:
            match_id, start, end = match
            starRating = doc[start:end]
            star_ratings.append(starRating.text)
        self._add_extraction("star_rating", star_ratings)

    def on_min_sqft_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        min_sqft = doc[start:end]
        for token in min_sqft:
            if token.like_num:
                value = token
        self._add_extraction("min_sqft", value)

    def on_max_sqft_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        max_sqft = doc[start:end]
        for token in max_sqft:
            if token.like_num:
                value = token
        self._add_extraction("max_sqft", max_sqft)

    def on_max_price_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        max_price = doc[start:end]
        for token in max_price:
            if token.like_num:
                value = token
        self._add_extraction("max_price", value)

    def on_min_price_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        min_price = doc[start:end]
        for token in min_price:
            if token.like_num:
                value = token

        self._add_extraction("min_price", value)

    def on_min_bed_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        min_bed = doc[start:end]
        self._add_extraction("min_bed", min_bed)

    def on_max_bed_match(self, matcher, doc, id, matches):
        match_id, start, end = matches[id]
        max_bed = doc[start:end]
        self._add_extraction("max_bed", max_bed)

    def _define_extraction_points(self, doc):
        self._add_extraction("state", self.extract_state(doc))
        self._add_extraction("city", self.extract_city(doc))
        self._add_extraction("zip_code", self.extract_zip_code(doc))
        #self._add_extraction("pricing_type", self.extract_pricing_type(doc))
        self._add_extraction("address", self.extract_address(doc))
        self._add_extraction("dog_friendly", self.extract_dog_friendly(doc))
        self._add_extraction("cat_friendly", self.extract_cat_friendly(doc))
        self._add_extraction("has_pool", self.extract_has_pool(doc))
        self._add_extraction("has_elevator", self.extract_has_elevator(doc))
        self._add_extraction("has_fitness_center", self.extract_has_fitness_center(doc))
        self._add_extraction("has_wheelchair_access", self.extract_has_wheelchair_access(doc))
        self._add_extraction("has_dishwasher", self.extract_has_dishwasher(doc))
        self._add_extraction("has_air_conditioning", self.extract_has_air_conditioning(doc))
        self._add_extraction("has_parking", self.extract_has_parking(doc))
        self._add_extraction("is_furnished", self.extract_is_furnished(doc))
        self._add_extraction("has_laundry_facilities", self.extract_has_laundry_facilities(doc))
        #self._add_extraction("property_type", self.extract_property_type(doc))

    # TODO: convert more of these extraction functions to the matcher format
    def extract_state(self, doc):
        for entity in doc.ents:
            if entity.label_ == 'GPE' and entity.lemma_.upper() in us_states:
                state = Utils.abbreviate(entity.lemma_)
                return state

    def extract_city(self, doc):
        for entity in doc.ents:
            if entity.label_ == 'GPE' and entity.lemma_.upper() not in us_states:
                return entity.lemma_.title()
    
    def extract_zip_code(self, doc):
        return [token.text for token in doc if
                re.match('\d{5}', token.text) and list(token.children) == []]
    
    """
    def extract_pricing_type(self, doc):
        types = []
        for token in doc:
            if Utils.is_price(token):
                result = self.Utils.find_pricing_type(token)
                if result:
                    types.append(result.text)
        return "IN REPAIR"
    """

    def extract_address(self, doc):
        return [token.text for token in doc if token.ent_type_ == "FAC"]
    
    def extract_dog_friendly(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="dog")
    
    def extract_cat_friendly(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="cat")
    
    def extract_has_pool(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="pool")
    
    def extract_has_elevator(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="elevator")
    
    def extract_has_fitness_center(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="fitness")
    
    def extract_has_wheelchair_access(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="wheelchair") or Utils.containsReferenceTo(doc=doc, reference='handicapped')
    
    def extract_has_dishwasher(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="dishwasher")
    
    def extract_has_air_conditioning(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="air conditioning")
    
    def extract_has_parking(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="parking")
    
    def extract_is_furnished(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="furniture")
    
    def extract_has_laundry_facilities(self, doc):
        return Utils.containsReferenceTo(doc=doc, reference="laundry")

    """
    def extract_property_type(self, doc):
        return "pt_industrial, pt_retail, pt_shopping_center, pt_multifamily, pt_specialty, pt_office, pt_health_care," \
               "pt_hospitality, pt_sports_and_entertainment, pt_land, pt_residential_income"
    """

class Utils:
    """
    Utils acts like a namespace for a number of helper functions.
    We've kept in NLP.py since it references nlp so often.
    """

    @staticmethod
    def containsReferenceTo(doc, reference, MATCH_THRESHOLD=0.6):
        containsReference = False
        ref = nlp(reference)
        for token in doc:
            if token.similarity(ref) > MATCH_THRESHOLD:
                containsReference = True
        return containsReference

    @staticmethod
    def is_noun(token):
        noun_tags = ('NN', 'NNS', 'NNP', 'NNPS')
        return token.tag_ in noun_tags

    @staticmethod
    def abbreviate(state):
        return us.states.lookup(state).abbr

    @staticmethod
    def find_pricing_type(token):
        for child in token.children:
            if child.text.upper() == "PER":
                for pricing in child.children:
                    return pricing
    
    @staticmethod
    def is_sqft(text):
        sq_fts = ['FEET', 'FOOT', 'SQUAREFEET', 'SQUAREFOOT', 'SQUARE', 'SQFT', 'SQ', 'FT']
        return text.upper() in sq_fts

    @staticmethod
    def is_max_quantity(text):
        max_quantites = ["LESS", "UNDER", "BELOW"]
        return text.upper() in max_quantites

    @staticmethod
    def is_min_quantity(text):
        min_quantites = ["MORE", "GREATER", "OVER"]
        return text.upper() in min_quantites

    @staticmethod
    def is_bed(text):
        bed_quatities = ['BED', 'ROOM', 'BEDROOM', 'PEOPLE']
        return text.upper() in bed_quatities
