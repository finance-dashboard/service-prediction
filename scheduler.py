#!/usr/bin/env python3
import os
import numpy as np
import grpc
import logging
from currency_service_pb2 import TimeSlice
from currency_service_pb2_grpc import CurrencyProviderStub
from flask import Flask, request, jsonify
from redis import Redis
from redis.exceptions import ConnectionError
from rq import Queue
from jobs import job

# TODO: do not use global variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', None)

stocks_host = os.getenv('STOCKS_HOST', 'localhost')
stocks_port = os.getenv('STOCKS_PORT', 50000)

crypto_host = os.getenv('CRYPTO_HOST', 'localhost')
crypto_port = os.getenv('CRYPTO_PORT', 50000)

dummy_host = os.getenv('DUMMY_HOST', 'localhost')
dummy_port = os.getenv('DUMMY_PORT', 50000)

queue = Queue(connection=Redis(redis_host, redis_port, redis_password))
app = Flask(__name__)

stocks_codes = {"TCSG", "YNDX", "SBER", "TSLA", "MOEX"}
crypto_codes = {"BTC-USD", "ETH-USD", "XRM-USD"}


@app.post('/predict')
def schedule_job():
    params = request.json

    if params is None:
        return 'Is content-type set to application/json?', 400

    for param in ['start_date', 'end_date', 'code']:
        if param not in params:
            return f'Missing parameter "{param}"', 400

    slc = TimeSlice(start=params['start_date'],
                    end=params['end_date'],
                    currencyCode=params['code'])
    vals = []

    if params['code'] in stocks_codes:
        grpc_host = stocks_host
        grpc_port = stocks_port
    elif params['code'] in crypto_codes:
        grpc_host = crypto_host
        grpc_port = crypto_port
    elif params['code'] == 'dummy':
        grpc_host = dummy_host
        grpc_port = dummy_port
    else:
        return f'Unsupported code {params["code"]}', 500

    try:
        with grpc.insecure_channel(f'{grpc_host}:{grpc_port}') as ch:
            stub = CurrencyProviderStub(ch)
            values = stub.GetCurrency(slc)

            for val in values:
                vals.append(val.value)
    except grpc.RpcError as e:
        logging.error(e)
        return 'Try again later', 503

    try:
        j = queue.enqueue(job, np.array(vals))
    except ConnectionError:
        return 'Technical issues, check back a bit later', 503

    res = {'job_id': j.id}

    return jsonify(res), 202


@app.get('/check_status/<job_id>')
def check_status(job_id):
    try:
        res = queue.fetch_job(job_id)
    except ConnectionError as e:
        logging.error(e)
        return 'Technical issues, check back a bit later', 503

    if res is None:
        return 'No such job', 400
    if res.result is None:
        return 'Still working', 202

    return jsonify({'result': res.result}), 200


if __name__ == '__main__':
    logging.warn('Starting scheduler server')
    app.run(host="0.0.0.0")
