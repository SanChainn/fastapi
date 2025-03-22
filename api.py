import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Request Body Model
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# Serve static files (e.g., HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint for returning HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# API to send image data
@app.get("/image")
def get_image():
    return {"message": "Hello, FastAPI!", "image": "https://i.imgur.com/iIJBqUN.jpeg"}

