.PHONY: test

virtualenv:
	virtualenv env

init:
	pip install -r requirements.txt

test:
	pytest ./test

run:
	python ./src/main.py --data_path "./data/top-1m.csv"
