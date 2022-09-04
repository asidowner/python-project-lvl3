install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

package-remove:
	python3 -m pip uninstall hexlet-code

lint:
	poetry run flake8 page_loader tests

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint