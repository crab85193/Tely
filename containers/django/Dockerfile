FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y gettext libgettextpo-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

RUN chmod 755 entrypoint.sh

