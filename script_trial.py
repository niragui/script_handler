import sys

from time import sleep

import datetime

print(sys.argv)

if len(sys.argv) < 2:
    raise Exception("Must Add Parameter")

sleep_param = sys.argv[1]

if not sleep_param.isnumeric():
    raise TypeError(f"Must Be A Int [{sleep_param}]")

sleep_param = int(sleep_param)
print(f"[{datetime.datetime.now()}] Starting")

sleep(sleep_param)

print(f"[{datetime.datetime.now()}] Ending")