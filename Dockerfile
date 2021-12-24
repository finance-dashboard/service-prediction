FROM python:3.10-slim
WORKDIR /app/
ENV PATH=/app/env/bin:$PATH
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv /app/env && pip install -r /app/requirements.txt --no-cache-dir
COPY . /app
ENTRYPOINT "gunicorn"
CMD "scheduler:app"
