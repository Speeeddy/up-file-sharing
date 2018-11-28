import requests

URL_API = "https://up-karoon.ga/api/"
URL_WEB = "https://up-karoon.ga/"

r_api = requests.get(url = URL_API) 
r_web = requests.get(url = URL_WEB) 

assert r_api.status_code == 200
assert r_web.status_code == 200
