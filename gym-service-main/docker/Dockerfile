FROM python:3-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

#Setup
RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    bash \
    build-base \
    jpeg-dev \
    python3 \
    python3-dev \
    py3-pip \
    zlib-dev

RUN pip3 -V
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# clean
RUN apk del -r \
    python3-dev \
    zlib-dev

COPY . /app/


CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
