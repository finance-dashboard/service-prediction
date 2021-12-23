#!/usr/bin/env python3
import os
import numpy as np
import grpc
import logging
from currency_service_pb2 import TimeSlice
from currency_service_pb2_grpc import CurrencyProviderStub
from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from redis.exceptions import ConnectionError
from rq import Queue
from jobs import job

conn_strings = os.getenv('PROVIDER_CONNS', "")
conns = {}

for i in conn_strings.split(';'):
    conn, codes = i.split('=')
    codes = codes.split(',')
    host, port = conn.split(':')
    conns[host] = {'port': int(port), 'codes': set(codes)}

# TODO: do not use global variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', None)

queue = Queue(connection=Redis(redis_host, redis_port, redis_password))
app = Flask(__name__)
CORS(app)


@app.post('/predict')
def schedule_job():
    params = request.json

    if params is None:
        return ('No params received. Is content-type set to application/json?',
                400)

    for param in ['start_date', 'end_date', 'code']:
        if param not in params:
            return f'Missing parameter "{param}"', 400

    slc = TimeSlice(start=params['start_date'],
                    end=params['end_date'],
                    currencyCode=params['code'])
    vals = []

    grpc_host = None
    grpc_port = None

    for host, body in conns.items():
        if params['code'] in body['codes']:
            grpc_host = host
            grpc_port = body['port']

    if grpc_host is None or grpc_port is None:
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
        return 'No such job', 404
    if res.result is None:
        return 'Still working', 202

    return jsonify({'result': res.result}), 200


if __name__ == '__main__':
    logging.warn('Starting scheduler server')
    app.run(host="0.0.0.0")
