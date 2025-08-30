from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI()
ORDER_URL = "http://order-service:8000"
INVENTORY_URL = "http://inventory-service:8000"

html = """
<!DOCTYPE html>
<html>
<head>
  <title>Order demo</title>
</head>
<body>
<h1>Inventory Management</h1>
<form id="inv">
Item ID: <input name="item_id"><br>
Quantity: <input name="quantity" type="number"><br>
<button type="submit">Update</button>
</form>

<h1>Create Order</h1>
<form id="order">
Item: <select name="item_id" id="items"></select><br>
Quantity: <input name="quantity" type="number" value="1"><br>
Amount: <input name="amount" type="number" value="9.99" step="0.01"><br>
<button type="submit">Send</button>
</form>
<pre id="out"></pre>
<script>
async function loadItems(){
  const res = await fetch('/api/items');
  const items = await res.json();
  const sel = document.getElementById('items');
  sel.innerHTML = '';
  for(const i of items){
    const opt = document.createElement('option');
    opt.value = i.item_id;
    opt.textContent = `${i.item_id} (${i.quantity})`;
    sel.appendChild(opt);
  }
}
document.getElementById('inv').addEventListener('submit', async e => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  data.quantity = Number(data.quantity);
  await fetch('/api/stock', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  await loadItems();
});
document.getElementById('order').addEventListener('submit', async e => {
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
loadItems();
</script>
</body>
</html>
"""

class OrderRequest(BaseModel):
    item_id: str
    quantity: int
    amount: float

class StockItem(BaseModel):
    item_id: str
    quantity: int

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(html)

@app.get("/api/items")
def api_items():
    resp = requests.get(f"{INVENTORY_URL}/items", timeout=5)
    return resp.json()

@app.post("/api/stock")
def api_stock(item: StockItem):
    resp = requests.post(f"{INVENTORY_URL}/stock", json=item.dict(), timeout=5)
    return resp.json()

@app.post("/api/orders")
def api_order(order: OrderRequest):
    resp = requests.post(f"{ORDER_URL}/orders", json=order.dict(), timeout=5)
    return resp.json()
