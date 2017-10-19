
__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

class CostarAPIMock(object):
    def __init__(self, address, country, state, city):
        self.address = address
        self.country = country
        self.state = state
        self.city = city