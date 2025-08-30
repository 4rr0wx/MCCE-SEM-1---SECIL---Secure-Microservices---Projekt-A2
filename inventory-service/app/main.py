from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
stock = {"widget": 10}

class ItemRequest(BaseModel):
    item_id: str
    quantity: int

@app.post("/reserve")
def reserve(req: ItemRequest):
    if stock.get(req.item_id, 0) < req.quantity:
        raise HTTPException(status_code=400, detail="insufficient stock")
    stock[req.item_id] -= req.quantity
    return {"status": "reserved"}

@app.post("/release")
def release(req: ItemRequest):
    stock[req.item_id] = stock.get(req.item_id, 0) + req.quantity
    return {"status": "released"}

@app.get("/stock/{item_id}")
def get_stock(item_id: str):
    return {"item_id": item_id, "quantity": stock.get(item_id, 0)}

