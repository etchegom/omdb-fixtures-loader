#!make

dev:
	@poetry install --no-interaction --no-root
	@poetry shell

lint:
	@flake8 omdb_fixtures_loader

fmt:
	@autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive omdb_fixtures_loader
	@isort -rc omdb_fixtures_loader
	@black omdb_fixtures_loader setup.py
