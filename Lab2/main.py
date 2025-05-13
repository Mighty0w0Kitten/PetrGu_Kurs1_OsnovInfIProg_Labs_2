# lab2_statistics_app/main.py

# Импорт необходимых библиотек
import csv  # Для чтения CSV-файлов
from datetime import datetime, timedelta  # Для работы с датами и интервалами времени
import statistics  # Для расчета статистических характеристик
import sys  # Для получения аргументов командной строки
from splitter import split_data  # Импорт функции разбиения интервалов из внешнего модуля

# ======= ФУНКЦИЯ СЧИТЫВАНИЯ ДАННЫХ ИЗ CSV-ФАЙЛА =======
def read_data_from_file(filename):
    """
    Считывает данные из CSV-файла и возвращает список кортежей вида:
    [(datetime, value), ...]

    Входной CSV-файл должен содержать:
    - В первом столбце: время в секундах от начала отсчета (тип float)
    - Во втором столбце: числовое значение (тип float)
    """
    data = []  # Инициализация списка для хранения результатов
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)  # Создание CSV-ридера
            for row in reader:
                if len(row) < 2:
                    continue  # Пропустить строку, если в ней меньше двух столбцов
                try:
                    seconds = float(row[0].strip())  # Время в секундах с начала (float)
                    value = float(row[1].strip())  # Значение (float)
                    base_time = datetime(2025, 1, 1)  # Начальная точка отсчета — 1 января 2025
                    dt = base_time + timedelta(seconds=seconds)  # Преобразование секунд в datetime
                    data.append((dt, value))  # Добавление пары (время, значение) в список
                except ValueError:
                    continue  # Пропустить строку, если значения некорректны
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")  # Сообщение, если файл не найден
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")  # Общее сообщение об ошибке
    return data  # Возвращаем считанные данные

# ======= ФУНКЦИЯ ВЫЧИСЛЕНИЯ СТАТИСТИК =======
def calculate_statistics(intervals):
    """
    Вычисляет статистические показатели для каждого временного интервала.

    Аргумент:
    - intervals: список списков с парами (datetime, значение)

    Возвращает:
    - список словарей с ключами: start, end, count, mean, mode, median
    """
    stats = []  # Список статистик по каждому интервалу
    for chunk in intervals:
        values = [val for _, val in chunk]  # Извлекаем значения из интервала
        try:
            chunk_stats = {
                "start": chunk[0][0],  # Начальное время интервала
                "end": chunk[-1][0],   # Конечное время интервала
                "count": len(values),  # Количество значений
                "mean": statistics.mean(values),  # Среднее значение
                "mode": statistics.mode(values),  # Мода (наиболее частое значение)
                "median": statistics.median(values)  # Медиана
            }
        except statistics.StatisticsError:
            # Обработка ошибки, если мода не может быть определена (несколько одинаково частых значений)
            chunk_stats = {
                "start": chunk[0][0],
                "end": chunk[-1][0],
                "count": len(values),
                "mean": statistics.mean(values),
                "mode": None,
                "median": statistics.median(values)
            }
        stats.append(chunk_stats)  # Добавление результатов в общий список
    return stats

# ======= ФУНКЦИЯ ВЫВОДА РЕЗУЛЬТАТОВ НА ЭКРАН =======
def print_statistics(stats):
    """
    Выводит статистику по каждому временному интервалу в удобочитаемом виде.

    Аргумент:
    - stats: список словарей со статистическими данными
    """
    for i, s in enumerate(stats):  # Перебираем все интервалы
        print(f"Интервал {i + 1} ({s['start']} - {s['end']}):")
        print(f"  Кол-во значений: {s['count']}")
        print(f"  Среднее значение: {s['mean']:.2f}")
        print(f"  Мода: {s['mode'] if s['mode'] is not None else 'Не определена'}")
        print(f"  Медиана: {s['median']:.2f}")
        print()  # Пустая строка между интервалами

# ======= ОСНОВНАЯ ТОЧКА ВХОДА =======
if __name__ == "__main__":
    # Проверяем наличие аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование: python main.py <имя_файла> [интервал_в_минутах]")
        sys.exit(1)  # Завершаем выполнение, если нет обязательного аргумента

    filename = sys.argv[1]  # Получаем имя файла из аргумента
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # Интервал разбиения (по умолчанию 5 минут)

    # Последовательность шагов:
    data = read_data_from_file(filename)  # Считываем и преобразуем данные
    intervals = split_data(data, interval_minutes=interval)  # Делим данные по времени
    stats = calculate_statistics(intervals)  # Расчёт статистик для каждого интервала
    print_statistics(stats)  # Вывод статистик на экран
