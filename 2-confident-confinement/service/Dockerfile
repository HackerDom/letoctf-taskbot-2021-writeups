FROM keltecc/nsjail:latest

RUN apt update \
    && apt install -y python3.8

RUN useradd -M -s /bin/false jail

COPY entrypoint.sh /tmp/

RUN chmod 555 /tmp/entrypoint.sh

COPY server.py flag.txt /var/service/

USER jail

ENTRYPOINT /tmp/entrypoint.sh
