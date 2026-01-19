.PHONY: run

DIR ?= ./receipts
run:
	echo "Running receipts app with directory: ${DIR}"
	PYTHONPATH=src python3 -m receipts_app.main ${DIR} --print
