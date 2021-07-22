#!/usr/bin/env sage

from math import cos


N = 16
R = RealField(4096)


def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read().strip()


def construct_polynomial(q, plaintext, key):
    F = GF(q)
    P.<x> = PolynomialRing(F)
    Q.<x> = P.quo(x^N - 1)

    r, s = map(Q, map(list, [plaintext, key]))

    return (r / s).lift().change_ring(ZZ)


def encrypt_polynomial(pol):
    values = [R(cos(z)) for z in pol]
    keystream = [R(1 + z).sin() for z in range(pol.degree() + 1)]

    return sum(k * v for k, v in zip(keystream, values))


def encrypt_block(plaintext, key):
    assert len(plaintext) == len(key) == N

    t = ceil(mean(plaintext + key)) ^ 3
    q = next_prime(t + randint(0, t))
    pol = construct_polynomial(q, plaintext, key)
    ciphertext = encrypt_polynomial(pol)

    return q, ciphertext


def encrypt(plaintext, key):
    assert len(plaintext) == len(key)

    ciphertext = []

    for i in range(0, len(plaintext), N):
        plaintext_block = plaintext[i:i+N]
        key_block = key[i:i+N]
        ciphertext_block = encrypt_block(plaintext_block, key_block)
        ciphertext.append(ciphertext_block)

    return ciphertext

 
def main():
    flag = read_file('flag.txt')
    key = read_file('key.txt')

    result = encrypt(flag, key)

    print(result)


if __name__ == '__main__':
    main()
