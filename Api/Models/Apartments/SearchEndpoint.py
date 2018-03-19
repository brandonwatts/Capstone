import requests
import json
import re


class SearchEndpoint:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.url = "https://www.apartments.com/services/search/"
        self.pattern = re.compile("(^[a-z0-9]*(?=|))|((?<=[0-9]~)[a-z0-9]*(?=|))")

    def extract_ids(self, pins_state):
        ids = re.findall(self.pattern, pins_state)
        ids_list = [ids[0][0]] + [id[1] for id in ids[1:]]
        return ids_list

    def call(self, request):

        response = requests.post(self.url, data=request, headers=self.headers)
        search_criteria = json.loads(response.text).get("SearchCriteria")
        pins_state = json.loads(response.text).get("PinsState").get('cl')
        apartment_ids = self.extract_ids(pins_state)
        return apartment_ids, search_criteria
