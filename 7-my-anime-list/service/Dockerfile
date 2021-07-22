FROM keltecc/nsjail:latest

RUN useradd -M -s /bin/false mal

ADD entrypoint.sh /tmp/

RUN chmod 555 /tmp/entrypoint.sh

ADD MAL flag.txt /var/service/

ADD libs.tar.gz /tmp/libs/

ADD ld-linux-x86-64.so.2 /tmp/

USER mal

ENTRYPOINT /tmp/entrypoint.sh
