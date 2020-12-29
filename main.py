from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schema import Vote
from ratelimit import limits
import pprint, json, requests, database, models, schema, hashlib

app = FastAPI()
templates = Jinja2Templates(directory="templates")

database.Base.metadata.create_all(bind=engine)

# Read the JSON data from the file into the program
# with open("example2.json", "r") as f: 
#    response = json.loads(f.read())

# Commenting this section out so it doesn't overwrite the monthly API pull limit
url = "http://api.mediastack.com/v1/news"

PARAMS = {
   "access_key" : "ab0622cf5843c7ae44b724303b6ef796",
   "categories": "business, technology, -entertainment",
   "countries" : "us",
   "sort" : "published_desc",
   "limit" : 10,
}

r = requests.get(url, params = PARAMS)
response = r.json()

# dependency
def get_db(): 
    try: 
        db = SessionLocal()
        yield db
    finally: 
        db.close()

# Homepage when you visit the localhost site
@app.get("/")
async def get_headlines(request: Request, db: Session = Depends(get_db)):
    for headline in response["data"]: 
        hashed_headline = int(hashlib.sha256((headline['title']).encode("utf-8")).hexdigest(), 16) % 10**8
        temp = db.query(models.HeadlineScore).filter_by(headline=hashed_headline).one_or_none()
        if temp is None: 
            headline["score"] = 0
        else: 
            headline["score"] = temp.score
    return templates.TemplateResponse("index.html", {"request": request, "headlines": response["data"]})

@app.post("/vote")
def vote(item: Vote, db: Session = Depends(get_db)):
    hashed_headline = int(hashlib.sha256(item.headline.encode("utf-8")).hexdigest(), 16) % 10**8
    #print(hashed_headline_int)
    #print(type(hashed_headline_int))
    temp = db.query(models.HeadlineScore).filter_by(headline=hashed_headline).one_or_none()
    if temp is None: 
        db_headlinescore = models.HeadlineScore(headline=hashed_headline, score=item.direction)
        db.add(db_headlinescore)
        db.commit()
        db.refresh(db_headlinescore)
        return db_headlinescore
    else:
        temp.score += item.direction
        db.commit()
        db.refresh(temp)
        return temp
   
