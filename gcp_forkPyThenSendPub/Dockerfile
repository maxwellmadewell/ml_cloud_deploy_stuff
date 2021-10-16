FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

COPY requirements.txt requirements.txt

run pip3 install -r requirements.txt

CMD ["python3", "forkPythonBlockSendPubMsg.py"]