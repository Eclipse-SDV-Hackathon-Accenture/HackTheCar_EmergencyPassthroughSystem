FROM ubuntu:20.04

# # Adding project's resources
# ADD src /opt/src

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y \
    software-properties-common \
    python3 \
    python3-pip \
    libc6 libcurl4 libgcc-s1 libhdf5-103 libprotobuf17 libqt5core5a libqt5gui5 libqt5widgets5 libqt5svg5 libstdc++6 sysstat ifstat libqwt-qt5-6 libyaml-cpp0.6 \
    wget \
    vim \
    nano \
    git

RUN add-apt-repository ppa:ecal/ecal-latest && \
    apt update && \
    apt install -y \
    ecal

# Working at /opt
WORKDIR /opt

RUN wget https://github.com/eclipse-ecal/ecal/releases/download/v5.12.1/ecal5-5.12.1-1focal-cp38-cp38-linux_x86_64.whl

COPY ./pyproject.toml /opt/pyproject.toml

# Installing pip packages
RUN pip3 install ecal5-5.12.1-1focal-cp38-cp38-linux_x86_64.whl && \
    pip3 install .
# Cleaning up
RUN rm ecal5-5.12.1-1focal-cp38-cp38-linux_x86_64.whl && \
    rm pyproject.toml
