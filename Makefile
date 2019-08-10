#!/usr/bin/env make

#
# Makefile
#
# Copyright (C) 2019 Franco Masotti <franco.masotti@live.com>
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
	yapf --style '{based_on_style: pep8; indent_width: 4}' -i fattura_pa_reader/*.py tests/*.py
	flake8 fattura_pa_reader/*.py --ignore=F401,E501 tests/*.py

doc:
	$(MAKE) -C docs html

install:
	pip install .

test:
	python setup.py test

uninstall:
	pip uninstall fattura_elettronica_reader

dist:
	python setup.py sdist
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info

.PHONY: default pep doc install test uninstall dist upload clean
