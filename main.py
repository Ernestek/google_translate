import os

from img_translate import save_txt, get_translated_text_on_pic
from pic_translate_selenium import PicGoogleTranslateParser

PROJECT_ID = 'img-translate-397007'

def main(folder_path):
    target_language_code = 'en'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            filename_format = filename.split('.')[1]
            if filename_format in ('png', 'jpg', 'jpeg'):
                # Start translate picture to txt
                save_txt(filename,
                         get_translated_text_on_pic(
                             file=filename,
                             project_id=PROJECT_ID,
                             target_language_code=target_language_code,
                         ))
                # Start translate picture to picture
                with PicGoogleTranslateParser() as placer:
                    placer.placer_google_translate_parser(filename)

            else:
                return 'Not supported format file'
    return 'Translated'



import tkinter as tk
from tkinter import filedialog

# from main import main


def start_processing():
    source_path = source_entry.get()
    destination_path = destination_entry.get()

    # Здесь можно добавить код для обработки файлов из source_path и сохранения в destination_path
    print(source_path)
    response = main(source_path)
    # print(destination_path)
    # Например, можно скопировать файлы из source_path в destination_path

    result_label.config(text=response)


def browse_source_path():
    path = filedialog.askdirectory()
    # path = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
    source_entry.delete(0, tk.END)
    source_entry.insert(0, path)


def browse_destination_path():
    path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, path)


# Создание главного окна
root = tk.Tk()
root.title("Picture Translator")
root.geometry("600x300")  # Задание размера окна

# Создание и размещение виджетов
source_label = tk.Label(root, text="Source path:")
source_label.pack()

source_entry = tk.Entry(root)
source_entry.pack()

source_browse_button = tk.Button(root, text="path...", command=browse_source_path)
source_browse_button.pack()

destination_label = tk.Label(root, text="Destination path:")
destination_label.pack()

destination_entry = tk.Entry(root)
destination_entry.pack()

destination_browse_button = tk.Button(root, text="path...", command=browse_destination_path)
destination_browse_button.pack()

start_button = tk.Button(root, text="Start", command=start_processing)
start_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Запуск главного цикла обработки событий
root.mainloop()