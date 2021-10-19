import requests
import json



def ya_decode(url):
    response = requests.get(url)
    return response.status_code
