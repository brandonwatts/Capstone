class Geography(object):
    def __init__(self, geotype, city, state):
        self.GeographyType = geotype
        self.Address = Address(city, state)

class Listings(object):
    def __init__(self, ratings):
        self.Ratings = ratings

class Address(object):
    def __init__(self, city, state):
        self.City = city
        self.State = state
