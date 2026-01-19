.PHONY: run

DIR ?= ./receipts
run:
	echo "Running receipts app with directory: ${DIR}"
	python3 src/receipts_app/main.py ${DIR} --print
