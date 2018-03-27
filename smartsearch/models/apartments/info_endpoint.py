""" This module represents the "info" endpoint.

This endpoint is used to obtain the info for each individual apartment ID.

"""

import json
import asyncio
import aiohttp

_url = "https://www.apartments.com/services/property/infoCardData"
_headers = {"Content-Type": "application/json"}

async def _call_for_key(key, search_criteria):
    """ Calls the endpoint designated by self.urlf for an individual key.
    
    key -- Valid API key. ex. "y96k2tv"
    search_criteria -- Search Criteria for a given API call. It is the same for all the keys.
    
    """
    
    call = {"ListingKeys": [str(key)], "SearchCriteria": search_criteria}
    data = json.dumps(call)
    async with aiohttp.ClientSession() as session:
        async with session.post(_url, data=data, headers=_headers) as resp:
            return await resp.text()

def call(keys, search_criteria):
    """ Calls the endpoint designated by self.url
    
    keys -- List of valid API keys. ["y96k2tv", "pd8cl9v", ...]
    search_criteria -- Search Criteria for a given API call. It is the same for all the keys.
    
    """

    futures = [_call_for_key(key, search_criteria) for key in keys]
    loop = asyncio.get_event_loop()
    apartments = loop.run_until_complete(asyncio.gather(*futures))
    apartments = [json.loads(result) for result in apartments]
    return apartments
