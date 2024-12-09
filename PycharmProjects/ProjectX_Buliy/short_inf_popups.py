from tkinter import Label,Button,Toplevel

def empty_popup(root):
    popup = Toplevel(root)
    popup.title("Помилка")
    popup.geometry("300x100")
    label = Label(popup, text="Назва'name' повинна бути строкою.")
    label.pack(pady=10)
    button = Button(popup, text="Закрити", command=popup.destroy)
    button.pack()

def delete_error(root):
    popup = Toplevel(root)
    popup.title("Помилка")
    popup.geometry("300x100")
    label = Label(popup, text="Дані використовуються в іншій таблиці")
    label.pack(pady=10)
    button = Button(popup, text="Закрити", command=popup.destroy)
    button.pack()

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 300
    popup_height = 90
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)


def wrong_data(root):
    popup = Toplevel(root)
    popup.title("Ошибка")
    popup.geometry("300x100")
    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования
    x_coordinate = (screen_width - 300) // 2
    y_coordinate = (screen_height - 10) // 2

    # Устанавливаем геометрию окна
    popup.geometry(f"300x100+{x_coordinate}+{y_coordinate-150}")
    label = Label(popup, text="Таких даних не існує")
    label.pack(pady=10)
    button = Button(popup, text="Закрыть", command=popup.destroy)
    button.pack()

def error_saving_psw(root):
    popup = Toplevel(root)
    popup.title("Помилка")
    popup.geometry("300x100")
    label = Label(popup, text="Паролі на співпадають")
    label.pack(pady=10)
    button = Button(popup, text="Закрыть", command=popup.destroy)
    button.pack()

def success_login(root):
    popup = Toplevel(root)
    popup.title("Ви успішно увійшли!")
    popup.geometry("300x100")

    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования
    x_coordinate = (screen_width - 300) // 2
    y_coordinate = (screen_height - 100) // 2

    # Устанавливаем геометрию окна
    popup.geometry(f"300x100+{x_coordinate}+{y_coordinate}")

    label = Label(popup, text="Ви успішно зареєструвались")
    label.pack(pady=10)
    button = Button(popup, text="Закрити", command=popup.destroy)
    button.pack()





