
from short_inf_popups import  *
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *



def add_save_th(root, self):
    """if not root is self.new_window:
            root.withdraw()"""
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Зона зберігання")

    Label(popup, text="Нова зона зберігання", font=("Arial", 20, "bold")).pack(pady=19)

    im = self.back

    def insert_th():
        try:
            temperature.config(highlightbackground="lightgray")
            count_pal.config(highlightbackground="lightgray")
            thona.config(highlightbackground="lightgray")
            all_labels = [thona.get(), count_pal.get(), temperature.get()]

            empty_fields = []
            for i, label in enumerate(all_labels):
                if not label:
                    empty_fields.append(i)

            if empty_fields:
                print("Следующие поля не заполнены:")
                for field_index in empty_fields:
                    if field_index == 0:
                        thona.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 1:
                        count_pal.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 2:
                        temperature.config(highlightbackground="red", highlightcolor="red")

                error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
                error_lable.place(x=185, y=205)
                error_lable.config(foreground="red")
                return
            else:
                if not check_validate():
                    return
                print("Все поля заполнены.")

            # Получаем код категории из базы данных

            sql_insert_th = f"INSERT INTO Зона_зберігання (Назва_зони_зберігання, Місткість_палетів_," \
                            f" Температура_зберігання, Код_складу) VALUES ('{thona.get()}', '{count_pal.get()}'," \
                            f" '{temperature.get()}','{self.current_sclad_id}')"

            execute_sql_query_insert(conn_str, sql_insert_th)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_save_menu()
            back_form()
        except Exception as ex:
            print("Error228: ",ex)


    def back_form():
        popup.destroy()
        root.deiconify()
        self.btn_add_prod.config(state="normal")
        # root.deiconify()

    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(count_pal, 'error_label'):
            count_pal.error_label.destroy()
            count_pal.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(temperature, 'error_label'):
            temperature.error_label.destroy()
            temperature.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = count_pal.get().strip()  # Удаляем пробелы в начале и конце строки
        price_value = temperature.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        sql_names = f"""
                              SELECT * FROM Зона_зберігання
                              WHERE Назва_зони_зберігання = '{thona.get()}'
                            """

        names = execute_sql_query_get(conn_str, sql_names)
        print(names, "save_names")
        if names:
            error_label2 = Label(popup, text="Така зона вже існує")
            error_label2.place(x=235, y=107)
            error_label2.config(foreground="red")
            error_value_list.append(thona)
            print("Помилка: така зона вже існує")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            count_pal.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            count_pal.error_label = error_label

        if not price_value.isdigit():
            error_value_list.append(price_value)
            temperature.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            temperature.error_label = error_label

        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0, activebackground='red',
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=23)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    ttk.Label(popup, text="Назва зони зберігання:", font=("Arial", 14,)).pack(pady=8, padx=10, anchor="nw")
    thona = Entry(popup, width=20, font=("Arial", 12))
    thona.place(x=240, y=86)

    ttk.Label(popup, text="Місткість палетів:", font=("Arial", 14,)).pack(pady=11, padx=10, anchor="nw")
    count_pal = Entry(popup, width=20, font=("Arial", 12))
    count_pal.place(x=240, y=134)

    ttk.Label(popup, text="Температура зберігання:", font=("Arial", 14,)).pack(pady=9, padx=10, anchor="nw")
    temperature = Entry(popup, width=20, font=("Arial", 12))
    temperature.place(x=240, y=180)
    Button(popup, text="Додати", font=("Arial", 14), width=10, command=insert_th).pack(pady=20)
    # sql_query_ins = "INSERT INTO Зона_зберігання (Назва_зони_зберігання, Місткість_палетів_," \
    # f" Температура_зберігання, Код_складу) VALUES ('{}')"
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 300
    # Вычисляем координаты для центрирования

    x_coordinate = root.winfo_x() + 5 + (root_width - popup_width) // 2
    y_coordinate = root.winfo_y() + 50 + (root_height - popup_height) // 2

    if not root is self.new_window:
        x_coordinate = root.winfo_x() + 100 + (root_width - popup_width) // 2
        y_coordinate = root.winfo_y() + 270 + (root_height - popup_height) // 2
    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)

    def on_close():
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")

        popup.destroy()  # Закрыть всплывающее окно
        self.btn_add_prod.config(state="normal")


    popup.protocol("WM_DELETE_WINDOW", on_close)

def change_save_th(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування")

    def on_close():
        # Здесь отключаем кнопку del_items
        self.del_items.config(state="normal")
        self.change_items.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.withdraw()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    def add_data():
        try:
            all_labels = [thona.get(), count_pal.get(), temperature.get()]

            empty_fields = []
            for i, label in enumerate(all_labels):
                if not label:
                    empty_fields.append(i)

            if empty_fields:
                print("Следующие поля не заполнены:")
                for field_index in empty_fields:
                    if field_index == 0:
                        thona.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 1:
                        count_pal.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 2:
                        temperature.config(highlightbackground="red", highlightcolor="red")

                error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
                error_lable.place(x=185, y=200)
                error_lable.config(foreground="red")
                return
            else:
                if not check_validate():
                    return
                print("Все поля заполнены.")

            # Получаем код категории из базы данных


            sql_update_prod = f"""
                    UPDATE Зона_зберігання
                    SET Назва_зони_зберігання = '{thona.get()}',
                        Місткість_палетів_ = '{count_pal.get()}',
                        Температура_зберігання = '{temperature.get()}'
                    WHERE Код_зони_зберігання = '{self.item_text[0]}'
                """

            execute_sql_query_insert(conn_str, sql_update_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_save_menu()
        except Exception as ex:
            print("Error228: ",ex)

    def back_form():
        self.change_items.config(state="normal")
        popup.destroy()

    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(count_pal, 'error_label'):
            count_pal.error_label.destroy()
            count_pal.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(temperature, 'error_label'):
            temperature.error_label.destroy()
            temperature.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = count_pal.get().strip()  # Удаляем пробелы в начале и конце строки
        price_value = temperature.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            count_pal.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            count_pal.error_label = error_label

        if not price_value.isdigit():
            error_value_list.append(price_value)
            temperature.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            temperature.error_label = error_label

        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    im = self.back
    ttk.Label(popup, text="Редагування", font=("Arial", 20, "bold")).pack(pady=15)

    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0,
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=16)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    ttk.Label(popup, text="Назва зони зберігання:", font=("Arial", 14,)).pack(pady=8, padx=10, anchor="nw")
    thona = Entry(popup, width=20, font=("Arial", 12))
    thona.insert(0, f"{self.item_text[1]}")
    thona.place(x=240, y=75)

    ttk.Label(popup, text="Місткість палетів:", font=("Arial", 14,)).pack(pady=11, padx=10, anchor="nw")
    count_pal = Entry(popup, width=20, font=("Arial", 12))
    count_pal.insert(0, f"{self.item_text[2]}")
    count_pal.place(x=240, y=122)

    ttk.Label(popup, text="Температура зберігання:", font=("Arial", 14,)).pack(pady=9, padx=10, anchor="nw")
    temperature = Entry(popup, width=20, font=("Arial", 12))
    temperature.insert(0, f"{self.item_text[3]}")
    temperature.place(x=240, y=169)
    Button(popup, text="Редагувати", font=("Arial", 14), width=10, command=add_data).pack(pady=25)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 300

    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)




