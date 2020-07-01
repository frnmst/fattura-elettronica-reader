#!/usr/bin/env make
#
# Makefile
#
# Copyright (C) 2019-2020 Franco Masotti <franco.masotti@live.com>
#
# This file is part of fattura-elettronica-reader.
#
# fattura-elettronica-reader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fattura-elettronica-reader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.
#

default: pep doc test

githook:
	git config core.hooksPath .githooks

pep:
	pipenv run yapf --style '{based_on_style: pep8; indent_width: 4}' -i fattura_pa_reader/*.py tests/*.py
	pipenv run flake8 fattura_pa_reader/*.py --ignore=F401,E501 tests/*.py

doc:
	pipenv run $(MAKE) -C docs html

install:
	pip install .

uninstall:
	pip uninstall fattura_elettronica_reader

install-dev:
	pipenv install

uninstall-dev:
	pipenv --rm

test:
	pipenv run python setup.py test

dist:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
	pipenv run pipenv run twine check dist/*

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	pipenv run $(MAKE) -C docs clean

.PHONY: default pep doc install install-dev test uninstall uninstall-dev dist upload clean
