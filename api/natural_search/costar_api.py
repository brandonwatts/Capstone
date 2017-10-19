from CostarAPIMockSchema import CostarApiMockSchema
from CostarAPIMock import CostarAPIMock


def costar_api_mock():
    api_response = CostarAPIMock(address="123 St.", city="Richmond", state="Virginia", country="USA")
    schema = CostarApiMockSchema()
    return schema.dump(api_response).data
