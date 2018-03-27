""" This module represents the "search" endpoint.

This endpoint is used to obtain the apartment ids and search criteria of a given JSON search query. The JSON search
query is built by the ApartmentsAPI class.

"""

import requests
import json

_headers = {"Content-Type": "application/json"}
_url = "https://www.apartments.com/services/search/"

def _extract_ids(pins_state):
    """ Helper method which extracts ids from the PinsState block
    
    pins_state -- String of pipe delimited items which include keys which take some form like "0~XXXXXX"
    
    """
    index = 0
    
    while index < len(pins_state):
        start = index
        while index < len(pins_state) and pins_state[index] != '|': index += 1
        yield pins_state[start:index]
        while index < len(pins_state) and pins_state[index] != '~': index += 1
        index += 1


def call(request):
    """ Calls the endpoint designated by _url
    
    request -- JSON that is returned by the .call() function of apartments
    
    """
    
    response = requests.post(_url, data=request, headers=_headers)
    response = json.loads(response.text)
    search_criteria = response.get("SearchCriteria")
    pins_state_ids = response.get("PinsState").get('cl')
    apartment_ids = _extract_ids(pins_state_ids)
    return apartment_ids, search_criteria
