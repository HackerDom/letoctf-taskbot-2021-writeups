from utils import text_to_blocks, blocks_to_text, pad, unpad, xor_bytes

S = [32, 13, 30, 55, 42, 35, 44, 57, 0, 45, 39, 49, 15, 52, 12, 59, 8, 38, 46, 4, 33, 48, 16, 27, 31, 21, 29, 40, 36, 11, 18, 47, 1, 60, 7, 14, 26, 43, 28, 6, 54, 2, 51, 61, 19, 58, 50, 37, 41, 23, 9, 56, 62, 63, 3, 17, 5, 24, 10, 53, 25, 22, 20, 34]
P = [36, 6, 20, 59, 1, 10, 45, 33, 58, 27, 24, 19, 41, 40, 23, 9, 17, 43, 51, 5, 21, 29, 18, 14, 12, 39, 0, 32, 46, 35, 54, 42, 22, 34, 57, 60, 44, 48, 4, 53, 16, 61, 3, 47, 50, 25, 30, 38, 31, 56, 15, 28, 37, 13, 55, 8, 62, 7, 52, 49, 63, 2, 26, 11]
S_INV = [S.index(i) for i in range(len(S))]
P_INV = [P.index(i) for i in range(len(P))]

BLOCK_SIZE = (len(S) // 8) * 2
ROUNDS = 7


class Feistel:
    def __init__(self, key):
        self._rounds = ROUNDS
        self._block_size = BLOCK_SIZE
        self._keys = self._expand_key(key)

    def _expand_key(self, key):
        keys = [key]
        for _  in range(self._rounds-1):
            keys.append(keys[-1][-1:] + keys[-1][:-1])
        return keys

    def _perm(self, block):
        i_block = int.from_bytes(block, 'big')
        b_block = list(bin(i_block)[2:].zfill(self._block_size*4))
        b_res = ''.join(b_block[P[i]] for i in range(len(P)))
        i_res = int(b_res, 2)
        return i_res.to_bytes(self._block_size // 2, 'big')

    def _unperm(self, block):
        i_block = int.from_bytes(block, 'big')
        b_block = list(bin(i_block)[2:].zfill(self._block_size * 4))
        b_res = ''.join(b_block[P_INV[i]] for i in range(len(P_INV)))
        i_res = int(b_res, 2)
        return i_res.to_bytes(self._block_size // 2, 'big')

    def _encrypt_block(self, block):
        L, R = block[:self._block_size // 2], block[self._block_size // 2:]
        for i in range(self._rounds):
            L, R = R, xor_bytes(self._perm(xor_bytes(L, self._keys[i])), R)
        return R + L

    def _decrypt_block(self, block):
        R, L = block[:self._block_size // 2], block[self._block_size // 2:]
        for i in range(self._rounds):
            R, L = L, xor_bytes(self._unperm(xor_bytes(R, L)), self._keys[self._rounds - i - 1])
        return L + R

    def encrypt(self, pt):
        pt_blocks = text_to_blocks(pad(pt, self._block_size), self._block_size)
        ct_blocks = [self._encrypt_block(block) for block in pt_blocks]
        return blocks_to_text(ct_blocks)

    def decrypt(self, ct):
        ct_blocks = text_to_blocks(ct, self._block_size)
        pt_blocks = [self._decrypt_block(block) for block in ct_blocks]
        return unpad(blocks_to_text(pt_blocks))

if __name__ == '__main__':
    pt = b'Hello there! This is our testing information'
    cipher = Feistel(b'Pr3s5_F_')
    ct = cipher.encrypt(pt)
    print(cipher.decrypt(ct) == pt)