.PHONY: setup api web dev docs test fmt lint type bench

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"

api:
	autonomi api

web:
	cd dashboard && npm i && npm run dev

dev: api web

docs:
	mkdocs serve

test:
	pytest -q

fmt:
	black .

lint:
	ruff .

type:
	mypy src

bench:
	python -m autonomi_kit.eval.bench --tasks small --plot out/bench.png
