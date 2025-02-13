FROM debian:buster

RUN apt update && \
    apt install python3 python3-pip libldap2-dev libsasl2-dev xmlsec1 sudo -y && \
    pip3 install --upgrade pip && \
    pip3 install fastapi-framework-mvc &&\
    useradd fastapi -u 1000 -m && \
    mkdir -p /home/flask && \
    chown -R fastapi:fastapi /home/flask && \
    mkdir -p /etc/server/ && \
    mkdir -p /var/log/server/ && \
    mkdir -p /srv/http/ && \
    chown -R fastapi:fastapi /var/log/server/ /srv/http/ && \
    chmod -R 775 /var/log/server/ /srv/http/

USER fastapi

WORKDIR /srv/http

ENTRYPOINT /bin/bash
