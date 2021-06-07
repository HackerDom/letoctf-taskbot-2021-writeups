#!/usr/bin/env python3.7

from pwn import remote
from random import randrange
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


p = 0x92d9c4cebe39e2182b2e781047320548d5dbb0471e8f62ad1f39255c6c32e38849a69e8bae661266f115686235093ae69c479787600afce8a940127d07bd28e5f26dda53d89640088558f63a42e6007c50558af642d70b2e533576a1c6c0f285a2fa94c22eea2586c253bd86804a8e7abfc3f299f5d2e1da13daed627a0db877


def main(io):
    factor = 348419
    assert (p - 1) % factor == 0
    plaintext = b'[?] Here is your flag:'[:AES.block_size]
    
    while True:
        h = pow(randrange(1, p), (p - 1) // factor, p)
        if 1 < h < p - 1:
            break
    
    io.recvline()
    io.recvline()
    io.sendline(str(h).encode())
    io.recvline()
    ciphertext = bytes.fromhex(io.recvline().strip().decode())

    for x in range(factor):
        key = md5(pow(h, x, p).to_bytes(128, 'big')).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        if ciphertext.startswith(cipher.encrypt(plaintext)):
            print(unpad(cipher.decrypt(ciphertext), AES.block_size))
            break
    
    return


if __name__ == '__main__':
    with remote('0.0.0.0', 31337) as io:
        main(io)
