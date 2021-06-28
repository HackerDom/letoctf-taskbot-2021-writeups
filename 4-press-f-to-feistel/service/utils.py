def xor_bytes(a, b):
    return bytes([x^y for x,y in zip(a, b)])

def text_to_blocks(text, block_size):
    return [text[i: i+block_size] for i in range(0, len(text), block_size)]

def blocks_to_text(blocks):
    return b''.join(blocks)

def pad(text, block_size):
    b = (-len(text)) % block_size
    b = b if b else block_size
    return text + bytes([b]*b)

def unpad(text):
    return text[:-text[-1]]