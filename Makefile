.PHONY: sync build check clean lint test

sync:
	uv sync --locked --all-groups

build:
	uv build

check: lint test

clean:
	rm -rf dist
	rm -rf htmlcov
	rm -rf method_lines.egg-info
	rm -f .coverage
	rm -f coverage.xml

lint:
	uv run --locked ruff check .

test:
	uv run --locked pytest \
	    --cov method_lines \
	    --cov-report html \
	    --cov-report term-missing \
	    --cov-report xml
