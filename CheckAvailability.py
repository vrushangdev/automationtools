# 1. Use SMSPVASERVICE TO Find Price Of All Countries
# 2. See Valid Numbers Availaible Below Our Max Budget
# 3. Create Account If Yes

from config import COUNTRY_LIST
import requests
import json

OUR_BUDGET = 0.3
response = requests.get(COUNTRY_LIST)
data = json.loads(response.text)
#print(data)
affordable_list = []
for d in data:
    country_code = d['code']
    BALANCE_URL = "http://smspva.com/priemnik.php?metod=get_service_price&country={}&service=opt4&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP".format(country_code)
    res = requests.post(BALANCE_URL)
    final_data = json.loads(res.text)
    if float(final_data['price']) < float(OUR_BUDGET):
        affordable_list.append(final_data)
try:
    handle = open('affordable_country.txt','w')
    handle.write(json.dumps(affordable_list))
    handle.close()
except Exception as e:
    print(e)



