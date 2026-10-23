.PHONY: sync build check clean lint test

sync:
	uv sync --locked --all-groups

build:
	uv build

check: lint test

clean:
	rm -rf coverage
	rm -rf dist
	rm -rf method_lines.egg-info
	rm .coverage

lint:
	uv run --locked flake8 method_lines

test:
	uv run --locked coverage run -m unittest
	uv run --locked coverage html
