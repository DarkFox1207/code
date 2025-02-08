import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class CustomTerminal:
    def __init__(self, master):
        self.master = master
        self.master.title("Терминал")
        self.master.geometry("700x500")
        self.current_path = os.getcwd()  # Текущая директория

        # Текстовое поле для отображения результатов
        self.output_area = ScrolledText(self.master, wrap=tk.WORD, state="normal")
        self.output_area.pack(fill="both", expand=True, padx=5, pady=5)
        self.output_area.insert(tk.END, f"Текущая директория: {self.current_path}\n")
        self.output_area.see(tk.END)

        # Ввод команд
        self.command_entry = ttk.Entry(self.master)
        self.command_entry.pack(fill="x", padx=5, pady=5)
        self.command_entry.bind("<Return>", self.run_command)  # Обработчик Enter

    def run_command(self, event=None):
        command = self.command_entry.get().strip()
        if not command:
            return

        self.output_area.insert(tk.END, f"> {command}\n", "command")

        # Парсинг команды
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd == "ls":
                self.list_directory()
            elif cmd == "cd":
                if args:
                    self.change_directory(args[0])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите путь для перехода.\n", "error")
            elif cmd == "mkdir":
                if args:
                    self.create_directory(args[0])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите имя папки.\n", "error")
            elif cmd == "rm":
                if args:
                    self.remove_item(args[0])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите имя файла или папки.\n", "error")
            elif cmd == "ipconfig":
                self.run_system_command("ipconfig")
            elif cmd == "ping":
                if args:
                    self.run_system_command(f"ping {args[0]}")
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите адрес для пинга.\n", "error")
            elif cmd == "copy":
                if len(args) == 2:
                    self.copy_item(args[0], args[1])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите источник и цель.\n", "error")
            elif cmd == "move":
                if len(args) == 2:
                    self.move_item(args[0], args[1])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите источник и цель.\n", "error")
            elif cmd == "type":
                if args:
                    self.view_file_content(args[0])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите имя файла.\n", "error")
            elif cmd == "touch":
                if args:
                    self.create_empty_file(args[0])
                else:
                    self.output_area.insert(tk.END, "Ошибка: укажите имя файла.\n", "error")
            elif cmd == "help":
                self.display_help()
            else:
                self.output_area.insert(tk.END, "Неизвестная команда.\n", "error")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

        self.output_area.see(tk.END)
        self.command_entry.delete(0, tk.END)

    def list_directory(self):
        """Выводит список файлов и папок в текущей директории."""
        try:
            items = os.listdir(self.current_path)
            for item in items:
                self.output_area.insert(tk.END, f"{item}\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def change_directory(self, path):
        """Переходит в указанную директорию."""
        try:
            os.chdir(path)
            self.current_path = os.getcwd()
            self.output_area.insert(tk.END, f"Текущая директория: {self.current_path}\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def create_directory(self, name):
        """Создает папку."""
        try:
            os.makedirs(os.path.join(self.current_path, name))
            self.output_area.insert(tk.END, f"Папка {name} создана.\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def remove_item(self, name):
        """Удаляет файл или папку."""
        try:
            path = os.path.join(self.current_path, name)
            if os.path.isdir(path):
                os.rmdir(path)
                self.output_area.insert(tk.END, f"Папка {name} удалена.\n", "output")
            elif os.path.isfile(path):
                os.remove(path)
                self.output_area.insert(tk.END, f"Файл {name} удален.\n", "output")
            else:
                self.output_area.insert(tk.END, f"{name} не найден.\n", "error")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def run_system_command(self, command):
        """Выполняет системную команду."""
        try:
            # Устанавливаем кодировку UTF-8
            command = f'chcp 65001 >nul & {command}'
            result = subprocess.run(command, shell=True, text=True, capture_output=True, encoding="utf-8")
            if result.stdout:
                self.output_area.insert(tk.END, result.stdout, "output")
            if result.stderr:
                self.output_area.insert(tk.END, result.stderr, "error")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def copy_item(self, source, target):
        """Копирует файл."""
        try:
            subprocess.run(f'copy "{source}" "{target}"', shell=True, text=True)
            self.output_area.insert(tk.END, f"Файл {source} скопирован в {target}.\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def move_item(self, source, target):
        """Перемещает файл."""
        try:
            subprocess.run(f'move "{source}" "{target}"', shell=True, text=True)
            self.output_area.insert(tk.END, f"Файл {source} перемещен в {target}.\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def view_file_content(self, filename):
        """Просмотр содержимого файла."""
        try:
            path = os.path.join(self.current_path, filename)
            with open(path, 'r') as file:
                content = file.read()
                self.output_area.insert(tk.END, f"{content}\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def create_empty_file(self, filename):
        """Создание пустого файла."""
        try:
            path = os.path.join(self.current_path, filename)
            with open(path, 'w', encoding='utf-8') as file:
                pass
            self.output_area.insert(tk.END, f"Файл {filename} создан.\n", "output")
        except Exception as e:
            self.output_area.insert(tk.END, f"Ошибка: {e}\n", "error")

    def display_help(self):
        """Выводит список доступных команд."""
        commands = [
            "ls - просмотр файлов в текущей директории",
            "cd <путь> - переход в указанную директорию",
            "mkdir <имя> - создание новой папки",
            "rm <имя> - удаление файла или папки",
            "ipconfig - просмотр конфигурации сети",
            "ping <адрес> - проверка доступности сети",
            "copy <источник> <цель> - копирование файла",
            "move <источник> <цель> - перемещение файла",
            "type <имя_файла> - просмотр содержимого текстового файла",
            "touch <имя_файла> - создание пустого файла",
            "help - отображение списка доступных команд"
        ]
        self.output_area.insert(tk.END, "Доступные команды:\n", "output")
        for cmd in commands:
            self.output_area.insert(tk.END, f"{cmd}\n", "output")


def launch_terminal():
    terminal_window = tk.Toplevel()
    CustomTerminal(terminal_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomTerminal(root)
    root.mainloop()
