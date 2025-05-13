# splitter.py
from datetime import timedelta  # Импортируем timedelta для вычислений с временем

def split_data(data, interval_minutes=5):
    """
    Разбивает данные на интервалы указанной длительности.

    Аргументы:
    - data: список кортежей (datetime, значение)
    - interval_minutes: продолжительность интервала в минутах (по умолчанию 5)

    Возвращает:
    - список списков, каждый из которых содержит данные одного временного отрезка
    """
    if not data:
        return []  # Если входной список пуст, возвращаем пустой список интервалов

    data.sort(key=lambda x: x[0])  # Сортируем данные по времени (первый элемент кортежа)
    intervals = []  # Список для хранения всех интервалов
    start_time = data[0][0]  # Начальное время первого интервала
    end_time = start_time + timedelta(minutes=interval_minutes)  # Конечное время первого интервала
    current_chunk = []  # Текущий интервал, который заполняется

    for dt, value in data:
        if dt < end_time:
            current_chunk.append((dt, value))  # Добавляем в текущий интервал, если не вышло за пределы
        else:
            intervals.append(current_chunk)  # Сохраняем завершенный интервал
            current_chunk = [(dt, value)]  # Начинаем новый интервал с текущего значения
            start_time = dt  # Обновляем начало интервала
            end_time = start_time + timedelta(minutes=interval_minutes)  # И конец интервала

    if current_chunk:
        intervals.append(current_chunk)  # Добавляем последний непустой интервал

    return intervals  # Возвращаем список интервалов
