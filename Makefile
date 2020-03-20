.PHONY: build, check, clean, lint

build:
	python setup.py sdist
	python setup.py bdist_wheel

check:
	coverage run -m unittest
	coverage html

clean:
	rm -rf build
	rm -rf coverage
	rm -rf dist
	rm -rf method_lines.egg-info
	rm .coverage

lint:
	flake8 method_lines
