FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get install -y sudo && \
    sudo apt-get install -y openjdk-8-jdk &&\
    apt-get install -y git && \
    apt-get install -y dos2unix && \
    apt-get install -y zip unzip && \
    apt-get install -y bzip2  && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p $HOME/miniconda


RUN mkdir /STRetch  
   
### Copy the and Mount the Repository to the Container ####
COPY . /STRetch
WORKDIR /STRetch 

RUN dos2unix /STRetch/install.sh && \
    bash /STRetch/install.sh
