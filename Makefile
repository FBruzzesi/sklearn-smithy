sources = sksmithy tests

clean-folders:
	rm -rf __pycache__ */__pycache__ */**/__pycache__ \
		.pytest_cache */.pytest_cache */**/.pytest_cache \
		.ruff_cache */.ruff_cache */**/.ruff_cache \
		.mypy_cache */.mypy_cache */**/.mypy_cache \
		site build dist htmlcov .coverage .tox

lint:
	ruff version
	ruff format $(sources)
	ruff check $(sources) --fix
	ruff clean

test:
	pytest tests -n auto

coverage:
	rm -rf .coverage
	(rm docs/img/coverage.svg) || (echo "No coverage.svg file found")
	coverage run -m pytest
	coverage report -m
	coverage-badge -o docs/img/coverage.svg

types:
	mypy $(sources)

check: lint test types clean-folders

docs-serve:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

pypi-push:
	rm -rf dist
	hatch build
	hatch publish

get-version :
	@echo $(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)
