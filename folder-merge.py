import inspect
import os
import shutil

while True:
    relative = input("Вы используете относительный или абсолютный путь к папке? [y/n] ")
    if relative == 'y'.replace(' ', ''):
        dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        departure_folder = input("Введите адрес исходной папки: ")
        destination_folder = input("Введите адрес папки: ")
        departure_folder = os.path.join(dirname, departure_folder)
        destination_folder = os.path.join(dirname, destination_folder)
        if os.path.exists(departure_folder) and os.path.exists(destination_folder):
            break
        else:
            print("Какая-то из папок не найдена. Проверьте введенные данные и попробуйте снова.")
    elif relative == 'n'.replace(' ', ''):
        departure_folder = input("Введите адрес исходной папки: ")
        destination_folder = input("Введите адрес папки: ")
        if os.path.exists(departure_folder) and os.path.exists(destination_folder):
            break
        else:
            print("Какая-то из папок не найдена. Проверьте введенные данные и попробуйте снова.")

while True:
    mode = input("Выберите режим: \n"
                 "1 - Совмещение копированием \n"
                 "2 - Совмещение перемещением \n")
    if mode == '1'.replace(' ', ''):
        print("[временное копирование...]", end=' ')
        shutil.copytree(departure_folder, "temp")
        departure_folder = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "temp")
        print("- готово")
        break
    if mode == '2'.replace(' ', ''):
        break

print("[поиск несуществующих файлов...]", end=' ')
set_file = {}
set_folder = {}
for dirname in departure_folder, destination_folder:
    set_file[dirname] = set()
    set_folder[dirname] = set()
    for path, dirs, files in os.walk(dirname):
        set_folder[dirname].update(os.path.join(path, ''.join(os.path.splitext(folder)[:])) for folder in dirs)
        set_file[dirname].update(os.path.join(path, ''.join(os.path.splitext(fn)[:])) for fn in files)
delta = set_file[departure_folder] - set_file[destination_folder]
print('- готово')

print('[процесс перемещения...]', end=' ')
for folder in set_folder[departure_folder]:
    os.makedirs(os.path.join(folder.replace(departure_folder, destination_folder)), exist_ok=True)
for file in delta:
    os.rename(file, file.replace(departure_folder, destination_folder))
print('- готово')
print('[очистка...]', end=' ')
try:
    shutil.rmtree(departure_folder)
except PermissionError:
    print("В результате программы произошла какая-то ошибка."
          "\nВероятно, процесс не может получить доступ к файлу, так как этот файл занят другим процессом.")
print('- готово')
