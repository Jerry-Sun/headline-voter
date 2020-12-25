from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pprint, json, requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Read the JSON data from the file into the program
with open("example2.json", "r") as f: 
   response = json.loads(f.read())


# Commenting this section out so it doesn't overwrite the monthly API pull limit
#url = "http://api.mediastack.com/v1/news"

#PARAMS = {
#    "access_key" : "ab0622cf5843c7ae44b724303b6ef796",
#    "categories": "business, technology, -entertainment",
#    "countries" : "us",
#    "sort" : "published_desc",
#    "limit" : 10,
#}

#r = requests.get(url, params = PARAMS)
#response = r.json()

#create the dictionary that will track headlines and their corresponding count
tracker_dict = {}

#receive the FE click event data from index.html 
class Vote(BaseModel): 
    headline: str
    direction: int

# Homepage when you visit the localhost site
@app.get("/")
async def homepage(request: Request):
    return {"message": "Welcome to this MediaStack project"}

# Webpage when you visit the "localhost/jinja" url
@app.get("/jinja")
async def get_headlines(request: Request):
#    print(response["data"])
#    print(response[1])
    return templates.TemplateResponse("index.html", {"request": request, "headlines": response["data"]})

# TODO: add titles to dictionary when button is clicked
# TODO: initialize as 1 or -1, then +1 or -1 depending on clicks
@app.post("/vote")
async def test(item: Vote):
    hashed_headline = hash(item.headline)
    if tracker_dict.__contains__(hashed_headline): 
        tracker_dict[hashed_headline] += item.direction
    else: 
        tracker_dict[hashed_headline] = item.direction
    print("Received message")
    # return "Response received"
   
