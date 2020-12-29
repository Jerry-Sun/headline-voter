from pydantic import BaseModel

#receive the FE click event data from index.html 
class Vote(BaseModel): 
    headline: str
    direction: int

    class Config: 
        orm_mode = True