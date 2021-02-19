test-install: _devel-install-virtualenv
devel-install: _devel-install-virtualenv

_%:
	virtualenv $@
	. $@/bin/activate && pip install -e .

clean:
	rm _* dist -r
	

run-unit_tests: _devel-install-virtualenv
	. $</bin/activate && pip install pytest pudb pint
	. $</bin/activate && cd testing && time python -m pytest -s $(OPTS)

run-cli_tests: _devel-install-virtualenv
	. $</bin/activate && pip install cram
	. $</bin/activate && cd testing && time cram *.t

run-tests:
	make test-install
	make run-unit_tests
	make run-cli_tests

list-requirements:
	@ pipenv graph | grep '^[^ ]' 

build-package:
	pipenv run python setup.py sdist

upload-package:
	pipenv run python -m twine upload dist/*

