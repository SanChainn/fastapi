import os
import uvicorn
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
    print("hello, FastAPI!")
    return {"message": "Hello, FastAPI!"}

# Root Endpoint
@app.get("/image")
def read_root():
    print("hello, FastAPI!")
    return {"message": "Hello, FastAPI!", "image": "https://i.imgur.com/iIJBqUN.jpeg"}

# Path Parameter Example
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Post Request Example
@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}

# Ensure it runs with the correct port on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
