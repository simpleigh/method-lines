.PHONY: build, clean

build:
	python setup.py sdist
	python setup.py bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf method_lines.egg-info
