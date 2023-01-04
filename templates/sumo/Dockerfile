FROM debian:bullseye-slim

#Install sumo
RUN apt-get update 
RUN apt-get -y install sumo sumo-tools sumo-doc

RUN apt-get -y install python3-pip
ENV SUMO_HOME /usr/share/sumo

#test Tools for checking x11 
RUN apt-get -y install x11-apps
ENV DISPLAY gateway.docker.internal:0.0


# app
WORKDIR /opt/app

COPY example example
COPY app.py app.py
COPY traciapp.py traciapp.py
COPY webapp.py webapp.py

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]