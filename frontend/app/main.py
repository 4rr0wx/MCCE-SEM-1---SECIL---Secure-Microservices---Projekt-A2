from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI()
ORDER_URL = "http://order-service:8000"

html = """
<!DOCTYPE html>
<html>
<head>
  <title>Order demo</title>
</head>
<body>
<h1>Create Order</h1>
<form id="f">
Item ID: <input name="item_id" value="widget"><br>
Quantity: <input name="quantity" type="number" value="1"><br>
Amount: <input name="amount" type="number" value="9.99" step="0.01"><br>
<button type="submit">Send</button>
</form>
<pre id="out"></pre>
<script>
document.getElementById('f').addEventListener('submit', async e => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  data.quantity = Number(data.quantity);
  data.amount = Number(data.amount);
  const res = await fetch('/api/orders', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  document.getElementById('out').textContent = await res.text();
});
</script>
</body>
</html>
"""

class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    amount: float

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(html)

@app.post("/api/orders")
def api_order(order: OrderRequest):
    resp = requests.post(f"{ORDER_URL}/orders", json=order.dict(), timeout=5)
    return resp.json()

