.PHONY: up down logs test fmt api producer consumer dashboard

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	pytest -q

api:
	uvicorn src.api:app --reload --port 8000

producer:
	python -m src.producer

consumer:
	python -m src.consumer

dashboard:
	streamlit run dashboard/app.py

