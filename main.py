from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pprint, json, requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("example2.json", "r") as f: 
    data = f.read()

#@app.get("/")
#async def homepage(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/jinja")
async def get_headlines(request: Request):
#    print(data["data"])
#    print(data[1])
    return templates.TemplateResponse("index.html", {"request": request, "headlines": data})
   
