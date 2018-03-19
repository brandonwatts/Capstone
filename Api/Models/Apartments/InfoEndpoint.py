import json
import asyncio
import aiohttp


class InfoEndpoint:

    """ This class represents the "Info" Endpoint.

    This Endpoint is used to obtain the info for each individual apartment ID.

    """

    def __init__(self):
        self.url = "https://www.apartments.com/services/property/infoCardData"
        self.headers = {'Content-Type': 'application/json'}

    def call(self, keys, search_criteria):
        """ Calls the Endpoint designated by self.url

        keys -- List of valid API keys. ['y96k2tv', 'pd8cl9v', ...]
        search_criteria -- Search Criteria for a given API call. It is the same for all the keys.

        """

        futures = [self.call_for_key(key, search_criteria) for key in keys]
        loop = asyncio.get_event_loop()
        apartments = loop.run_until_complete(asyncio.gather(*futures))
        apartments = [json.loads(result) for result in apartments]
        return apartments

    async def call_for_key(self, key, search_criteria):
        """ Calls the Endpoint designated by self.urlf for each individual key.

        key -- Valid API key. ex. 'y96k2tv'
        search_criteria -- Search Criteria for a given API call. It is the same for all the keys.

        """

        call = {'ListingKeys': [str(key)], 'SearchCriteria': search_criteria}
        data = json.dumps(call)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data=data, headers=self.headers) as resp:
                return await resp.text()
