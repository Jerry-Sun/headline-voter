from typing import Optional
from fastapi import FastAPI
import pprint, json, requests

app = FastAPI()
with open("example2.json", "r") as f: 
    data = f.read()


@app.get("/")
async def get_headlines():
    return {data}