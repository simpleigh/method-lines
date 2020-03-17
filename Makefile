.PHONY: build, check, clean, lint

build:
	python setup.py sdist
	python setup.py bdist_wheel

check:
	python -m unittest

clean:
	rm -rf build
	rm -rf dist
	rm -rf method_lines.egg-info

lint:
	flake8 method_lines
