#!make

dev:
	@poetry install --no-interaction --no-root
	@poetry shell

pre-commit:
	@pre-commit run --all-files
