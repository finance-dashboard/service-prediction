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

queue = Queue(connection=Redis())
app = Flask(__name__)

grpc_host = os.getenv('HOST', 'localhost')
grpc_port = os.getenv('PORT', '50000')


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
    except ConnectionError:
        return 'Technical issues, check back a bit later', 503

    if res is None:
        return 'No such job', 400
    if res.result is None:
        return 'Still working', 202

    return jsonify({'result': res.result}), 200


if __name__ == '__main__':
    app.run()
