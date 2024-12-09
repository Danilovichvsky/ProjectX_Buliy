
import tkinter as tk
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
back = None
add_prod_im = None

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty()

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x-60}+{y-10}")

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def entry_data(root, form3_instance):
    labels_list = []

    def add():
        for label in labels_list:
            label.destroy()

        existing_names = [name[1] for name in get_scl()]
        name = entry_skl.get()

        if name:
            if name in existing_names:
                label_error_add1 = ttk.Label(popup, text="Такий склад вже існує", foreground="red", background="White")
                label_error_add1.place(x=35, y=120)
                labels_list.append(label_error_add1)
            else:
                sql_query = f"INSERT INTO Склад (Назва_складу) VALUES (N'{name}')"
                execute_sql_query_insert(conn_str, sql_query)
                popup.withdraw()  # Скрываем окно, но сохраняем его состояние
                form3_instance.check_data()
                choose_manu(popup,form3_instance)


        else:
            label_error_add = ttk.Label(popup, text="Введіть назву", foreground="red", background="White")
            label_error_add.place(x=60, y=120)
            labels_list.append(label_error_add)



    popup = tk.Toplevel(root)
    popup.title("Додавання складу")
    popup.geometry("200x150")

    style = ttk.Style()
    style.configure("White.TButton", background="white", borderwidth=0)

    label = ttk.Label(popup, text="Введіть назву складу", font=("Arial", 12))
    label.pack(pady=10)
    entry_skl = Entry(popup, font=("Arial", 14), width=10)
    entry_skl.pack(pady=5)

    button_add = tk.Button(popup, text="Додати",font=("Arial", 12),background='white', bd=0,
                        highlightthickness=0, highlightbackground='white', command=add)
    button_add.pack(pady=7)

    popup.resizable(False, False)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    popup_width = 300
    popup_height = 140
    x_coordinate = root.winfo_x() + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 70 + (root_height - popup_height) // 2

    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")

    def on_close():
        popup.withdraw()


    popup.protocol("WM_DELETE_WINDOW", on_close)

def change_scl(self, root, chosen):
    def update_name():
        new_name = scl_name.get()
        kod_current_scl = f"SELECT Код_складу FROM Склад WHERE Назва_складу = '{chosen}'"
        kod = execute_sql_query_get(conn_str, kod_current_scl)
        sql_query = f"UPDATE Склад SET Назва_складу = '{new_name}' WHERE Код_складу = '{kod[0][0]}'"
        execute_sql_query_insert(conn_str, sql_query)
        popup.destroy()
        self.menu(new_name)

    popup = tk.Toplevel(root)
    popup.title("Редагування")

    Label(popup, text="Редагування складу",font=("Arial",12,"bold")).pack()
    self.edit_scl_name.config(state="disabled")
    label_name = Label(popup, text="Нова назва: ")
    label_name.place(x=20, y=40)
    scl_name = ttk.Entry(popup, width=20)
    scl_name.insert(0,chosen)
    scl_name.place(x=120, y=40)

    button_update = tk.Button(popup, text="Оновити", command=update_name)
    button_update.place(x=120, y=90)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    popup_width = 300
    popup_height = 150
    x_coordinate = root.winfo_x() + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 70 + (root_height - popup_height) // 2

    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")

    def on_close():
        self.edit_scl_name.config(state="normal")
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)


def get_scl():
    sql_query = "SELECT * FROM Склад;"
    return execute_sql_query_get(conn_str, sql_query)

# В popups.py
def delete_scl(root, form3_instance):
    labels_list = []
    names = []
    for scl in get_scl():
        names.append(scl[1])

    def delete():
        name = entry_skl.get().lower()
        print(name)
        # Check if a name is entered
        if not name or not name in names:
            label_error_add = ttk.Label(popup, text="Дані введено не вірно", foreground="red", background="White")
            label_error_add.place(x=60, y=120)
            labels_list.append(label_error_add)
        else:
            sql_query = f"DELETE FROM Склад WHERE Назва_складу = {form3_instance.chosen_name} "
            execute_sql_query_insert(conn_str, sql_query)  # Note: Pass parameters as a tuple
            popup.destroy()
            form3_instance.check_data()

    popup = Toplevel(root)
    popup.title("Warehouse Deletion")
    popup.geometry("200x150")
    label = Label(popup, text="Введіть назву складу", font=("Arial", 12))
    label.pack(pady=10)
    entry_skl = Entry(popup, font=("Arial", 14), width=10)
    entry_skl.pack(pady=5)

    button_add = ttk.Button(popup, text="Видалити", width=10, command=delete)
    button_add.pack(pady=5)
    popup.resizable(False, False)

    # Get the dimensions of the root window
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()

    # Get the dimensions of the popup window
    popup_width = 200
    popup_height = 150

    # Calculate the coordinates to center the popup window
    x_coordinate = root.winfo_x() + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 70 + (root_height - popup_height) // 2

    # Place the popup window at the center
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")

def open_menu_(self,popup,chosen_name):
    self.menu(chosen_name)
    popup.destroy()
    self.new_window.deiconify()

    self.new_window.lift()

def choose_manu(root, self):
    popup_ch = tk.Toplevel(root)
    popup_ch.title("Вибір складу")
    popup_ch.resizable(False, False)

    container = ttk.Frame(popup_ch)
    canvas = Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((90, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    label = Label(scrollable_frame, text="Оберіть склад", font=("Arial", 14, "bold"))
    label.pack(pady=10)
    name = []
    while not name:
        name = get_scl()
    for i, names in enumerate(name):
        btn_choose = ttk.Button(scrollable_frame, text=names[1], width=30,
                                command=lambda chosen_name=names[1]: open_menu_(self, popup_ch, chosen_name))
        btn_choose.pack(pady=3)

    def add_warehouse():
        entry_data(root, self)  # Вызываем функцию для добавления склада
        popup_ch.withdraw()

    add_else_btn = ttk.Button(popup_ch, text="Додати склад", command=add_warehouse)
    add_else_btn.pack(side="bottom", pady=(50, 20))

    # Центрируем всплывающее окно по отношению к родительскому окну
    screen_width = popup_ch.winfo_screenwidth()
    screen_height = popup_ch.winfo_screenheight()
    x_coordinate = (screen_width - popup_ch.winfo_reqwidth()) // 2
    y_coordinate = (screen_height - popup_ch.winfo_reqheight()) // 2
    popup_ch.geometry(f"+{x_coordinate-110}+{y_coordinate-140}")

    def on_close_child_window():
        # Уничтожаем окно при его закрытии
        self.login_form_instance.root.destroy()

    # Назначаем обработчик закрытия окна
    popup_ch.protocol("WM_DELETE_WINDOW", on_close_child_window)

def filter_save_th(root,self):

    popup = Toplevel(root)
    popup.title("Фільтр. Зона зберігання")
    popup.geometry("300x100")
    label = Label(popup, text="Зона зберігання")
    label.pack(pady=10)

    label_name = Label(popup, text="Введіть назву: ")
    label_name.place(x=10,y=40)

    entry_data =Entry(popup,width=20)
    entry_data.place(x=110,y=40)

    button = Button(popup, text="Знайти")
    button.pack(pady=50)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 300
    popup_height = 150
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 380 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)
































