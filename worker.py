#!/usr/bin/env python3
import sys

# Preimport required modules
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from rq import Connection, Worker

with Connection():
    qs = sys.argv[1:] or 'default'

    w = Worker(qs)
    w.work()
