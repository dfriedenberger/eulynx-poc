FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py app.py
CMD [ "python3", "app.py", "--host" , "server" , "--port" , "5000"]
