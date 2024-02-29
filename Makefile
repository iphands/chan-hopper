.PHONY: debug
debug:
	python main.py \
	   --debug true \
	  --iperf-host noir.lan \
	  --unifi-host unifi-controller.noir.lan \
	  --ap-id 5de8531246e0fb00f79da35c \
	  --mode 2 \
	  --nm-uuid d9225f27-b7b1-4181-9388-728522d7dff1

.PHONY: check
check:
	black . && pyre && python ./test.py
