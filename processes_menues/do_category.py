from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *


def add_category(root, self):
    """if not root is self.new_window:
            root.withdraw()"""
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")
    popup = Toplevel(root)
    popup.title("Нова категорія")

    def back_form():
        popup.destroy()
        root.deiconify()
        self.btn_add_prod.config(state="normal")

    im = self.back
    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0, activebackground='red',
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=5)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    def add():
        enter_name.config(highlightbackground="lightgray")
        # Получаем значение из поля ввода
        category_name = enter_name.get()
        get_cat_name = f"SELECT Категорія FROM Категорія WHERE Категорія = '{category_name}' AND" \
                       f" Код_складу = '{self.current_sclad_id}'"
        is_cat = execute_sql_query_get(conn_str, get_cat_name)
        if is_cat:
            enter_name.config(highlightbackground="red", highlightcolor="red")
            error_lable = Label(popup, text="Така категорія вже існує",font=("Arial",12))
            error_lable.place(x=160, y=100)
            error_lable.config(foreground="red")
            return

        if category_name:  # Проверяем, что поле не пустое
            try:
                get_current_sclad_query = f"SELECT Код_складу FROM Склад WHERE Назва_складу = '{self.chosen_name}'"
                current_sclad = execute_sql_query_get(conn_str, get_current_sclad_query)
                # Формируем SQL-запрос с использованием значений из поля ввода
                sql_add = f"INSERT INTO Категорія (\"Категорія\", \"Код_складу\") VALUES" \
                          f" ('{category_name}', '{current_sclad[0][0]}')"

                execute_sql_query_insert(conn_str, sql_add)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                self.open_category_menu()
                back_form()
            except Exception as e:
                # Обрабатываем ошибку при выполнении SQL-запроса
                print(f"Ошибка при добавлении категории: {e}")
        else:
            enter_name.config(highlightbackground="red", highlightcolor="red")
            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
            error_lable.place(x=185, y=100)
            error_lable.config(foreground="red")
            return



    ttk.Label(popup, text="Додавання категорії", font=("Arial", 20, "bold")).pack()

    new_cat = Label(popup, text="Назва категорії:", font=("Arial", 14))
    new_cat.pack(anchor="nw", padx=10, pady=30)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.place(x=175, y=65)

    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add)
    btn_go.pack(pady=10)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 200
    # Вычисляем координаты для центрирования
    x_coordinate = root.winfo_x() + 100 + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() - 50 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)

    def on_close():
        self.btn_add_prod.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.destroy()  # Закрыть всплывающее окно

    popup.protocol("WM_DELETE_WINDOW", on_close)

def change_category(root, self):
    #if not root is self.new_window:
       # root.withdraw()
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування")

    def back_form():
        self.btn_add_prod.config(state="normal")
        self.change_items.config(state="normal")
        popup.destroy()  # Закрыть всплывающее окно

    im = self.back
    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0, activebackground='red',
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=5)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    def add():
        # Получаем значение из поля ввода
        category_name = enter_name.get()
        if category_name:  # Проверяем, что поле не пустое
            try:
                enter_name.config(highlightbackground="lightgray")
                # Получаем значение из поля ввода
                category_name = enter_name.get()

                sql_update_prod = f"""
                        UPDATE Категорія
                        SET Категорія = '{enter_name.get()}' 
                        WHERE Код_категорії = '{self.item_text[0]}' AND Код_складу = '{self.current_sclad_id}'
                    """

                execute_sql_query_insert(conn_str, sql_update_prod)
                self.open_category_menu()
            except Exception as ex:
                print("Error228: ", ex)
        else:
            enter_name.config(highlightbackground="red", highlightcolor="red")
            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
            error_lable.place(x=185, y=100)
            error_lable.config(foreground="red")
            return
    ttk.Label(popup, text="Редагування категорії", font=("Arial", 20, "bold")).pack()

    new_cat = Label(popup, text="Назва категорії:", font=("Arial", 14))
    new_cat.pack(anchor="nw", padx=10, pady=26)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.insert(0, f"{self.item_text[1]}")
    enter_name.place(x=175, y=65)

    btn_go = Button(popup, text="Редагувати", font=("Arial", 14), width=10, command=add)
    btn_go.pack(pady=10)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 200
    # Вычисляем координаты для центрирования
    x_coordinate = root.winfo_x() + 560 + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 250 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)

    def on_close():
        popup.destroy()  # Закрыть всплывающее окно
        #time.sleep(1)
        self.btn_add_prod.config(state="normal")
        self.change_items.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")



    popup.protocol("WM_DELETE_WINDOW", on_close)