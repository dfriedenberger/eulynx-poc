FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "app.py", "--host" , "server" , "--port" , "5000"]
