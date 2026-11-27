# One version, in one place: pyproject.toml.
VERSION := $(shell python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
IMAGE ?= shop-model
GIT_SHA := $(shell git rev-parse --short HEAD 2>/dev/null || echo nogit)
GATE_SPLIT ?= holdout

.PHONY: install lint test validate gate build up version ci

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install --no-deps -e ".[dev]"

lint:
	ruff check src tests

test:
	pytest -q

validate:
	shop-validate

gate:
	shop-gate --split $(GATE_SPLIT)

build:
	docker build --build-arg MODEL_VERSION=$(VERSION) -t $(IMAGE):$(VERSION) -t $(IMAGE):$(VERSION)-$(GIT_SHA) .

up:
	MODEL_VERSION=$(VERSION) docker compose up -d --build

version:
	@echo $(VERSION)

ci: lint test validate gate build
