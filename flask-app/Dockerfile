FROM python:3.6

ADD requirements.txt /app/
WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt && \
    echo "pip freeze:" && pip freeze

ADD . /app/

ENV LISTEN_HOST=0.0.0.0
ENV LISTEN_PORT=8080

CMD ["python3", "-u", "app.py"]
