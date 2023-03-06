PYTHON = python3

.PHONY = help test check_codestyle

help:
	@echo "---------------HELP-----------------"
	@echo "To check codestyle type make setup"
	@echo "To test the project type make test"
	@echo "------------------------------------"

test:
	${PYTHON} -m pytest tests

check_codestyle:
	black --check app
	flake8 app
	pylint --rcfile tox.ini --fail-under=9.5 app
	mypy --config-file=tox.ini --check-untyped-defs app

