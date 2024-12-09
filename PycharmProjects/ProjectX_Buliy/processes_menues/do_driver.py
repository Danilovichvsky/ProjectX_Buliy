from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *


def add_driver(root, self):
    """if not root is self.new_window:
            root.withdraw()"""
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Новий водій")

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
        enter_number.config(highlightbackground="lightgray")

        all_labels = [enter_name.get(), enter_number.get()]

        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)

        sql_number = f"SELECT * FROM Автотранспорт WHERE Номер_транспорту = '{enter_number.get()}'"
        present_n = execute_sql_query_get(conn_str, sql_number)
        if hasattr(enter_number, 'error_label_name'):
            enter_number.error_label_name.destroy()

        if present_n:
            error_lable_name = Label(popup, text="Такий номер авто вже існує")
            error_lable_name.place(x=200, y=193)
            error_lable_name.config(foreground="red")
            enter_number.config(highlightbackground="red", highlightcolor="red")
        if empty_fields:
            print("Следующие поля не заполнены:")
            for field_index in empty_fields:
                if field_index == 0:
                    enter_name.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 1:
                    enter_number.config(highlightbackground="red", highlightcolor="red")

            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
            error_lable.place(x=155, y=160)
            error_lable.config(foreground="red")
            return
        else:
            print("Все поля заполнены.")
        # Получаем значение из поля ввода
        try:
            sql_add = f"INSERT INTO Водій (\"ПІБ_водія\", \"Телефон_водія\") VALUES \
                       ('{enter_name.get()}', '{enter_number.get()}')"
            execute_sql_query_insert(conn_str, sql_add)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_driver_menu()
            back_form()
        except Exception as e:
            # Обрабатываем ошибку при выполнении SQL-запроса
            print(f"Ошибка при добавлении категории: {e}")

    ttk.Label(popup, text="Додавання водія", font=("Arial", 20, "bold")).pack(pady=3)

    new_ts = Label(popup, text="ПІБ водія:", font=("Arial", 14))
    new_ts.pack(anchor="nw", padx=10, pady=20)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.place(x=210, y=65)

    number_dr = Label(popup, text="Телефон водія:", font=("Arial", 14))
    number_dr.pack(anchor="nw", padx=10, pady=2)
    enter_number = Entry(popup, width=20, font=("Arial", 12))
    enter_number.place(x=210, y=115)


    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add)
    btn_go.pack(pady=20)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 250
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 380 + (root_height - popup_height) // 2

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

def change_driver(root, self):
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
        enter_name.config(highlightbackground="lightgray")
        enter_number.config(highlightbackground="lightgray")


        all_labels = [enter_name.get(), enter_number.get()]

        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)
                empty_fields.append(i)

        if empty_fields:
            print("Следующие поля не заполнены:")
            for field_index in empty_fields:
                if field_index == 0:
                    enter_name.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 1:
                    enter_number.config(highlightbackground="red", highlightcolor="red")

            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
            error_lable.place(x=155, y=160)
            error_lable.config(foreground="red")
            return
        else:
            print("Все поля заполнены.")
        # Получаем значение из поля ввода
        try:
            sql_update_prod = f"""
                    UPDATE Водій
                    SET ПІБ_водія = '{enter_name.get()}',
                    Телефон_водія = '{enter_number.get()}'
                    WHERE Код_водія = '{self.item_text[0]}'
                """

            execute_sql_query_insert(conn_str, sql_update_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_driver_menu()
            back_form()
        except Exception as ex:
            print("Error228: ", ex)

    ttk.Label(popup, text="Редагування водія", font=("Arial", 20, "bold")).pack()

    new_ts = Label(popup, text="ПІБ водія:", font=("Arial", 14))
    new_ts.pack(anchor="nw", padx=10, pady=30)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.insert(0, f"{self.item_text[1]}")
    enter_name.place(x=210, y=65)

    number_dr = Label(popup, text="Телефон водія:", font=("Arial", 14))
    number_dr.pack(anchor="nw", padx=10, pady=2)
    enter_number = Entry(popup, width=20, font=("Arial", 12))
    enter_number.insert(0, f"{self.item_text[2]}")
    enter_number.place(x=210, y=115)

    btn_go = Button(popup, text="Редагувати", font=("Arial", 14), width=10, command=add)
    btn_go.pack(pady=30)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 250
    # Вычисляем координаты для центрирования
    x_coordinate = root.winfo_x() + 963 + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 480 + (root_height - popup_height) // 2

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