FROM python:3.11.6-bookworm as latest

WORKDIR /usr/src/server
COPY server.py . 
COPY aptos_verify/ aptos_verify/
COPY pyproject.toml .

RUN pip install poetry==1.7.0 && poetry install 

ARG HTTP_PORT=9998
ARG HTTP_HOST='localhost'

EXPOSE ${HTTP_PORT}

CMD ["python3 server.py"]