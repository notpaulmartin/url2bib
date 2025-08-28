info:
	# Use:
	# $ make publish
	# or
	# $ make publish-test

publish: build upload-pypi
publish-test: build upload-test

build:
	rm -rf ./dist
	./env/bin/python -m build

upload-pypi:
	./env/bin/python -m twine check dist/*
	./env/bin/python -m twine upload dist/*

upload-test:
	./env/bin/python -m twine check dist/*
	./env/bin/python -m twine upload --repository testpypi dist/*
