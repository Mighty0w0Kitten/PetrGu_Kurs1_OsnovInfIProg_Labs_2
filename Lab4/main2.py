import tkinter as tk  # Импорт библиотеки tkinter для создания графического интерфейса
from tkinter import filedialog, messagebox, scrolledtext  # Импорт дополнительных модулей tkinter для диалогов, сообщений и прокручиваемого текста
import json  # Импорт модуля json для работы с JSON файлами
import os  # Импорт модуля os для проверки существования файлов

class JSONEditor:
    def __init__(self, root):
        # Конструктор класса, инициализирует главное окно приложения
        self.root = root  # Сохраняем ссылку на главное окно tkinter
        self.root.title("JSON Editor")  # Устанавливаем заголовок окна
        self.root.geometry("800x600")  # Задаем размер окна 800x600 пикселей

        # Создаем фрейм (контейнер) для поля ввода пути к файлу и кнопки обзора
        self.path_frame = tk.Frame(self.root)
        self.path_frame.pack(pady=10, padx=10, fill=tk.X)  # Размещаем фрейм с отступами и растягиванием по горизонтали

        # Метка с текстом "Путь к файлу JSON:"
        self.path_label = tk.Label(self.path_frame, text="Путь к файлу JSON:")
        self.path_label.pack(side=tk.LEFT)  # Размещаем метку слева внутри фрейма

        # Поле ввода для пути к файлу
        self.path_entry = tk.Entry(self.path_frame)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)  # Размещаем поле ввода слева, растягивая по ширине

        # Кнопка "Обзор" для выбора файла через диалоговое окно
        self.browse_button = tk.Button(self.path_frame, text="Обзор", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT)  # Размещаем кнопку справа от поля ввода

        # Прокручиваемое текстовое поле для отображения и редактирования JSON
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=25)
        # wrap=tk.WORD - перенос слов, height=25 - высота в строках
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)  # Размещаем с отступами, растягивая по ширине и высоте

        # Фрейм для кнопок управления (загрузка, проверка, сохранение)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)  # Размещаем фрейм с отступом сверху

        # Кнопка "Загрузить" для чтения JSON файла
        self.load_button = tk.Button(self.button_frame, text="Загрузить", command=self.load_json)
        self.load_button.pack(side=tk.LEFT, padx=5)  # Размещаем слева с отступом

        # Кнопка "Проверить" для валидации JSON
        self.validate_button = tk.Button(self.button_frame, text="Проверить", command=self.validate_json)
        self.validate_button.pack(side=tk.LEFT, padx=5)  # Размещаем слева с отступом

        # Кнопка "Сохранить" для сохранения JSON
        self.save_button = tk.Button(self.button_frame, text="Сохранить", command=self.save_json)
        self.save_button.pack(side=tk.LEFT, padx=5)  # Размещаем слева с отступом

    def browse_file(self):
        # Метод для выбора JSON файла через диалоговое окно
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        # Открывает диалог выбора файла, фильтруя только .json файлы
        if file_path:  # Если пользователь выбрал файл (не отменил выбор)
            self.path_entry.delete(0, tk.END)  # Очищаем поле ввода
            self.path_entry.insert(0, file_path)  # Вставляем выбранный путь

    def load_json(self):
        # Метод для загрузки и отображения JSON файла
        file_path = self.path_entry.get()  # Получаем путь из поля ввода
        if not file_path:  # Проверяем, не пустое ли поле
            messagebox.showerror("Ошибка", "Укажите путь к файлу!")  # Выводим ошибку
            return

        if not os.path.exists(file_path):  # Проверяем, существует ли файл
            messagebox.showerror("Ошибка", "Файл не существует!")  # Выводим ошибку
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Открываем файл для чтения
                json_data = json.load(file)  # Загружаем JSON в Python объект
                self.text_area.delete(1.0, tk.END)  # Очищаем текстовое поле
                # Форматируем JSON с отступами и вставляем в текстовое поле
                self.text_area.insert(tk.END, json.dumps(json_data, indent=4, ensure_ascii=False))
                # indent=4 - отступы для читаемости, ensure_ascii=False - поддержка не-ASCII символов
        except json.JSONDecodeError:  # Обрабатываем ошибку некорректного JSON
            messagebox.showerror("Ошибка", "Некорректный JSON файл!")
        except Exception as e:  # Обрабатываем другие возможные ошибки
            messagebox.showerror("Ошибка", f"Ошибка при загрузке: {str(e)}")

    def validate_json(self):
        # Метод для проверки корректности JSON в текстовом поле
        try:
            json_text = self.text_area.get(1.0, tk.END)  # Получаем весь текст
            json.loads(json_text)  # Пытаемся разобрать текст как JSON
            messagebox.showinfo("Успех", "JSON корректен!")  # Успех, если нет ошибок
        except json.JSONDecodeError as e:  # Обрабатываем ошибку синтаксиса JSON
            messagebox.showerror("Ошибка", f"Некорректный JSON: {str(e)}")

    def save_json(self):
        # Метод для сохранения отредактированного JSON
        try:
            json_text = self.text_area.get(1.0, tk.END)  # Получаем текст из поля
            json.loads(json_text)  # Проверяем корректность JSON перед сохранением
            # Открываем диалог для выбора пути сохранения
            save_path = filedialog.asksaveasfilename(
                defaultextension=".json",  # Автоматически добавляем .json
                filetypes=[("JSON files", "*.json")]  # Фильтр для .json файлов
            )
            if save_path:  # Если пользователь выбрал путь
                with open(save_path, 'w', encoding='utf-8') as file:  # Открываем файл для записи
                    file.write(json_text)  # Записываем текст
                messagebox.showinfo("Успех", "Файл успешно сохранен!")  # Сообщаем об успехе
        except json.JSONDecodeError:  # Обрабатываем ошибку некорректного JSON
            messagebox.showerror("Ошибка", "Некорректный JSON! Проверьте синтаксис.")
        except Exception as e:  # Обрабатываем другие ошибки
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

if __name__ == "__main__":
    # Точка входа программы
    root = tk.Tk()  # Создаем главное окно приложения
    app = JSONEditor(root)  # Создаем экземпляр редактора
    root.mainloop()  # Запускаем главный цикл обработки событий