install:
	pip3 install -r requirements.txt
test: install
	python3 -m unittest
run: test
	python3 main.py
