FROM ubuntu:22.04 as latest

WORKDIR /usr/src/server
COPY . .

RUN apt update && apt-get install -y build-essential python python3 zip net-tools iptables sudo curl && pip install poetry==1.7.0 && poetry install 

ARG HTTP_PORT=9998
ARG HTTP_HOST='localhost'

EXPOSE ${HTTP_PORT}

CMD ["python3", "-m server"]