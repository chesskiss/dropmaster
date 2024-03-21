import requests
import pandas as pd

# set up the request parameters
params = {
  'api_key': '53DEAF5E341F4B3DA30B1250B77BE99C',
  'amazon_domain': 'amazon.com',
  'asin': 'B07FDHK5NW',
  'type': 'product',
  'output': 'json'
}

# make the http GET request to Rainforest API
api_result = requests.get('https://api.rainforestapi.com/request', params)
#####################################################################################
# My code begins
###########################
json = api_result.json()
#df = pd.read_csv(api_result.content)
df = pd.read_json(api_result)
print(df.head(1))

from io import BytesIO
print(api_result.json())
print(dj)
'''
import json
parsed = json.loads(api_result.content)
print(len(parsed))
'''

#with open('amazon_product.csv', 'w') as file:
#     file.write(api_result.content.rating)
#    file.close()
