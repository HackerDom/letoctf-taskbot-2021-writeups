#!/bin/sh

nsjail \
    --mode l \
    --port 31337 \
    --time_limit 30 \
    --disable_proc \
    --bindmount_ro /bin/ \
    --bindmount_ro /usr/bin/ \
    --bindmount_ro /dev/null \
    --bindmount_ro /etc/passwd \
    --bindmount_ro /etc/group \
    --bindmount_ro /var/service/ \
    --bindmount_ro /tmp/libs/:/lib/x86_64-linux-gnu/ \
    --bindmount_ro /tmp/ld-linux-x86-64.so.2:/lib64/ld-linux-x86-64.so.2 \
    --cwd /var/service/ \
    --hostname mal \
    --max_cpus 1 \
    --stderr_to_null \
    -- \
    ./MAL
