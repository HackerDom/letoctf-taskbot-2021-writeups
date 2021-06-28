import sys
import requests

URL = sys.argv[1]

F = GF(2)


def xor_bytes(a, b):
    return bytes([x^^y for x,y in zip(a, b)])

def get_flag():
    r = requests.get(URL + '/api/get_flag')
    return bytes.fromhex(r.json()['encrypted_flag'])

def encrypt(data):
    r = requests.post(URL + '/api/encrypt', json={'pt': data.hex()})
    return bytes.fromhex(r.json()['ct'])

def bytes_to_vector(text):
    i_text = ZZ(int(text.hex(), 16))
    b_text = i_text.bits()
    b_text.extend([0]*(16*8 - len(b_text)))
    return b_text

def vector_to_bytes(vec):
    res = 0
    for x in vec[::-1]:
        res = (res << 1) | int(x)
    return int(res).to_bytes(16, 'big')

if __name__ == '__main__':
    flag_ct = get_flag()
    zero_ct = encrypt(b'\0'*16)[:16]

    M = []
    for i in range(16*8):
        data = int(1<<i).to_bytes(16, 'big')
        M.append(bytes_to_vector(xor_bytes(zero_ct, encrypt(data)[:16])))
    M = matrix(F, M)

    flag_ct_blocks = [bytes_to_vector(xor_bytes(zero_ct, flag_ct[i:i+16])) for i in range(0, len(flag_ct), 16)]
    res_blocks = []
    for block in flag_ct_blocks:
        v = vector(F, block)
        res_blocks.append(vector_to_bytes(M.solve_left(v)))
    print(b''.join(res_blocks))