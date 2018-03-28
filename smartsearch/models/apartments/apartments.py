from smartsearch.models.apartments import info_endpoint
from smartsearch.models.apartments import search_endpoint
from smartsearch.models.apartments.apartments_schema import ApartmentsSchema

_schema = ApartmentsSchema()

def _mapattrs(attributes):
    """ Maps the result returned by nlp.py into the correct schema designated by CoStar """
    return {
        'Geography': {
            'Address': {
                'City': attributes.get('city'),
                'State': attributes.get('state')
            },
            'GeographyType': 2
        },
        'Listing': {
            'Ratings': 31,
            'MinRentAmount': attributes.get('min_price'),
            'MaxRentAmount': attributes.get('max_price'),
            'MinSqft': attributes.get('min_sqft'),
            'MaxSqft': attributes.get('max_sqft'),
            'Amenities': 0
        }
    }

def _get_data(dump):
    return dump.data if hasattr(dump, 'data') else dump

def call(attributes):
    """ Pulls data from the search endpoint and then the info endpoint """
    apartments_api = _get_data(_schema.dumps(_mapattrs(attributes)))
    apartment_ids, search_criteria = search_endpoint.call(apartments_api)
    return info_endpoint.call(apartment_ids, search_criteria)
