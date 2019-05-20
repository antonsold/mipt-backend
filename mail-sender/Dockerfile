FROM python:3.6

ADD requirements.txt /app/
WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt && \
    echo "pip freeze:" && pip freeze

ADD . /app/

CMD ["python3", "-u", "mailer.py"]
