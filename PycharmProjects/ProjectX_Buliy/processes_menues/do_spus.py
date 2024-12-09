from datetime import date
from tkinter import Button,Label,Entry, Toplevel, END

from processes_menues.do_customer import add_customer
from processes_menues.do_save_thona import add_save_th
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from processes_menues.do_product import add_prod

def count_pallets(entry):
    try:
        sql_count = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{entry.get()}' "
        result = execute_sql_query_get(conn_str, sql_count)
        total_pallets = 0
        # Получаем результат
        total_pallets += result[0][0] if result and result[0] else 0
        if total_pallets is None:
            total_pallets=0
        return total_pallets
    except Exception as e:
        print(f"Ошибка при подсчете количества палетов: {e}")
        return 0

def add_spus(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Нове списання")

    def save_data_fottime():
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_reason = enter_reason.get()
        self.entered_data = enter_data.entry.get()
        self.entered_number_ord = enter_number_ord.get()

    def on_close():
        self.btn_add_prod.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.withdraw()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    def add_data():

        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_reason.config(highlightbackground="lightgray")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_name.config(style="Custom.TCombobox")
        enter_number_ord.config(highlightbackground="lightgray")
        enter_count.config(highlightbackground="lightgray")


        all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(),
                      enter_name.get(), enter_reason.get()]



        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)

        if hasattr(enter_number_ord, 'error_lable_name'):
            enter_number_ord.error_lable_name.destroy()

        sql_number = f"SELECT * FROM Акт_списання WHERE Номер_акту_списання = '{enter_number_ord.get()}'"
        present_n = execute_sql_query_get(conn_str, sql_number)
        if present_n:
            error_lable_name = Label(popup, text="Такий номер списання вже існує")
            error_lable_name.place(x=200, y=93)
            error_lable_name.config(foreground="red")
            enter_number_ord.config(highlightbackground="red", highlightcolor="red")
            enter_number_ord.error_lable_name = error_lable_name
            return

        if empty_fields:
            for field_index in empty_fields:
                if field_index == 0:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_data.entry.config(style="Custom.TCombobox")
                elif field_index == 1:
                    enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 2:
                    enter_count.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_name.config(style="Custom.TCombobox")
                elif field_index == 4:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_reason.config(highlightbackground="red", highlightcolor="red")

            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля",font=("Arial",12))
            error_lable.place(x=155, y=305)
            error_lable.config(foreground="red")
            popup.error_label = error_lable
            return
        else:
            if not check_validate():
                return


        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)


        sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        print("SQL query for price:", sql_th_price)
        price = execute_sql_query_get(conn_str, sql_th_price)
        print("Price:", price)

        total_count = count_pallets(enter_name)
        try:
            if int(enter_count.get()) <= total_count:
                # SQL-запрос для добавления новой записи в таблицу Продукція
                sql_add_prod = f"""
                                    INSERT INTO Акт_списання (Дата, Номер_акту_списання,
                                     Кількість__палетів_,Причина_списання,Код_складу,Код_продукції)
                                    VALUES ('{enter_data.entry.get()}', '{enter_number_ord.get()}',
                                     '{enter_count.get()}', '{enter_reason.get()}','{self.current_sclad_id}', 
                                     '{kod_pr[0][0]}');"""

                execute_sql_query_insert(conn_str, sql_add_prod)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                update_product_stock(enter_name.get(),int(enter_count.get()))
                self.open_spus_menu()
            else:
                enter_count.config(highlightbackground="red", highlightthickness=0.5)
                error_label = Label(popup, text="ПОМИЛКА: Завелика кількість товару ")
                error_label.place(x=90, y=305)
                error_label.config(foreground="red")
                popup.error_label = error_label
        except Exception as e:
            print("An error occurred:", e)

    def open_add_pr_form():
        save_data_fottime()
        add_prod(popup,self)
        popup.withdraw()

    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(enter_number_ord, 'error_label'):
            enter_number_ord.error_label.destroy()
            enter_number_ord.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_count, 'error_label'):
            enter_count.error_label.destroy()
            enter_count.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=145, y=328)
            error_label.config(foreground="red")
            enter_count.error_label = error_label


        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=145, y=348)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label
        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Додавання списання", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер списання:", font=("Arial", 14))
    number_ord.place(x=10, y=65)
    enter_number_ord = Entry(popup, width=17, font=("Arial", 14))
    enter_number_ord.place(x=175, y=65)

    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.place(x=10, y=115)

    enter_name = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_name.place(x=175, y=115)
    def load_data_cat(event):
        cat_names_upd = execute_sql_query_get(conn_str, f"SELECT Назва_продукції FROM Продукція WHERE Код_складу = '{self.current_sclad_id}'")
        if not cat_names_upd:
            not_found_prod = Label(popup, text="Продукція відсутня на складі", font=("Arial", 12))
            not_found_prod.place(x=150, y=455)
            not_found_prod.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_name['values'] = [el[0] for el in cat_names_upd]

    enter_name.bind("<Button-1>", load_data_cat)

    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=165)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.place(x=175, y=165)

    add_pr_btn = Button(popup, image=self.add_prod_im, command=open_add_pr_form, width=30, height=30)
    add_pr_btn.place(x=390, y=112)
    add_pr_btn.config(background="White", highlightbackground="White", activebackground="white")

    reason_lbl = ttk.Label(popup, text="Причина:", font=("Arial", 14))
    reason_lbl.place(x=10, y=215)
    enter_reason = Entry(popup, width=17, font=("Arial", 14))
    enter_reason.place(x=175, y=215)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=265)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.place(x=175, y=265)


    def update_product_stock(product_name, pallets_count):
        # Получаем информацию о продукции по названию
        get_product_info_query = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{enter_name.get()}'"
        product_info = execute_sql_query_get(conn_str, get_product_info_query)

        if product_info:
            # Получаем текущее количество палетов продукции
            current_pallets_count = product_info[0][0]  # Предполагается, что количество палетов находится на второй позиции

            # Обновляем количество палетов, добавляя количество палетов из ордера
            updated_pallets_count = current_pallets_count - pallets_count

            # Обновляем запись в таблице Продукція
            update_query = f"UPDATE Продукція SET Кількість_палетів_ = '{updated_pallets_count}' " \
                           f"WHERE Назва_продукції = '{product_name}'"
            execute_sql_query_insert(conn_str, update_query)

            # Выводим сообщение об успешном обновлении
            print(f"Количество палетов для продукции '{product_name}' успешно обновлено.")
        else:
            print(f"Продукция с названием '{product_name}' не найдена.")

    def check_product_availability(event):
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")

        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)

        if not kod_pr:
            error_label_name = Label(popup, text="Такої продукції не має на складі")
            error_label_name.place(x=180, y=143)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_name.config(style="Custom.TCombobox")

    enter_name.bind("<KeyRelease>", check_product_availability)

    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add_data)
    btn_go.place(x=190, y=340)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 400
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)


def change_spus(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування")

    def save_data_fottime():
        #enter_name.delete(0, "end")
        #enter_count.delete(0, "end")
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_data = enter_data.entry.get()
        self.entered_reason = enter_reason.get()
        self.entered_number_ord= enter_number_ord.get()

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
            if hasattr(popup, 'error_label'):
                popup.error_label.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_reason.config(highlightbackground="lightgray")
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")
            enter_number_ord.config(highlightbackground="lightgray")
            enter_count.config(highlightbackground="lightgray")

            all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(),
                          enter_name.get(), enter_reason.get()]

            empty_fields = []
            for i, label in enumerate(all_labels):
                if not label:
                    empty_fields.append(i)

            if hasattr(enter_number_ord, 'error_label_name'):
                enter_number_ord.error_label_name.destroy()


            if empty_fields:
                print("Следующие поля не заполнены:")
                for field_index in empty_fields:
                    if field_index == 0:
                        combostyle.configure("Custom.TCombobox", bordercolor="red")
                        enter_data.entry.config(style="Custom.TCombobox")
                    elif field_index == 1:
                        enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 2:
                        enter_count.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 3:
                        combostyle.configure("Custom.TCombobox", bordercolor="red")
                        enter_name.config(style="Custom.TCombobox")
                    elif field_index == 4:
                        combostyle.configure("Custom.TCombobox", bordercolor="red")
                        enter_reason.config(highlightbackground="red", highlightcolor="red")

                error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля", font=("Arial", 12))
                error_lable.place(x=155, y=305)
                error_lable.config(foreground="red")
                return
            else:
                if not check_validate():
                    return


            sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
            kod_pr = execute_sql_query_get(conn_str, sql_name)

            total_count = count_pallets(enter_name)
            order_number = enter_number_ord.get()
            sql_query = f"SELECT * FROM Акт_списання WHERE Номер_акту_списання = '{order_number}'"
            result = execute_sql_query_get(conn_str, sql_query)

            if hasattr(enter_number_ord, 'error_label_name'):
                enter_number_ord.error_label_name.destroy()

            enter_number_ord.config(highlightbackground="lightgray", highlightcolor="lightgray")
            if len(result) > 0:
                error_label_name = Label(popup, text="Такий номер ордеру вже існує")
                error_label_name.place(x=200, y=93)
                error_label_name.config(foreground="red")
                enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                enter_number_ord.error_label_name = error_label_name

                return

            if int(enter_count.get()) <= total_count:
                sql_update_prod = f"""
                        UPDATE Акт_списання
                        SET Дата = '{enter_data.entry.get()}',
                            Номер_акту_списання = '{enter_number_ord.get()}',
                            Кількість__палетів_ = '{enter_count.get()}',
                            Причина_списання = '{enter_reason.get()}',
                            Код_складу = '{self.current_sclad_id}',
                            Код_продукції = '{kod_pr[0][0]}'
                        WHERE Код_акту_списання = '{self.item_text[0]}'
                    """
                execute_sql_query_insert(conn_str, sql_update_prod)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                update_product_stock(enter_name.get(), int(enter_count.get()))
                self.open_spus_menu()
            else:
                enter_count.config(highlightbackground="red", highlightthickness=0.5)
                error_label = Label(popup, text="ПОМИЛКА: Завелика кількість товару ")
                error_label.place(x=90, y=305)
                error_label.config(foreground="red")
                popup.error_label = error_label
        except TypeError:
            add_data()

    def open_add_pr_form():
        save_data_fottime()
        add_prod(popup, self)
        popup.withdraw()

    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(enter_number_ord, 'error_label'):
            enter_number_ord.error_label.destroy()
            enter_number_ord.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_count, 'error_label'):
            enter_count.error_label.destroy()
            enter_count.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=300)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=145, y=348)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label

        popup.error_label = error_label

        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Редагування списання", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер списання:", font=("Arial", 14))
    number_ord.place(x=10, y=65)
    enter_number_ord = Entry(popup, width=17, font=("Arial", 14))
    enter_number_ord.insert(0, f"{self.item_text[1]}")
    enter_number_ord.place(x=175, y=65)

    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.place(x=10, y=115)

    enter_name = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_name.insert(0, f"{self.item_text[3]}")
    enter_name.place(x=175, y=115)

    def load_data_cat(event):
        cat_names_upd = execute_sql_query_get(conn_str,
                                              f"SELECT Назва_продукції FROM Продукція WHERE Код_складу = '{self.current_sclad_id}'")
        if not cat_names_upd:
            not_found_prod = Label(popup, text="Продукція відсутня на складі", font=("Arial", 12))
            not_found_prod.place(x=150, y=455)
            not_found_prod.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_name['values'] = [el[0] for el in cat_names_upd]

    enter_name.bind("<Button-1>", load_data_cat)

    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=165)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.insert(0, f"{self.item_text[4]}")
    enter_count.place(x=175, y=165)

    add_pr_btn = Button(popup, image=self.add_prod_im, command=open_add_pr_form, width=30, height=30)
    add_pr_btn.place(x=390, y=112)
    add_pr_btn.config(background="White", highlightbackground="White", activebackground="white")

    reason_lbl = ttk.Label(popup, text="Причина:", font=("Arial", 14))
    reason_lbl.place(x=10, y=215)
    enter_reason = Entry(popup, width=17, font=("Arial", 14))
    enter_reason.insert(0, f"{self.item_text[5]}")
    enter_reason.place(x=175, y=215)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=265)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.entry.delete(0, END)
    enter_data.entry.insert(0, f"{self.item_text[6]}")
    enter_data.place(x=175, y=265)

    def update_product_stock(product_name, pallets_count):
        # Получаем информацию о продукции по названию
        get_product_info_query = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{enter_name.get()}'"
        product_info = execute_sql_query_get(conn_str, get_product_info_query)

        if product_info:
            # Получаем текущее количество палетов продукции
            current_pallets_count = product_info[0][
                0]  # Предполагается, что количество палетов находится на второй позиции

            # Обновляем количество палетов, добавляя количество палетов из ордера
            updated_pallets_count = current_pallets_count - pallets_count

            # Обновляем запись в таблице Продукція
            update_query = f"UPDATE Продукція SET Кількість_палетів_ = '{updated_pallets_count}' " \
                           f"WHERE Назва_продукції = '{product_name}'"
            execute_sql_query_insert(conn_str, update_query)

            # Выводим сообщение об успешном обновлении
            print(f"Количество палетов для продукции '{product_name}' успешно обновлено.")
        else:
            print(f"Продукция с названием '{product_name}' не найдена.")

    def check_product_availability(event):
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")

        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)

        if not kod_pr:
            error_label_name = Label(popup, text="Такої продукції не має на складі")
            error_label_name.place(x=180, y=143)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_name.config(style="Custom.TCombobox")

    enter_name.bind("<KeyRelease>", check_product_availability)

    btn_go = Button(popup, text="Редагувати",font=("Arial",14),width=10, command=add_data)
    btn_go.place(x=195,y=340)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 400
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)
