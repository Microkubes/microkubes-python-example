FROM python:3.7-slim-stretch

RUN apt update && apt install git -y
RUN apt-get install ca-certificates

ADD . /

RUN pip install -r requirements.txt

ENV API_GATEWAY_URL=http://kong-admin:8001
ENV FLASK_APP=service.py
ENV FLASK_ENV=development 

CMD ["flask", "run", "--host=0.0.0.0"]