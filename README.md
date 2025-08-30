# Secure Microservices Prototype

Dieses Repository enthält einen einfachen Prototypen einer Microservice-Architektur mit Python und Docker. Der Prototyp besteht aus vier Services:

- **order-service** – koordiniert Bestellungen und führt eine Transaktion über Inventory und Payment aus.
- **inventory-service** – verwaltet den Lagerstand.
- **payment-service** – verarbeitet Zahlungen.
- **frontend** – bietet ein einfaches Web-Interface zur Erstellung von Bestellungen.

Die Kommunikation erfolgt über HTTP-APIs. Die Bestellung stellt einen Transaktions-Usecase dar: Zuerst wird Lagerbestand reserviert, danach eine Zahlung ausgelöst. Scheitert die Zahlung, wird der Lagerbestand wieder freigegeben (SAGA / Compensation).

## Starten
Voraussetzung ist eine lokale Installation von Docker und Docker Compose. Anschließend kann der Prototyp wie folgt gestartet werden:

```bash
docker compose up --build
```

Die Services sind danach erreichbar unter:

- Frontend: http://localhost:8003
- Order-Service: http://localhost:8000/docs
- Inventory-Service: http://localhost:8001/docs
- Payment-Service: http://localhost:8002/docs

Zum Stoppen `Ctrl+C` drücken und anschließend `docker compose down` ausführen.

## Entwicklung
Jeder Service basiert auf [FastAPI](https://fastapi.tiangolo.com/). Der Einstiegspunkt befindet sich in `app/main.py` der jeweiligen Komponente.

## Report
Ein ausführlicher Report (3000 Wörter) ist in `report/REPORT.md` vorzubereiten. Er soll Architektur, Sicherheitsaspekte und Fault Tolerance beschreiben.
