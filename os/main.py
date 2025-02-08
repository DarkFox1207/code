import os
import shutil
import psutil
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinterdnd2 import TkinterDnD, DND_FILES, DND_ALL
import logging
from datetime import datetime
import GPUtil
from terminal import launch_terminal

# Путь к корневой папке
base_path = r"C:\Users\Pavel\Desktop\code\os\superapp"

# Путь для сохранения логов
log_directory = r"C:\Users\Pavel\Desktop\code\os"
log_file = os.path.join(log_directory, "log.txt")

# Убедимся, что папка для логов существует
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Настройка логирования
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Функция для логирования
def log_event(event_message):
    logging.info(event_message)

# Папки, которые будем отображать
system_folder = os.path.join(base_path, "System")
recycle_bin_folder = os.path.join(base_path, "Recycle bin")

# Переменные для копирования и вставки
copied_item = None

# Функция для создания папок, если они не существуют
def create_folders():
    if not os.path.exists(system_folder):
        os.makedirs(system_folder)
    if not os.path.exists(recycle_bin_folder):
        os.makedirs(recycle_bin_folder)

# Функция для отображения файловой структуры в дереве
def populate_tree(tree, parent, path):
    """Заполняет дерево файлами и папками"""
    for folder_name in os.listdir(path):
        full_path = os.path.join(path, folder_name)
        is_folder = os.path.isdir(full_path)
        
        # Вставляем в дерево
        node = tree.insert(parent, 'end', text=folder_name, open=False, values=[full_path])
        
        if is_folder:
            populate_tree(tree, node, full_path)

# Функция для вывода информации "О программе"
def show_about():
    messagebox.showinfo("О программе", 
                        "Предмет: Операционные системы и оболочки\n"
                        "Язык программирования: Python\n"
                        "ФИО: Петров Павел Олегович\n"
                        "Группа: ИВТ-34у")

# Функция для вывода информации о горячих клавишах
def show_hotkeys():
    messagebox.showinfo("Горячие клавиши",
                        "1. Ctrl+C - Копировать файл/папку\n"
                        "2. Ctrl+V - Вставить файл/папку\n"
                        "3. Delete - Удалить в корзину\n"
                        "4. Ctrl+S - Создать папку\n"
                        "5. Ctrl+F - Создать файл\n"
                        "6. Ctrl+R - Обновить дерево папок")

# Функция отображения подключенных съемных носителей
def list_removable_drives():
    removable_drives = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            removable_drives.append(partition.device)
    return removable_drives

# Функция для отображения подключенных устройств в виде сообщения
def display_removable_drives():
    drives = list_removable_drives()
    if drives:
        drive_list = "\n".join(drives)
        messagebox.showinfo("Подключенные устройства", f"Подключенные съемные устройства:\n{drive_list}")
    else:
        messagebox.showinfo("Подключенные устройства", "Нет подключенных съемных устройств.")

# Функция запуска системных утилит
def run_calculator():
    try:
        subprocess.Popen("calc.exe")
        log_event("Калькулятор запущен")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить калькулятор: {e}")

def run_command_prompt():
    try:
        subprocess.Popen("cmd.exe")
        log_event("Командная строка запущена")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить командную строку: {e}")

def run_explorer():
    try:
        subprocess.Popen("explorer.exe")
        log_event("Проводник запущен")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить проводник: {e}")

# Функция копирования
def copy_item(event=None):
    global copied_item
    selected_item = tree.selection()
    if selected_item:
        item_path = tree.item(selected_item[0])['values'][0]  # Получаем полный путь
        # Проверяем, что не выбрана папка "System"
        if item_path == system_folder:
            messagebox.showerror("Ошибка", "Нельзя копировать папку 'System'.")
            return
        copied_item = item_path
        print(f"Скопировано: {copied_item}")

# Функция вставки
def paste_item(event=None):
    global copied_item
    if copied_item:
        selected_item = tree.selection()
        if selected_item:
            target_path = tree.item(selected_item[0])['values'][0]  # Получаем полный путь
            if os.path.isdir(target_path):
                if os.path.isdir(copied_item):
                    # Копируем папку
                    dest_path = os.path.join(target_path, os.path.basename(copied_item))
                    shutil.copytree(copied_item, dest_path)
                else:
                    # Копируем файл
                    shutil.copy(copied_item, target_path)
                print(f"Вставлено: {copied_item} в {target_path}")
                refresh_tree()
            else:
                messagebox.showerror("Ошибка", "Невозможно вставить в выбранный объект.")
        else:
            messagebox.showerror("Ошибка", "Выберите папку для вставки.")
    else:
        messagebox.showerror("Ошибка", "Нет скопированного объекта.")

# Функция удаления в корзину
def delete_to_recycle_bin(event=None):
    selected_item = tree.selection()
    if selected_item:
        item_path = tree.item(selected_item[0])['values'][0]  # Получаем полный путь
        # Проверяем, что не выбрана папка "System"
        if item_path == system_folder:
            messagebox.showerror("Ошибка", "Нельзя удалить папку 'System'.")
            return
        if os.path.exists(item_path):
            # Перемещаем в корзину
            recycle_item_path = os.path.join(recycle_bin_folder, os.path.basename(item_path))
            shutil.move(item_path, recycle_item_path)
            print(f"Удалено в корзину: {os.path.basename(item_path)}")
            refresh_tree()
        else:
            messagebox.showerror("Ошибка", "Файл или папка не найдены.")
    else:
        messagebox.showerror("Ошибка", "Выберите файл или папку для удаления.")

# Функция создания папки
def create_folder(event=None):
    folder_name = askstring("Имя папки", "Введите имя новой папки:")
    if folder_name:
        new_folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Создана папка: {folder_name}")
            refresh_tree()

# Функция создания файла
def create_file(event=None):
    file_name = askstring("Имя файла", "Введите имя нового файла:")
    if file_name:
        new_file_path = os.path.join(base_path, file_name)
        with open(new_file_path, 'w') as f:
            f.write("")
        print(f"Создан файл: {file_name}")
        refresh_tree()

# Функция для обработки drop
def on_drop(event):
    selected_item = tree.selection()
    if selected_item:
        target_path = tree.item(selected_item[0])['values'][0]  # Путь до целевой папки
        dropped_item = event.data
        if os.path.isdir(dropped_item):
            shutil.move(dropped_item, target_path)
            print(f"Перемещено: {dropped_item} в {target_path}")
            refresh_tree()

# Функция для поиска
def search_files():
    search_term = search_entry.get().lower()  # Получаем текст из поля поиска и приводим к нижнему регистру
    tree.delete(*tree.get_children())  # Очищаем дерево
    root_node = tree.insert("", "end", text="superapp", open=True)  # Вставляем корневую папку
    search_in_directory(base_path, root_node, search_term)

# Функция для поиска по директориям
def search_in_directory(directory, parent, search_term):
    for folder_name in os.listdir(directory):
        full_path = os.path.join(directory, folder_name)
        if search_term in folder_name.lower():  # Проверка, содержится ли поисковый запрос в названии папки/файла
            tree.insert(parent, 'end', text=folder_name, values=[full_path])
        if os.path.isdir(full_path):
            search_in_directory(full_path, parent, search_term)  # Рекурсивно ищем в подкаталогах

# Функция для отображения информации о видеокарте
def show_gpu_info():
    gpu_info = ""
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            gpu_info = "Видеокарты не найдены."
        else:
            for gpu in gpus:
                gpu_info += (
                    f"Имя: {gpu.name}\n"
                    f"Нагрузка: {gpu.load * 100:.2f}%\n"
                    f"Свободная память: {gpu.memoryFree:.2f} МБ\n"
                    f"Занятая память: {gpu.memoryUsed:.2f} МБ\n"
                    f"Общая память: {gpu.memoryTotal:.2f} МБ\n"
                    f"Температура: {gpu.temperature:.2f}°C\n"
                    f"UUID: {gpu.uuid}\n\n"
                )
    except Exception as e:
        gpu_info = f"Ошибка при получении информации о видеокарте: {e}"
    messagebox.showinfo("Информация о видеокарте", gpu_info)
    log_event("Просмотр информации о видеокарте")

# Функция для отображения списка процессов и пользователей
def show_user_processes():
    # Создаем окно
    process_window = tk.Toplevel(root)
    process_window.title("Процессы и пользователи")
    process_window.geometry("600x400")
    
    # Создаем таблицу с использованием Treeview
    columns = ("PID", "Процесс", "Пользователь")
    tree = ttk.Treeview(process_window, columns=columns, show="headings")
    
    # Определяем заголовки и размеры столбцов
    tree.heading("PID", text="PID")
    tree.heading("Процесс", text="Процесс")
    tree.heading("Пользователь", text="Пользователь")
    tree.column("PID", width=80, anchor="center")
    tree.column("Процесс", width=250, anchor="w")
    tree.column("Пользователь", width=150, anchor="center")
    
    # Прокрутка для таблицы
    scrollbar = ttk.Scrollbar(process_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    
    # Заполняем таблицу данными
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            pid = proc.info['pid']
            name = proc.info['name']
            username = proc.info['username'] or "root"  # Заменяем None на "root"
            tree.insert("", "end", values=(pid, name, username))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")
    
    log_event("Просмотр списка процессов и пользователей")

# Функция для отображения информации о процессоре
def show_cpu_info():
    cpu_info = ""
    try:
        cpu_info += f"Процессор: {psutil.cpu_count(logical=True)} ядер (логических)\n"
        cpu_info += f"Физические ядра: {psutil.cpu_count(logical=False)}\n"
        cpu_info += f"Частота процессора: {psutil.cpu_freq().current:.2f} МГц\n"
        cpu_info += f"Загрузка процессора: {psutil.cpu_percent(interval=1)}%\n"
    except Exception as e:
        cpu_info = f"Ошибка при получении информации о процессоре: {e}"
    messagebox.showinfo("Информация о процессоре", cpu_info)
    log_event("Просмотр информации о процессоре")

# Функция обновления дерева
def refresh_tree(event=None):
    tree.delete(*tree.get_children())  # Очищаем дерево
    # Добавляем корневую папку снова, чтобы избежать ошибок с удалением root_node
    root_node = tree.insert("", "end", text="superapp", open=True)
    populate_tree(tree, root_node, base_path)  # Заполняем заново

# Создаем графическое окно с поддержкой Drag and Drop
root = TkinterDnD.Tk()
root.title("Superapp")
root.geometry("1024x720")

# Создаем меню
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Создаем меню «О программе»
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справка", menu=help_menu)
help_menu.add_command(label="О программе", command=show_about)
help_menu.add_command(label="Горячие клавиши", command=show_hotkeys)

# Меню "Инструменты"
tools_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Инструменты", menu=tools_menu)

# Подменю "Устройства" для отображения подключенных съемных устройств
tools_menu.add_command(label="Устройства", command=display_removable_drives)

# Подменю "Утилиты"
utilities_menu = tk.Menu(tools_menu, tearoff=0)
tools_menu.add_cascade(label="Утилиты", menu=utilities_menu)
utilities_menu.add_command(label="Калькулятор", command=run_calculator)
utilities_menu.add_command(label="Проводник", command=run_explorer)
utilities_menu.add_command(label="Командная строка", command=run_command_prompt)
utilities_menu.add_command(label="Терминал", command=launch_terminal)

# Меню "Дополнительно"
additional_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Дополнительно", menu=additional_menu)
additional_menu.add_command(label="Видеокарта", command=show_gpu_info)
additional_menu.add_command(label="Пользователь", command=show_user_processes)
additional_menu.add_command(label="Загрузка процессора", command=show_cpu_info)

# Дерево для отображения структуры папок
tree = ttk.Treeview(root, columns=("path"))
tree.pack(fill="both", expand=True)

# Поле для поиска
search_frame = tk.Frame(root)
search_frame.pack(fill="x")
search_label = tk.Label(search_frame, text="Поиск:")
search_label.pack(side="left", padx=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)
search_button = tk.Button(search_frame, text="Поиск", command=search_files)
search_button.pack(side="left", padx=5)

# Добавляем корневую папку
root_node = tree.insert("", "end", text="superapp", open=True)

# Добавляем папки System и Recycle bin
create_folders()  # Создаём папки, если они не существуют
populate_tree(tree, root_node, base_path)

# Привязка горячих клавиш
root.bind("<Control-c>", copy_item)  # Ctrl+C - Копировать
root.bind("<Control-v>", paste_item)  # Ctrl+V - Вставить
root.bind("<Delete>", delete_to_recycle_bin)  # Delete - Удалить в корзину
root.bind("<Control-s>", create_folder)  # Ctrl+S - Создать папку
root.bind("<Control-f>", create_file)  # Ctrl+F - Создать файл
root.bind("<Control-r>", refresh_tree)  # Ctrl+R - Обновить дерево папок

# Устанавливаем функцию на drop
tree.drop_target_register(DND_FILES)  # Убираем файлы и папки как таргет для drag & drop
tree.dnd_bind('<<Drop>>', on_drop)

# Запуск основного цикла приложения
root.mainloop()
