#!/usr/bin/env python3
import numpy as np
from flask import Flask, request, jsonify
from redis import Redis
from redis.exceptions import ConnectionError
from rq import Queue
from jobs import job

queue = Queue(connection=Redis())
app = Flask(__name__)


@app.post('/predict')
def schedule_job():
    params = request.json

    if params is None:
        return 'Is content-type set to application/json?', 400

    for param in ['start_date', 'end_date', 'type']:
        if param not in params:
            return f'Missing parameter "{param}"', 400

    # TODO: get data from external provider
    try:
        # TODO: replace array stub with actual value
        j = queue.enqueue(job, np.array([1, 2, 3, 4]))
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
