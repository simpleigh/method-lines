.PHONY: build, clean

build:
	python setup.py sdist
	python setup.py bdist_wheel

clean:
	rm -r build
	rm -r dist
	rm -r method_lines.egg-info
