FROM python:3.8

RUN apt update \
    && apt install -y socat

RUN useradd -M -s /bin/false service

WORKDIR /var/service/

COPY server.py flag.txt requirements.txt ./

RUN pip install -r requirements.txt

USER service

ENTRYPOINT socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"timeout 30 python3.8 -u server.py"
