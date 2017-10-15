import simplejson as json

def costar_api_mock(json_query):
    mock_json = json.loads('{ "Address" : "195 East Owlwood Road", "Country" : "United States of America", '
                           '"State" : "Virginia", "City" : "Richmond" }')

    return json.dumps(mock_json) + ' (What you actually sent: ' + json_query + ')'
