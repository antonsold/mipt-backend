FROM python:3.4-alpine
ADD . /code
WORKDIR ./code

ENV FLASK_APP first_app.py

RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base

RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["flask", "db", "init"]
CMD ["flask", "db", "migrate", "-m", "\"Add two table\""]
CMD ["flask", "db", "upgrade"]
CMD ["flask", "run", "--host=0.0.0.0"]