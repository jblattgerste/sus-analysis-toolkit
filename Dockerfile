# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /dashApp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 80

CMD ["python", "./dashApp.py", "--host=0.0.0.0"]
