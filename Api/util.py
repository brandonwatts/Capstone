import spacy

nlp = spacy.load('en')

def flatten(iterable):
    return [i for j in iterable for i in j]

class Phrase:
    def __init__(self, phrase):
        self.phrase = nlp(phrase)
    def is_match(self, token):
        if token.i + len(self.phrase) <= len(token.doc):
            return all(token.doc[token.i + i].lemma == self.phrase[i].lemma for i in range(len(self.phrase)))
    def extract(self, token):
        return token.doc[token.i:][:len(self.phrase)]
    def children(self, token):
        return flatten([other.children for other in self.extract(token)])
    def size(self, token):
        return len(self.phrase)

class Any:
    def __init__(self, *nodes):
        self.nodes = nodes
    def is_match(self, token):
        return any(node.is_match(token) for node in self.nodes)
    def extract(self, token):
        for node in self.nodes:
            if node.is_match(token):
                return node.extract(token)
    def children(self, token):
        for node in self.nodes:
            if node.is_match(token):
                return node.children(token)
    def size(self, token):
        for node in self.nodes:
            if node.is_match(token):
                return node.size(token)

class AnyPhrase(Any):
    def __init__(self, *phrases):
        array = [Phrase(phrase) for phrase in phrases]
        super().__init__(*array)

# TODO: Allow for grandchild/grandparent relations and etc.
class Branch:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
    def is_match(self, token):
        if self.parent.is_match(token):
            return any(self.child.is_match(i) for i in self.parent.children(token))
    def extract(self, token):
        for child in self.parent.children(token):
            if self.child.is_match(child):
                return [self.parent.extract(token), child]
    def children(self, token):
        return self.parent.children(token)
    def size(self, token):
        return self.parent.size(token)

class Sequence:
    def __init__(self, *nodes):
        self.nodes = nodes
    def is_match(self, token):
        for node in self.nodes:
            if node.is_match(token):
                token = token.doc[token.i + node.size(token)]
            else:
                return False
        return True
    def extract(self, token):
        extract = []
        for node in self.nodes:
            extract.append(node.extract(token))
            token = token.doc[token.i + node.size(token)]
        return extract
    def children(self, token):
        children = []
        for node in self.nodes:
            children += node.children(token)
            token = token.doc[token.i + node.size(token)]
        return children
    def size(self, token):
        size = 0
        for node in self.nodes:
            size += node.size(token)
            token = token.doc[token.i + node.size(token)]
        return size

class Number:
    def __init__(self):
        pass
    def is_match(self, token):
        return token.pos_ == "NUM"
    def extract(self, token):
        return token
    def children(self, token):
        return token.children
    def size(self, token):
        return 1

def search(node, doc):
    return list(map(node.extract, filter(node.is_match, doc)))

maximum_qualifier = AnyPhrase("less than", "under", "no more than", "at most")
maximum_number = Sequence(maximum_qualifier, Number())

result = search(maximum_number, nlp("List all houses with at most 4 bedrooms and that cost under 200,000."))
