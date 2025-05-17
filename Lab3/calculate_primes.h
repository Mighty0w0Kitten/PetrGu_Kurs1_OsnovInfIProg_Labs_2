#ifndef CALCULATE_PRIMES_H
#define CALCULATE_PRIMES_H

/* Объявление функции calculate_primes */
void calculate_primes(int primes[], int n);

#endif // CALCULATE_PRIMES_H

/*Основная задача calculate_primes.h
	Объявление функции calculate_primes: Заголовочный файл содержит прототип функции calculate_primes,
	чтобы её можно было использовать в других файлах, например, в primes.c.

	void calculate_primes(int primes[], int n);
	этот код говорит компилятору:
	-Функция calculate_primes существует.
	-Она принимает массив индикаторов простых чисел (int primes[]) и целое число n.
	-Функция не возвращает значение (void).

	Без этого объявления компилятор не будет знать о функции,
	определённой в другом файле (calculate_primes.c), и выдаст ошибку.

*/