from fastapi import FastAPI
from enum import Enum

class available_drinks(str,Enum):
    chai = "chai"
    herbal_tea = "herbal tea"
    cocktails = "cocktails"
    
app = FastAPI()

drinks = {"chai":"tasty",
          "herbal tea":"yuck",
          "cocktails":"tgif"}

@app.get("/")
async def root():
    return {"Message":"Hello World!!!!"}


@app.get("/hello/{name}")
async def get_name(name):
    return {"Message": f"Hello {name}!!"}

@app.get("/drinks/{drink_name}")
async def get_drink_desc(drink_name: available_drinks):
    desc = drinks.get(drink_name)
    return f"{drink_name} is {desc}"
         