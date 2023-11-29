FROM ubuntu:latest

RUN apt update

RUN apt install software-properties-common -y

RUN add-apt-repository ppa:ecal/ecal-latest

RUN apt update && apt install ecal -y
# && \
    #  && \
    #add-apt-repository ppa:ecal/ecal-latest && \
    #apt update && \
    #apt install ecal
