.PHONY: check
check:
	black . && pyre && python ./test.py
