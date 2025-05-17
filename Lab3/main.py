#!/usr/bin/python3

import ctypes

# Загрузка библиотеки calculate_primes.dll
try:
    lib = ctypes.CDLL('./calculate_primes.dll')
except OSError as e:
    print(f"Ошибка загрузки calculate_primes.dll: {e}")
    exit(1)

# Определение сигнатуры функции calculate_primes
# void calculate_primes(int primes[], int n)
lib.calculate_primes.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.calculate_primes.restype = None

def main():
    # Ввод двух чётных чисел n и m
    print("Введите два четных числа n и m (4 <= n < m < 10 000 000):")
    try:
        n, m = map(int, input().split())
    except ValueError:
        print("Ошибка: введите два целых числа.")
        return

    # Проверка корректности ввода
    if not (4 <= n < m < 10_000_000):
        print("Ошибка: числа должны удовлетворять условию 4 <= n < m < 10 000 000.")
        return

    # Если n нечётное, увеличиваем до ближайшего чётного
    if n % 2 != 0:
        n += 1

    # Создание массива для простых чисел
    primes = (ctypes.c_int * (m + 1))()  # Массив размером m+1, инициализирован нулями
    # Вызов функции calculate_primes для заполнения массива
    lib.calculate_primes(primes, m)

    # Перебор всех чётных чисел k в диапазоне от n до m
    for k in range(n, m + 1, 2):
        count = 0  # Счётчик пар простых чисел
        first_x = 0  # Первое простое число в паре
        first_y = 0  # Второе простое число в паре

        # Перебор чисел x от 2 до k/2
        for x in range(2, k // 2 + 1):
            if primes[x] and primes[k - x]:  # Если x и k-x простые
                count += 1
                if count == 1:  # Сохраняем первую пару
                    first_x = x
                    first_y = k - x

        # Вывод результата, если найдены пары
        if count > 0:
            print(f"{k} {count} {first_x} {first_y}")

if __name__ == "__main__":
    main()

# Комментарии к логике программы:
# 1) Программа запрашивает два числа n и m от пользователя.
# 2) Проверяется, что 4 <= n < m < 10 000 000.
# 3) Если n нечётное, оно увеличивается до ближайшего чётного.
# 4) Создаётся массив ctypes для хранения индикаторов простых чисел.
# 5) Функция calculate_primes из calculate_primes.dll заполняет массив primes.
# 6) Для каждого чётного k от n до m:
#    - Перебираются x от 2 до k/2.
#    - Если x и k-x простые (primes[x] и primes[k-x] равны 1), увеличивается счётчик.
#    - Первая найденная пара сохраняется в first_x и first_y.
#    - Если пары найдены, выводится строка: k count first_x first_y.
# 7) Перебор до k/2 предотвращает дублирование пар (например, 3+7 и 7+3 для k=10).