import requests
import pyEX as p


API_TOKEN = 'pk_c27c7a02dc4f4ebaa994b0a633d32908'

c = p.Client(api_token=API_TOKEN, version='stable')
try :
    print(c.options.optionExpirations('AMD'))
except Exception as e:
    print(e)    