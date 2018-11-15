FROM python:3.7-slim-stretch

RUN apt update && apt install git -y

ADD . /

RUN pip install -r requirements.txt

ENV API_GATEWAY_URL=http://localhost:8001
ENV FLASK_APP=service.py

EXPOSE 5000

CMD [ "flask", "run" ]