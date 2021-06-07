#!/usr/bin/env python3.7

from random import randrange
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


p = 0x92d9c4cebe39e2182b2e781047320548d5dbb0471e8f62ad1f39255c6c32e38849a69e8bae661266f115686235093ae69c479787600afce8a940127d07bd28e5f26dda53d89640088558f63a42e6007c50558af642d70b2e533576a1c6c0f285a2fa94c22eea2586c253bd86804a8e7abfc3f299f5d2e1da13daed627a0db877
g = 0x2b4c217b740edb9b2491b9d7f5efaf32f3fee67b682d6e3802eb3a7fb1956073885f4a49725b543f292d6bb32af11af929b11a2deffac180f1b1ad95594bc813a26a1f70d0407a371603e06ed4418302952bf907e30979c0910ffed1ca146af3c3a223440186fd06249a85831a4ab73788ed4e90fc29a9d8875e842027bcfc22


def key_exchange() -> bytes:
    while True:
        x = randrange(2, p)
        if pow(g, x, p) > 1:
            break

    # print("[*] My public key:")
    # print(pow(g, x, p))

    print(f"[?] Please, input your public key:")
    shared = pow(int(input()), x, p)
    assert 1 < shared < p - 1, 'invalid shared key'
    
    return md5(shared.to_bytes(128, 'big')).digest()


def main(flag):
    print(f'[*] Hi!')

    key = key_exchange()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypt = lambda m: cipher.encrypt(pad(m.encode(), AES.block_size)).hex()
    print(f'[+] Passed key exchange. Switching to encrypted mode...')

    print(encrypt(f'[?] Here is your flag: {flag}'))
    return


if __name__ == '__main__':
    try:
        with open('flag.txt', 'r') as file:
            flag = file.read().strip()

        main(flag)
    except Exception as e:
        print(f'[-] {e}')
