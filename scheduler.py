#!/usr/bin/env python3
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from jobs import job

queue = Queue(connection=Redis())
app = Flask(__name__)


@app.post('/predict')
def schedule_job():
    params = request.json
    if params is None:
        return 'Is content-type set to application/json?', 400

    j = queue.enqueue(job, **params)
    res = {'job_id': j.id}

    return jsonify(res), 202


@app.get('/check_status/<job_id>')
def check_status(self, job_id):
    queue.fetch_job()
    return 200


if __name__ == '__main__':
    app.run()
