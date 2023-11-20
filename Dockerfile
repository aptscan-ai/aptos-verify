FROM ubuntu:22.04 as latest
WORKDIR /usr/src/server
COPY server.py . 
COPY aptos_verify/ aptos_verify/
COPY pyproject.toml .
COPY move/ move/
COPY requirement.txt .

RUN apt-get update && apt-get install -y curl
RUN apt install python3 python3-pip -y
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev 

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
RUN . /root/.cargo/env
ENV PATH="/root/.cargo/bin:${PATH}"

RUN curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3
ENV PATH="/root/.local/bin:$PATH"

RUN pip install poetry==1.7.0 && poetry install && pip install -r requirement.txt


ARG HTTP_PORT=9998

EXPOSE ${HTTP_PORT}

CMD ["python3", "server.py"]