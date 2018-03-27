from spacy.matcher import Matcher

class FieldMatcher(Matcher):
    def __init__(self, vocab, extractions):
        super().__init__(vocab)
        
        def extract(index):
            def callback(matcher, doc, i, matches):
                match_id, a, b = matches[i]
                if index > 0:
                    extractions[doc.vocab.strings[match_id]] = doc[a + index]
                else:
                    extractions[doc.vocab.strings[match_id]] = doc[b + index]
            return callback
        
        self.add("star_rating", extract(0), [{"IS_DIGIT": True}, {"LEMMA": "star"}])
        self.add("build_year", extract(-1), [{'LOWER': 'built'}, {'LOWER': 'in'}, {'ENT_TYPE': 'DATE'}])
        
        self.add("max_sqft", extract(-2), *FieldMatcher._maximum_patterns([], [{"LOWER": "squarefoot"}]))
        self.add("min_sqft", extract(-2), *FieldMatcher._minimum_patterns([], [{"LOWER": "squarefoot"}]))
        
        self.add("max_price", extract(-2), *FieldMatcher._maximum_patterns([], [{"LEMMA": "dollar"}]))
        self.add("min_price", extract(-2), *FieldMatcher._minimum_patterns([], [{"LEMMA": "dollar"}]))
        self.add("max_price", extract(-1), *FieldMatcher._maximum_patterns([{"ORTH": "$"}], []))
        self.add("min_price", extract(-1), *FieldMatcher._minimum_patterns([{"ORTH": "$"}], []))
        
        self.add("max_bed", extract(-2), *FieldMatcher._maximum_patterns([], [{"LEMMA": "bedroom"}]))
        self.add("min_bed", extract(-2), *FieldMatcher._minimum_patterns([], [{"LEMMA": "bedroom"}]))
        self.add("max_bed", extract(-2), *FieldMatcher._maximum_patterns([], [{"LEMMA": "bed"}]))
        self.add("min_bed", extract(-2), *FieldMatcher._minimum_patterns([], [{"LEMMA": "bed"}]))
    
    @staticmethod
    def _minimum_patterns(prefix, postfix):
        headers = [
            [{"LOWER": "not"}, {"LOWER": "under"}],
            [{"LOWER": "not"}, {"LOWER": "below"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "over"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "above"}],
            [{"LOWER": "at"}, {"LOWER": "lest"}],
            [{"LOWER": "no", "OP": "!"}, {"LOWER": "greater"}, {"LOWER": "than"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "greater"}, {"LOWER": "than"}],
            [{"LOWER": "no"}, {"LOWER": "less"}, {"LOWER": "than"}],
            [{"LOWER": "not"}, {"LOWER": "less"}, {"LOWER": "than"}],
            [{"LOWER": "no", "OP": "!"}, {"LOWER": "more"}, {"LOWER": "than"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "more"}, {"LOWER": "than"}]
        ]
        
        return [header + prefix + [{"IS_DIGIT": True}] + postfix for header in headers]
    
    @staticmethod
    def _maximum_patterns(prefix, postfix):
        headers = [
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "under"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "below"}],
            [{"LOWER": "not"}, {"LOWER": "over"}],
            [{"LOWER": "not"}, {"LOWER": "above"}],
            [{"LOWER": "at"}, {"LOWER": "most"}],
            [{"LOWER": "no"}, {"LOWER": "greater"}, {"LOWER": "than"}],
            [{"LOWER": "not"}, {"LOWER": "greater"}, {"LOWER": "than"}],
            [{"LOWER": "no", "OP": "!"}, {"LOWER": "less"}, {"LOWER": "than"}],
            [{"LOWER": "not", "OP": "!"}, {"LOWER": "less"}, {"LOWER": "than"}],
            [{"LOWER": "no"}, {"LOWER": "more"}, {"LOWER": "than"}],
            [{"LOWER": "not"}, {"LOWER": "more"}, {"LOWER": "than"}]
        ]
        
        return [header + prefix + [{"IS_DIGIT": True}] + postfix for header in headers] 
