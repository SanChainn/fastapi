import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from databases import Database

# Get the DATABASE_URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Set up SQLAlchemy engine and session
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database connection for async queries
database = Database(DATABASE_URL)

# FastAPI app
app = FastAPI()

# Define a model for an Item in the database
class ItemModel(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    is_offer = Column(Boolean, default=False)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Serve static files (e.g., HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint for returning HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Endpoint to retrieve items from the database
@app.get("/items/")
async def get_items():
    query = select(ItemModel)
    async with database.transaction():
        result = await database.fetch_all(query)
        items = [dict(item) for item in result]
    return items

# Endpoint to add a new item to the database
@app.post("/items/")
async def create_item(name: str, price: int, is_offer: bool = False):
    query = ItemModel(name=name, price=price, is_offer=is_offer)
    
    async with database.transaction():
        await database.execute(ItemModel.__table__.insert(), query)
    
    return {"message": "Item created successfully"}

# API to send image data
@app.get("/image")
def get_image():
    return {"message": "Hello, FastAPI!", "image": "https://i.imgur.com/iIJBqUN.jpeg"}
