.PHONY: clean test
clean:
	find . -type f -regextype posix-egrep -regex ".*\.(.*~|pyc|so)" -delete
	rm -rf build dist *.egg-info MANIFEST
installdeps:
	cat packages.txt | xargs sudo apt-get -y install
	sudo pip install -r requirements.txt
install: installdeps clean
	sudo python setup.py install
test: clean build
	nosetests tests --verbosity 3 --nocapture
build: clean
	python setup.py build_ext -i
	python setup.py build
sdist: clean
	python setup.py sdist