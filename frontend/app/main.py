from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI()
ORDER_URL = "http://order-service:8000"
INVENTORY_URL = "http://inventory-service:8000"

html = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Inventory &amp; Order Dashboard</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1d4ed8 45%, #38bdf8 100%);
      --surface: rgba(255, 255, 255, 0.88);
      --surface-muted: rgba(255, 255, 255, 0.65);
      --border: rgba(148, 163, 184, 0.35);
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #2563eb;
      --accent-dark: #1e3a8a;
      --danger: #ef4444;
      --success: #16a34a;
      font-family: "Segoe UI", "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: clamp(1.5rem, 3vw, 3rem);
      background: var(--bg-gradient);
      color: var(--text);
    }

    main {
      width: min(980px, 100%);
      background: var(--surface);
      border-radius: 24px;
      padding: clamp(2rem, 4vw, 3rem);
      box-shadow: 0 25px 60px rgba(15, 23, 42, 0.25);
      backdrop-filter: blur(12px);
    }

    header {
      text-align: center;
      margin-bottom: clamp(2rem, 4vw, 3rem);
    }

    h1 {
      margin: 0;
      font-size: clamp(2.2rem, 3vw, 2.8rem);
      letter-spacing: -0.02em;
    }

    p.lead {
      margin: 0.75rem auto 0;
      color: var(--text-muted);
      max-width: 60ch;
      font-size: 1.05rem;
    }

    .grid {
      display: grid;
      gap: clamp(1.5rem, 3vw, 2.5rem);
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }

    .card {
      background: var(--surface-muted);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 16px 32px rgba(15, 23, 42, 0.18);
    }

    .card h2 {
      margin: 0;
      font-size: 1.4rem;
    }

    label {
      display: block;
      font-weight: 600;
      margin-bottom: 0.4rem;
    }

    input,
    select,
    button {
      font: inherit;
      border-radius: 12px;
      border: 1px solid var(--border);
      padding: 0.65rem 0.85rem;
      width: 100%;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    input:focus,
    select:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25);
    }

    button {
      background: var(--accent);
      border: none;
      color: white;
      font-weight: 600;
      cursor: pointer;
      margin-top: 0.25rem;
      transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }

    button:hover {
      background: var(--accent-dark);
      transform: translateY(-1px);
      box-shadow: 0 10px 22px rgba(37, 99, 235, 0.35);
    }

    button:active {
      transform: translateY(0);
      box-shadow: none;
    }

    .status {
      border-radius: 14px;
      padding: 0.85rem 1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin: clamp(1.5rem, 3vw, 2.5rem) 0 0;
      border: 1px solid transparent;
    }

    .status::before {
      content: "";
      width: 0.75rem;
      height: 0.75rem;
      border-radius: 999px;
      background: currentColor;
      box-shadow: 0 0 0 4px rgba(15, 23, 42, 0.08);
    }

    .status.status-info {
      background: rgba(37, 99, 235, 0.12);
      color: var(--accent-dark);
      border-color: rgba(37, 99, 235, 0.4);
    }

    .status.status-success {
      background: rgba(34, 197, 94, 0.15);
      color: var(--success);
      border-color: rgba(34, 197, 94, 0.4);
    }

    .status.status-error {
      background: rgba(248, 113, 113, 0.18);
      color: var(--danger);
      border-color: rgba(248, 113, 113, 0.4);
    }

    .status.status-muted {
      background: rgba(148, 163, 184, 0.18);
      color: var(--text-muted);
      border-color: rgba(148, 163, 184, 0.35);
    }

    pre.output {
      background: rgba(15, 23, 42, 0.9);
      color: #e2e8f0;
      border-radius: 16px;
      padding: 1.25rem;
      font-family: "Fira Code", "SFMono-Regular", ui-monospace, "Segoe UI Mono", monospace;
      font-size: 0.95rem;
      overflow-x: auto;
      white-space: pre-wrap;
      border: 1px solid rgba(15, 23, 42, 0.4);
      margin-top: clamp(1.5rem, 3vw, 2.5rem);
    }

    @media (max-width: 600px) {
      main {
        padding: 1.75rem;
      }

      .card {
        padding: 1.25rem;
      }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Inventory Management &amp; Orders</h1>
      <p class="lead">Verwalte Lagerbestände und erstelle Bestellungen in einer aufgeräumten Oberfläche. Alle Aktionen werden sofort mit den Microservices synchronisiert.</p>
    </header>

    <section class="grid">
      <form id="inv" class="card">
        <h2>Bestand aktualisieren</h2>
        <div>
          <label for="inv-item-id">Artikelnummer</label>
          <input id="inv-item-id" name="item_id" placeholder="z. B. SKU-123" required>
        </div>
        <div>
          <label for="inv-quantity">Menge</label>
          <input id="inv-quantity" name="quantity" type="number" min="0" step="1" placeholder="z. B. 25" required>
        </div>
        <button type="submit">Bestand speichern</button>
      </form>

      <form id="order" class="card">
        <h2>Neue Bestellung</h2>
        <div>
          <label for="items">Artikel auswählen</label>
          <select name="item_id" id="items" required>
            <option value="" disabled selected>Inventar wird geladen …</option>
          </select>
        </div>
        <div>
          <label for="order-quantity">Menge</label>
          <input id="order-quantity" name="quantity" type="number" min="1" value="1" required>
        </div>
        <div>
          <label for="order-amount">Betrag (€)</label>
          <input id="order-amount" name="amount" type="number" min="0" step="0.01" value="9.99" required>
        </div>
        <button type="submit">Bestellung absenden</button>
      </form>
    </section>

    <div id="status" class="status status-muted">Bereit.</div>
    <pre id="out" class="output">Noch keine Aktionen durchgeführt.</pre>
  </main>
  <script>
    const statusEl = document.getElementById('status');
    const outputEl = document.getElementById('out');

    function setStatus(message, tone = 'info') {
      statusEl.textContent = message;
      statusEl.className = `status status-${tone}`;
    }

    function renderOutput(payload) {
      if (payload === undefined || payload === null) {
        outputEl.textContent = 'Keine Daten verfügbar.';
        return;
      }
      if (typeof payload === 'string') {
        try {
          const parsed = JSON.parse(payload);
          outputEl.textContent = JSON.stringify(parsed, null, 2);
          return;
        } catch (err) {
          outputEl.textContent = payload;
          return;
        }
      }
      outputEl.textContent = JSON.stringify(payload, null, 2);
    }

    async function loadItems(showFeedback = false) {
      try {
        const res = await fetch('/api/items');
        if (!res.ok) {
          throw new Error(`Serverantwort ${res.status}`);
        }
        const items = await res.json();
        const sel = document.getElementById('items');
        sel.innerHTML = '';
        if (items.length === 0) {
          const opt = document.createElement('option');
          opt.textContent = 'Keine Artikel im Lager verfügbar';
          opt.disabled = true;
          opt.selected = true;
          sel.appendChild(opt);
        } else {
          for (const i of items) {
            const opt = document.createElement('option');
            opt.value = i.item_id;
            opt.textContent = `${i.item_id} — ${i.quantity} Stück verfügbar`;
            sel.appendChild(opt);
          }
        }
        if (showFeedback) {
          setStatus('Inventar erfolgreich aktualisiert.', 'success');
        } else {
          setStatus('Inventar geladen.', 'muted');
        }
        return items;
      } catch (error) {
        setStatus('Fehler beim Laden des Inventars. Bitte später erneut versuchen.', 'error');
        console.error(error);
      }
    }

    document.getElementById('inv').addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = Object.fromEntries(new FormData(event.target));
      formData.quantity = Number(formData.quantity);
      setStatus('Bestand wird gespeichert …', 'info');
      try {
        const res = await fetch('/api/stock', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });
        const text = await res.text();
        renderOutput(text);
        if (!res.ok) {
          throw new Error(text);
        }
        await loadItems(true);
      } catch (error) {
        setStatus('Bestand konnte nicht gespeichert werden.', 'error');
        console.error(error);
      }
    });

    document.getElementById('order').addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = Object.fromEntries(new FormData(event.target));
      formData.quantity = Number(formData.quantity);
      formData.amount = Number(formData.amount);
      setStatus('Bestellung wird gesendet …', 'info');
      try {
        const res = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });
        const text = await res.text();
        renderOutput(text);
        if (!res.ok) {
          throw new Error(text);
        }
        setStatus('Bestellung erfolgreich erstellt.', 'success');
      } catch (error) {
        setStatus('Bestellung konnte nicht erstellt werden.', 'error');
        console.error(error);
      }
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
