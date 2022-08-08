#Operating System base image
FROM ubuntu:20.04

#Set the environment variables to run the project
#ENV DEBIAN_FRONTEND noninteractive

ARG DEBIAN_FRONTEND=noninteractive

#Create project directory and inform Docker to run under this directory
WORKDIR /root/repos/ns-3-allinone/ns-3.30/


#Add commands and parameters(Docker runs this firstly when container runs)
#ENTRYPOINT #ENTRYPOINT


#Run commands after ENTRYPOINT run(must have at least one CMD)
CMD ./waf --run scratch/gunji_olsr-randam


#Copy one or more files and folders from local to containers file system
COPY . /tmp


#Same with COPY but for archive and URL copy and execute
#ADD #ADD


#Execute any commands on top of the current image

RUN \
  apt-get update -y && \
  apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed" && \
  apt-get install -y --no-install-recommends sudo

RUN ["/bin/sh", "/tmp/ns-3_install.sh"]

#Inform the Docker that container listens on the specified network ports
#EXPOSE #EXPOSE

#ENV DEBIAN_FRONTEND teletype

#Specify the Dockerfile Author Name and Email
MAINTAINER Ueda sensei's laboratory
