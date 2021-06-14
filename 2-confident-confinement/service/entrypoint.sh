#!/bin/sh

nsjail \
    --mode l \
    --port 31337 \
    --time_limit 30 \
    --disable_proc \
    --bindmount_ro /bin/ \
    --bindmount_ro /usr/bin/ \
    --bindmount_ro /lib \
    --bindmount_ro /lib64 \
    --bindmount_ro /usr/lib \
    --bindmount_ro /dev/null \
    --bindmount_ro /etc/passwd \
    --bindmount_ro /etc/group \
    --bindmount_ro /var/service/ \
    --cwd /var/service/ \
    --hostname jail \
    --max_cpus 1 \
    --stderr_to_null \
    -- \
    /usr/bin/python3.8 -u server.py
