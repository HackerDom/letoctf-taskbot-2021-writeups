#!/usr/bin/env python3.8

from math import cos
from string import printable


N = 16
bits = 4096
R = RealField(bits)


def recover_block(q, pol):
    M_dl = 0 * matrix.identity(ZZ, N)
    M_dr = q * matrix.identity(ZZ, N)
    M_ul = matrix.identity(ZZ, N)
    M_ur = matrix(ZZ, [[0] * N])

    for i in range(N):
        line = list(pol)
        line = line[-i:] + line[:-i]
        M_ur = M_ur.stack(vector(ZZ, line))

    M = (M_ul.augment(M_ur[1:])).stack(M_dl.augment(M_dr))
    # print(M)

    L = M.LLL()
    # print(L)

    for row in L:
        for part in [row[:N], row[N:]]:
            for candidate in [part, -part]:
                possible_flag = bytes(int(z) % 256 for z in candidate)
                
                if all(chr(z) in printable for z in possible_flag):
                    flag = bytes(possible_flag).decode()
                    
                    for i in range(len(flag) - 1):
                        print(flag[i:] + flag[:i])

                    print()


def recover_polynomial(q, result):
    p1 = int(bits * log(2, 10))
    p2 = 57

    keystream = [R(1 + z).sin() for z in range(N)]
    keystream_lifted = [round(z * 10^p1) for z in keystream]
    result_lifted = round(result * 10^p1) * 10^p2
    
    M = (matrix.identity(ZZ, N + 1)).augment(vector(ZZ, keystream_lifted + [-result_lifted]))
    L = M.LLL()

    row = L[0]
    sign = row[-2]
    values = [float(R(z) / 10^p2) * sign for z in row[:N]]

    cache = {}

    for x in range(q):
        cache[cos(x)] = x

    return [cache[value] for value in values]

    
def main():
    with open('output.txt', 'r') as file:
        result = sage_eval(file.read())

    for q, ciphertext in result:
        pol = recover_polynomial(q, ciphertext)
        recover_block(q, pol)


if __name__ == '__main__':
    main()
    