import sys  # Модуль для работы с аргументами командной строки и завершения программы
import os  # Модуль для работы с файловой системой (проверка существования файла, чтение/запись)
from typing import List, Tuple, Optional  # Типы для аннотаций, улучшающих читаемость и проверку кода

class TextEditor:
    def __init__(self, file_path: str):
        # Инициализация редактора
        self.file_path = file_path  # Путь к файлу, с которым работает редактор
        self.lines: List[str] = []  # Список строк файла, хранящий текущее содержимое в памяти
        self.history: List[Tuple[str, List[str]]] = []  # История операций для команды undo (команда, состояние строк)
        self.load_file()  # Загружаем файл при создании объекта

    def load_file(self) -> None:
        """Загружает содержимое файла в память."""
        try:
            # Проверяем, существует ли файл
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    # Читаем файл и разбиваем на строки, убирая символы новой строки
                    self.lines = f.read().splitlines()
                    # Если файл пустой, инициализируем одной пустой строкой
                    if not self.lines:
                        self.lines = [""]
            else:
                # Если файла нет, создаем пустой список с одной пустой строкой
                self.lines = [""]
        except Exception as e:
            # Обрабатываем ошибки чтения файла и выводим сообщение
            print(f"Ошибка при загрузке файла: {e}")
            self.lines = [""]

    def save_file(self) -> None:
        """Сохраняет содержимое в файл."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # Записываем строки, соединяя их символом новой строки
                f.write("\n".join(self.lines))
                # Добавляем новую строку в конец, если последняя строка не пустая
                if self.lines and self.lines[-1]:
                    f.write("\n")
            print("Файл сохранен.")
        except Exception as e:
            # Обрабатываем ошибки записи файла и выводим сообщение
            print(f"Ошибка при сохранении файла: {e}")

    def save_to_history(self, command: str) -> None:
        """Сохраняет текущее состояние в историю для возможности отмены."""
        # Сохраняем команду и копию текущего списка строк
        self.history.append((command, self.lines.copy()))

    def insert(self, text: str, row: Optional[int] = None, col: Optional[int] = None) -> None:
        """Вставляет текст в указанную позицию, добавляя пустые строки и пробелы при необходимости."""
        self.save_to_history("insert")  # Сохраняем состояние перед изменением
        # Если номер строки не указан, вставляем в конец файла
        if row is None:
            row = len(self.lines)
        else:
            row -= 1  # Преобразуем пользовательский номер строки (с 1) в индекс (с 0)
        # Проверяем, что номер строки не отрицательный
        if row < 0:
            print(f"Ошибка: Номер строки {row + 1} вне диапазона.")
            self.history.pop()  # Удаляем историю, так как операция не выполнена
            return

        # Добавляем пустые строки, если указанный номер строки превышает текущую длину
        while row >= len(self.lines):
            self.lines.append("")

        current_line = self.lines[row]  # Текущая строка для вставки
        # Если позиция курсора не указана, вставляем в конец строки
        if col is None:
            col = len(current_line)
        # Проверяем, что позиция курсора не отрицательная
        if col < 0:
            print(f"Ошибка: Позиция {col} вне строки.")
            self.history.pop()  # Удаляем историю, так как операция не выполнена
            return

        # Если позиция курсора превышает длину строки, добавляем пробелы
        if col > len(current_line):
            current_line += " " * (col - len(current_line))
            self.lines[row] = current_line

        # Вставляем текст в указанную позицию
        self.lines[row] = current_line[:col] + text + current_line[col:]

    def delete_all(self) -> None:
        """Удаляет все содержимое файла."""
        self.save_to_history("del")  # Сохраняем состояние перед удалением
        # Заменяем содержимое одной пустой строкой
        self.lines = [""]

    def delete_row(self, row: int) -> None:
        """Удаляет указанную строку."""
        row -= 1  # Преобразуем пользовательский номер строки (с 1) в индекс (с 0)
        # Проверяем, что номер строки в допустимом диапазоне
        if row < 0 or row >= len(self.lines):
            print(f"Ошибка: Номер строки {row + 1} вне диапазона.")
            return
        self.save_to_history("delrow")  # Сохраняем состояние перед удалением
        self.lines.pop(row)  # Удаляем строку
        # Если файл стал пустым, добавляем одну пустую строку
        if not self.lines:
            self.lines = [""]

    def swap_rows(self, row1: int, row2: int) -> None:
        """Меняет местами две строки."""
        row1 -= 1  # Преобразуем пользовательский номер строки (с 1) в индекс (с 0)
        row2 -= 1  # Преобразуем пользовательский номер строки (с 1) в индекс (с 0)
        # Проверяем, что номера строк в допустимом диапазоне
        if row1 < 0 or row1 >= len(self.lines) or row2 < 0 or row2 >= len(self.lines):
            print(f"Ошибка: Номера строк {row1 + 1} или {row2 + 1} вне диапазона.")
            return
        # Проверяем, что строки не совпадают
        if row1 == row2:
            print("Ошибка: Номера строк совпадают.")
            return
        self.save_to_history("swap")  # Сохраняем состояние перед обменом
        # Меняем строки местами
        self.lines[row1], self.lines[row2] = self.lines[row2], self.lines[row1]

    def undo(self) -> None:
        """Отменяет последнюю операцию."""
        # Проверяем, есть ли операции в истории
        if not self.history:
            print("Нет операций для отмены.")
            return
        # Восстанавливаем предыдущее состояние строк
        self.lines = self.history.pop()[1]
        print("Последняя операция отменена.")

    def process_command(self, command: str) -> bool:
        """Обрабатывает введенную команду."""
        parts = command.strip().split()  # Разбиваем команду на части
        if not parts:
            return True  # Пустая команда, продолжаем цикл

        cmd = parts[0].lower()  # Приводим команду к нижнему регистру
        try:
            if cmd == "insert":
                # Проверяем, что текст заключен в кавычки
                if len(parts) < 2 or parts[1][0] != '"' or parts[1][-1] != '"':
                    print('Ошибка: Текст должен быть в двойных кавычках.')
                    return True
                text = parts[1][1:-1]  # Извлекаем текст без кавычек
                # Получаем номер строки и позицию курсора, если указаны
                row = int(parts[2]) if len(parts) > 2 else None
                col = int(parts[3]) if len(parts) > 3 else None
                self.insert(text, row, col)  # Выполняем вставку
            elif cmd == "del":
                self.delete_all()  # Удаляем все содержимое
            elif cmd == "delrow":
                # Проверяем, что указан номер строки
                if len(parts) < 2:
                    print("Ошибка: Укажите номер строки.")
                    return True
                self.delete_row(int(parts[1]))  # Удаляем строку
            elif cmd == "swap":
                # Проверяем, что указаны два номера строк
                if len(parts) < 3:
                    print("Ошибка: Укажите два номера строк.")
                    return True
                self.swap_rows(int(parts[1]), int(parts[2]))  # Меняем строки
            elif cmd == "undo":
                self.undo()  # Отменяем последнюю операцию
            elif cmd == "save":
                self.save_file()  # Сохраняем файл
            elif cmd == "exit":
                return False  # Завершаем цикл обработки команд
            else:
                print(f"Неизвестная команда: {cmd}")  # Неизвестная команда
        except ValueError:
            # Обрабатываем ошибки преобразования аргументов (например, не числа)
            print("Ошибка: Неверный формат аргументов.")
        except Exception as e:
            # Обрабатываем прочие ошибки
            print(f"Ошибка: {e}")
        return True  # Продолжаем цикл обработки команд

def main():
    # Проверяем, что передан ровно один аргумент (путь к файлу)
    if len(sys.argv) != 2:
        print("Использование: python text_editor.py <file_path>")
        sys.exit(1)  # Завершаем программу с ошибкой

    editor = TextEditor(sys.argv[1])  # Создаем объект редактора
    print("Введите команды (exit для выхода):")
    while True:
        command = input("> ")  # Запрашиваем команду у пользователя
        # Обрабатываем команду, прекращаем цикл при exit
        if not editor.process_command(command):
            break

if __name__ == "__main__":
    main()  # Запускаем основную функцию программы