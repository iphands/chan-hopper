#!/bin/bash

# python main.py \
#   --iperf-host noir.lan \
#   --unifi-host unifi-controller.noir.lan \
#   --ap-id 5de8531246e0fb00f79da35c\
#   --mode 2 \
#   --nm-uuid d9225f27-b7b1-4181-9388-728522d7dff1

echo
echo "-- For HandsNet"
echo "python main.py test-from-wired \
  --iperf-host noir.lan \
  --unifi-host unifi-controller.noir.lan \
  --ap-id 5de8531246e0fb00f79da35c \
  --mode 2 \
  --nm-uuid d9225f27-b7b1-4181-9388-728522d7dff1
"

echo "-- For HandsNet5"
echo "python main.py test-from-client \
  --iperf-host noir.lan \
  --unifi-host unifi-controller.noir.lan \
  --ap-id 5de8531246e0fb00f79da35c \
  --mode 5 \
  --nm-uuid a04d7a33-fb6d-418c-bf4f-0e640e390e1e"
