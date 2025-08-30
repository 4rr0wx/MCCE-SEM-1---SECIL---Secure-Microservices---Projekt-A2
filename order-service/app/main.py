from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()
INVENTORY_URL = "http://inventory-service:8000"
PAYMENT_URL = "http://payment-service:8000"
orders = {}

class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    amount: float

@app.post("/orders")
def create_order(order: OrderRequest):
    order_id = str(len(orders) + 1)
    try:
        res = requests.post(f"{INVENTORY_URL}/reserve", json=order.dict(), timeout=5)
        res.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="inventory unavailable")

    try:
        res = requests.post(
            f"{PAYMENT_URL}/charge",
            json={"order_id": order_id, "amount": order.amount},
            timeout=5,
        )
        res.raise_for_status()
    except requests.RequestException:
        try:
            requests.post(f"{INVENTORY_URL}/release", json=order.dict(), timeout=5)
        except requests.RequestException as e:
            # Log the failure to release inventory for operational visibility
            print(f"Failed to release inventory for order compensation: {e}")
        raise HTTPException(status_code=503, detail="payment unavailable")

    orders[order_id] = order.dict()
    return {"order_id": order_id, "status": "confirmed"}

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    try:
        refund_res = requests.post(
            f"{PAYMENT_URL}/refund", json={"order_id": order_id, "amount": order['amount']}, timeout=5
        )
        refund_res.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="refund unavailable")

    try:
        release_res = requests.post(f"{INVENTORY_URL}/release", json=order, timeout=5)
        release_res.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="inventory release unavailable")
    orders.pop(order_id)
    return {"status": "cancelled"}

