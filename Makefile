.PHONY: setup lint test

setup:
	git clone https://spacePetLabs@dev.azure.com/spacePetLabs/PythonSpace/_git/py-tools
	cd py-tools && poetry env use python3.12 && poetry install

lint:
	cd py-tools/py_tools && poetry run ./do_lint.sh --dir ../../. --output ../../analys.log

test:
	pytest tests/