from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pprint, json, requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Read the JSON data from the file into the program
with open("example2.json", "r") as f: 
    data = json.loads(f.read())

# Homepage when you visit the localhost site
@app.get("/")
async def homepage(request: Request):
    return {"message": "Welcome to this MediaStack project"}

# Webpage when you visit the "localhost/jinja" url
@app.get("/jinja")
async def get_headlines(request: Request):
#    print(data["data"])
#    print(data[1])
    return templates.TemplateResponse("index.html", {"request": request, "headlines": data["data"]})
   
