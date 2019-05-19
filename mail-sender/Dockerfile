FROM alpine:3.5
RUN apk add --update py2-pip
RUN apk add --update bash
WORKDIR /code
ADD . /code

ENV APP_MAIL_USERNAME "buchnev, kozinov"
ENV APP_MAIL_PASSWORD="backend2019"

RUN pip install -r /code/requirements.txt
CMD ["/code/wait-for-it.sh", "rabbit:5672", "--", "python", "-u", "/code/receive.py"]
