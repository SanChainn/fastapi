from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request Body Model
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Path Parameter Example
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Post Request Example
@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}

# Run the server with:
# uvicorn filename:app --reload
