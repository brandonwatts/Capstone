import requests
import json


class SearchEndpoint:

    """ This class represents the "Search" Endpoint.

    This Endpoint is used to obtain the apartment ids and search criteria of a given JSON search query. The JSON search
    query is built by the ApartmentsAPI class.
    """

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.url = "https://www.apartments.com/services/search/"

    def _extract_ids(self, pins_state):

        """ Helper method which extracts ids from the PinsState block

        pins_state -- String of pipe delimited items which include keys which take some form like "0~XXXXXX"

        """

        pins_state_list = pins_state.split("|")

        ''' Filter everything that starts with "0~" and then chop off those characters as they are not 
            actually part of the key.
        '''
        apartment_ids = [x[2:] for x in pins_state_list if x.startswith("0~")]
        return apartment_ids

    def call(self, request):

        """ Calls the Endpoint designated by self.url

        request -- JSON that is returned by the .call() method of ApartmentsAPI

        """

        response = requests.post(self.url, data=request, headers=self.headers)
        response = json.loads(response.text)
        search_criteria = response.get("SearchCriteria")
        pins_state_ids = response.get("PinsState").get('cl')
        apartment_ids = self._extract_ids(pins_state_ids)
        return apartment_ids, search_criteria
