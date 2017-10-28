from CostarAPIMockSchema import CostarApiMockSchema
from CostarAPIMock import CostarAPIMock


def costar_api_mock():
    api_response = CostarAPIMock(address="123 St.", city="Richmond", state="Virginia", country="USA")
    schema = CostarApiMockSchema()
    return schema.dump(api_response).data	

'''
- The following text below is based on a query on loopnet for all properties in Williamsburg, VA

- Request URL:
https://api.demandbase.com/api/v2/ip.json?referrer=http%3A%2F%2Fwww.loopnet.com%2F&page=http%3A%2F%2Fwww.loopnet.com%2Ffor-sale%2Fwilliamsburg-va%2F%3Fe%3Du&page_title=Williamsburg%2C%20VA%20Commercial%20Real%20Estate%20For%20Sale%20-%20LoopNet&key=f65d71050e8b992b31cf9cd95ec995c8&impid=4de8c1ef-2294-4ff2-895f-c97088b5e84c

- Request Headers:
GET /api/v2/ip.json?referrer=http%3A%2F%2Fwww.loopnet.com%2F&page=http%3A%2F%2Fwww.loopnet.com%2Ffor-sale%2Fwilliamsburg-va%2F%3Fe%3Du&page_title=Williamsburg%2C%20VA%20Commercial%20Real%20Estate%20For%20Sale%20-%20LoopNet&key=f65d71050e8b992b31cf9cd95ec995c8&impid=4de8c1ef-2294-4ff2-895f-c97088b5e84c HTTP/1.1
Host: api.demandbase.com
Connection: keep-alive
Origin: http://www.loopnet.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36
Accept: */*
Referer: http://www.loopnet.com/for-sale/williamsburg-va/?e=u
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9

- Request Headers Parsed:
Accept:*/*
Accept-Encoding:gzip, deflate, br
Accept-Language:en-US,en;q=0.9
Connection:keep-alive
Host:api.demandbase.com
Origin:http://www.loopnet.com
Referer:http://www.loopnet.com/for-sale/williamsburg-va/?e=u
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36

- Query String:
referrer=http%3A%2F%2Fwww.loopnet.com%2F&page=http%3A%2F%2Fwww.loopnet.com%2Ffor-sale%2Fwilliamsburg-va%2F%3Fe%3Du&page_title=Williamsburg%2C%20VA%20Commercial%20Real%20Estate%20For%20Sale%20-%20LoopNet&key=f65d71050e8b992b31cf9cd95ec995c8&impid=4de8c1ef-2294-4ff2-895f-c97088b5e84c

- Query String Parsed:
referrer:http://www.loopnet.com/
page:http://www.loopnet.com/for-sale/williamsburg-va/?e=u
page_title:Williamsburg, VA Commercial Real Estate For Sale - LoopNet
key:f65d71050e8b992b31cf9cd95ec995c8
impid:4de8c1ef-2294-4ff2-895f-c97088b5e84c

- I think this JSON Jonathan showed us below under the XHR section only has to do where the client is located, nothing to do with the actual query 

{registry_company_name: "Level 3 Communications", registry_city: "Richmond", registry_state: "VA",…}
access_type : "corporate"
annual_sales : 5500000
audience : "SMB"
audience_segment : "Telecommunications"
b2b : true
b2c : true
city : "San Bernardino"
company_name : "Amtec Communications Inc"
country : "US"
country_name : "United States"
demandbase_sid : 28375400
employee_count : 17
employee_range : "Small"
forbes_2000 : false
fortune_1000 : false
industry : "Telecommunications"
information_level : "Detailed"
ip : "8.30.81.2"
isp : false
latitude : 34.0686
longitude : -117.286
marketing_alias : "Amtec Communications"
phone : "909-884-9497"
primary_naics : "517919"
primary_sic : "4899"
region_name : "Virginia"
registry_area_code : 804
registry_city : "Richmond"
registry_company_name : "Level 3 Communications"
registry_country : "United States"
registry_country_code : "US"
registry_country_code3 : "USA"
registry_dma_code : 556
registry_latitude : 37.55220031738281
registry_longitude : -77.45819854736328
registry_state : "VA"
registry_zip_code : "23220"
revenue_range : "$5M - $10M"
state : "CA"
stock_ticker : null
street_address : "1894 Commercenter W Ste 201"
sub_industry : "Equipment & Services"
traffic : "Low"
web_site : "amteccommunications.com"
zip : "92408"
'''
