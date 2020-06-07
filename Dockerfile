FROM python:3.8.3-alpine

ENV API_SERVER=localhost

WORKDIR /ws_server
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD ws_server.py ./
ENTRYPOINT python ws_server.py "${API_SERVER}" 20080
