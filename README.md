# Shop Model

Predicts whether an item in the shop will sell based on its price.

## Requirements

Python 3.14 with virtual environment support.

On Ubuntu:

```bash
sudo apt install python3.14-venv
```

## Installation

Run these commands from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e ".[dev]"
cp env.example .env
```

## Testing

```bash
pytest
```

## Training

```bash
shop-train
```

The trained model is saved to `models/model.joblib`.

Shared configuration is stored in `config/config.yaml`, while machine-specific settings are stored in `.env`.

## Prediction API

Start the API server:

```bash
uvicorn shop_model.api:app --port 8888
```

The server loads the trained model from `models/model.joblib`.
Make sure you have run `shop-train` first.

In a second terminal, check that the API is running:

```bash
curl localhost:8888/health
```

Request a prediction:

```bash
curl localhost:8888/predict \
  -H "Content-Type: application/json" \
  -d '{"price": 20}'
```

Expected response:

```json
{"price":20.0,"probability_sold":0.675}
```

Interactive API documentation is available at:

http://localhost:8888/docs

Stop the server with Ctrl+C.

## Docker

Build the Docker image:

```bash
docker build -t shop-model:0.1 .
```

Start the container:

```bash
docker run -d --name shop-api -p 8888:8888 shop-model:0.1
```

Check that it's running:

```bash
docker ps
```

Test the API:

```bash
curl localhost:8888/health

curl localhost:8888/predict \
  -H "Content-Type: application/json" \
  -d '{"price":20}'
```

View container logs:

```bash
docker logs shop-api
docker logs -f shop-api
```

Stop and remove the container:

```bash
docker stop shop-api
docker rm shop-api
```

## Running with Docker Compose

Start the API and PostgreSQL database:

docker compose up -d --build

Check that both containers are running:

docker compose ps

Send a prediction:

curl -X POST localhost:8888/predict \
  -H "Content-Type: application/json" \
  -d '{"price": 8}'

View stored predictions:

docker compose exec db psql -U shop -d shop -c "SELECT * FROM predictions;"

View API logs:

docker compose logs -f api

Stop and remove the containers:

docker compose down

## Monitoring with Prometheus and Grafana

The project uses Docker Compose to run four services:

- **FastAPI** — serves predictions and exposes metrics.
- **PostgreSQL** — stores individual predictions.
- **Prometheus** — collects API metrics every 5 seconds.
- **Grafana** — visualises the collected metrics.

### Start the services

From the project root:

```bash
docker compose up -d --build
```

Check that all four services are running:

```bash
docker compose ps
```

### Access the services

| Service | URL (from Ubuntu) |
|---|---|
| FastAPI documentation | http://localhost:8888/docs |
| FastAPI metrics | http://localhost:8888/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

When accessing these services from the Mac, replace `localhost` with the Ubuntu VM's IP address (check using `hostname -I`).

In Grafana, navigate to **Dashboards → Model service**.

### Generate normal traffic

```bash
python3 monitoring/traffic.py --field price --mean 23 --sd 12 --duration 300
```

This simulates approximately five prediction requests per second, using prices centred around €23.

### Simulate data drift

```bash
python3 monitoring/traffic.py --field price --mean 35 --sd 12 --duration 300
```

This changes the average input price from €23 to €35 while maintaining the same standard deviation.

Observe the **Average Input Value** and **Input distribution** panels in Grafana to see the shift.

### Simulate an API outage

While generating traffic, run the following commands in a separate terminal:

```bash
docker compose stop api
```

After approximately 30 seconds:

```bash
docker compose start api
```

Observe how the request rate drops and recovers in Grafana.

### Stop the services

```bash
docker compose down
```

Docker Compose stops and removes the containers while preserving the named volumes. Avoid `docker compose down -v` unless you deliberately want to delete persisted data.
