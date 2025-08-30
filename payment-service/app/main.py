from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
payments = {}

class PaymentRequest(BaseModel):
    order_id: str
    amount: float

@app.post("/charge")
def charge(req: PaymentRequest):
    payments[req.order_id] = req.amount
    return {"status": "charged"}

@app.post("/refund")
def refund(req: PaymentRequest):
    if payments.get(req.order_id) == req.amount:
        payments.pop(req.order_id, None)
    return {"status": "refunded"}

