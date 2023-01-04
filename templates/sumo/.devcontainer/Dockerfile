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
