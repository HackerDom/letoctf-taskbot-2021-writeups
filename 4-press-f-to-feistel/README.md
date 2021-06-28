# LetoCTF Taskbot 2021 | press-f-to-feistel

Автор: [1MiKHalyCH1](https://github.com/1MiKHalyCH1)

## Описание

> Самая стандартная (правда самописная) система шифрования. Сможешь достать флаг?
> 
> `/api/encrypt` - ручка для шифрования. Отправляйте POST-запросы<br><br>
> `http://press-f-to-feistel.hdcourse.ru/api/get_flag`

## Файлы

- [press-f-to-feistel.zip](static/press-f-to-feistel.zip)

## Решение

Дана криптосистема на основе [сети Фейстеля](https://en.wikipedia.org/wiki/Feistel_cipher). 

Прочитав код, можно понять, что S-box в нём вообще не используется. Это значит, что система шифрования линейная. То есть любой `ct` можно выразить в виде комбинации pt:

`pt1 ^ pt2 = ct1 ^ ct2`

1) Построим базисные вектора. Для этого зашифруем нолики, а потом единичку на каждом из возможных мест. Получим базисные вектора:

`basis[i] = E(0..1(на i-ом месте)..0) ^ E(0..0)`

2) Построим из них "диагональную" матрицу (т.е. для `I` построим `A = E(I) ^ E(0)`, где i-ая строчка:

```
A[i] = (E(I)^E(0))[i] = E(I[i]) ^ E(0) = basis[i]
```

3) Для каждого блока флага решим:
```
A = E(I)^E(0), b = flag_block, c = E(flag_block) ^ E(0)

bA = c => A.solve_left(c) = b
```

4) Напечатаем флаг

5) ...

6) PROFIT!

## Статика

[feistel.py](static/press-f-to-feistel/feistel.py) - файл с реализацией Фейстеля

## Флаг

`LetoCTF{F3i5TeL_w1Th0u7_SBOX_1s_n0t_s3cUr3}`
