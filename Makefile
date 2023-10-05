#!make

dev:
	@poetry install --no-interaction --no-root
	@poetry shell

lint:
	@pflake8 omdb_fixtures_loader

fmt:
	@isort -rc omdb_fixtures_loader
	@black omdb_fixtures_loader setup.py
