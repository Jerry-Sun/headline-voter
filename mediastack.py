import pprint, json, requests

url = "http://api.mediastack.com/v1/news"

PARAMS = {
    "access_key" : "ab0622cf5843c7ae44b724303b6ef796",
    "categories": "business, technology, -entertainment",
    "countries" : "us",
    "languages" : "en",
    "sort" : "published_desc",
    "limit" : 10,
}

r = requests.get(url, params = PARAMS)
data = r.json()
pprint.pprint(data)
