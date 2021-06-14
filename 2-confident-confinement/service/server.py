#!/usr/bin/env python3.8

import sys
import string


def main():
    enabled = string.ascii_lowercase + string.punctuation + string.whitespace
    disabled = '+-*/%&|^~<>="\'(){}, '
    alphabet = set(enabled) - set(disabled)

    max_length = 400
    
    print(f'len(alphabet) == {len(alphabet)}')
    print(sys.version)

    code = input('>>> ')

    if len(code) > max_length or any(char not in alphabet for char in code):
        print('Bad code :(')
        return

    try:
        exec(code, {'__builtins__': {}})
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
