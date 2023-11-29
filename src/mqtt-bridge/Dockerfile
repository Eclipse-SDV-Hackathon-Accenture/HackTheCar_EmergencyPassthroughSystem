# Starting from 22.04 (jammy)
FROM ubuntu:20.04

# Adding project's resources
ADD src /opt/src

# Installing apt add repository capability
RUN apt update && \
    apt install software-properties-common -y

# Adding ecal-repo to apt
RUN add-apt-repository ppa:ecal/ecal-latest

# Installing required software
RUN apt update && apt install wget ecal python3-pip python3-dev -y

# Working at /opt
WORKDIR /opt

RUN wget https://github.com/eclipse-ecal/ecal/releases/download/v5.12.1/ecal5-5.12.1-1focal-cp38-cp38-linux_x86_64.whl

RUN pip install paho-mqtt ecal5-5.12.1-1focal-cp38-cp38-linux_x86_64.whl

RUN apt autoremove
