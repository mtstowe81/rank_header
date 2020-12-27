.PHONY: test

virtualenv:
	virtualenv env

init:
	pip install -r requirements.txt

test:
	pytest ./tests

run:
	python ./rankheader/main.py --data_path "./data/top-1m.csv"
