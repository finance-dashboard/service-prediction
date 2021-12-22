#!/usr/bin/env python3
import os
import sys
import logging
import time

# Preimport required modules
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from redis import Redis
from rq import Connection, Worker

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

REDIS_CONN = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
TRY_COUNTER = 10

while TRY_COUNTER > 0:
    try:
        with Connection(REDIS_CONN):
            qs = sys.argv[1:] or 'default'

            w = Worker(qs)
            w.work()
    # TODO: handle specific connection error exception
    except:
        logging.warning(f'Unable to connect. {TRY_COUNTER} attempts left')
        time.sleep(5)
        TRY_COUNTER -= 1
