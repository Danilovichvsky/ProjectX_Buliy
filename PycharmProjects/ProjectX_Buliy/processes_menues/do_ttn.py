from datetime import date
from tkinter import Button,Label,Entry, Toplevel, END

from processes_menues.do_avto import add_avto
from processes_menues.do_customer import add_customer
from processes_menues.do_driver import add_driver
from processes_menues.do_save_thona import add_save_th
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from processes_menues.do_product import add_prod


def add_ttn(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Нова ТТН")

    def save_data_fottime():
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_cst = cst_name.get()
        self.entered_data = enter_data.entry.get()
        self.entered_sum = enter_sum.get()
        self.entered_price = enter_price.get()
        self.entered_driver = enter_driver.get()
        self.entered_number_ord = enter_number_ord.get()
        self.entered_ts= enter_ts.get()


        #self.entered_category = enter_category.get()
        #self.entered_price = enter_price.get()
        #self.entered_th = enter_th.get()

    def on_close():
        self.btn_add_prod.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.withdraw()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    def add_data():
        if hasattr(popup, 'error_lable'):
            popup.error_lable.destroy()

        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_data.config(style="CustomGray.TCombobox")
        enter_name.config(style="CustomGray.TCombobox")
        enter_driver.config(style="CustomGray.TCombobox")
        enter_ts.config(style="CustomGray.TCombobox")
        cst_name.config(style="CustomGray.TCombobox")

        enter_number_ord.config(highlightbackground="lightgray")
        enter_count.config(highlightbackground="lightgray")
        enter_price.config(highlightbackground="lightgray")

        error_lable = Label(popup, text="")

        all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(), enter_price.get(),
                      enter_name.get(),  cst_name.get(),enter_driver.get(),enter_ts.get()]


        sql_number = f"SELECT Номер_ТТН FROM ТТН WHERE Номер_ТТН = '{enter_number_ord.get()}'"
        present_n = execute_sql_query_get(conn_str, sql_number)
        if hasattr(enter_number_ord, 'error_lable_name'):
            enter_number_ord.error_lable_name.destroy()
        if present_n:
            error_lable_name = Label(popup, text="Такий номер ТТН вже існує")
            error_lable_name.place(x=200, y=93)
            error_lable_name.config(foreground="red")
            enter_number_ord.config(highlightbackground="red", highlightcolor="red")
            enter_number_ord.error_lable_name = error_lable_name
            return


        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)


        if empty_fields:
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            for field_index in empty_fields:
                if field_index == 0:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_data.entry.config(style="Custom.TCombobox")
                elif field_index == 1:
                    enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 2:
                    enter_count.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    enter_price.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 4:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_name.config(style="Custom.TCombobox")
                elif field_index == 5:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    cst_name.config(style="Custom.TCombobox")
                elif field_index == 6:

                    enter_driver.config(style="Custom.TCombobox")
                elif field_index == 7:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_ts.config(style="Custom.TCombobox")

            error_lable.config(foreground="red", text="Пропущені поля")
            error_lable.place(x=190, y=550)
            popup.error_lable = error_lable  # Сохраняем ссылку на метку в объекте окна
            return
        else:
            if not check_validate():
                return
            print("Все поля заполнены.")


        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)

        sql_name = f"SELECT Код_водія FROM Водій WHERE ПІБ_водія = '{enter_driver.get()}' "
        kod_dr = execute_sql_query_get(conn_str, sql_name)

        sql_name = f"SELECT Код_замовника FROM Замовник WHERE ПІБ_контактної_особи = '{cst_name.get()}' "
        kod_cst = execute_sql_query_get(conn_str, sql_name)

        sql_name = f"SELECT Код_транспорту FROM Автотранспорт WHERE Назва_транспорту = '{enter_ts.get()}' "
        kod_ts = execute_sql_query_get(conn_str, sql_name)

        """sql_name = f"SELECT Код_ТТН FROM ТТН WHERE Номер_ТТН = '{enter_number_ord.get()}' "
        kod_ttn = execute_sql_query_get(conn_str, sql_name)
        if kod_ttn:
            print("такий номер ттн вже э")
            return """

        sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        print("SQL query for price:", sql_th_price)
        price = execute_sql_query_get(conn_str, sql_th_price)
        print("Price:", price)

        try:

            # SQL-запрос для добавления новой записи в таблицу Продукція

            sql_add_prod = f"""
                INSERT INTO ТТН (Дата, Номер_ТТН, Кількість_палетів_, Ціна_за_од, Сума, Код_замовника, Код_складу, Код_продукції, Код_водія, Код_транспорту)
                VALUES ('{enter_data.entry.get()}', '{enter_number_ord.get()}', '{enter_count.get()}',
                        '{enter_price.get()}', '{enter_sum.get()}', '{kod_cst[0][0]}', '{self.current_sclad_id}',
                        '{kod_pr[0][0]}', '{kod_dr[0][0]}', '{kod_ts[0][0]}')"""

            execute_sql_query_insert(conn_str, sql_add_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_ttn_menu()


        except Exception as e:
            error_prod_sclad = Label(popup, text=f"Помилка запиту: {e}")
            error_prod_sclad.place(x=90, y=328)
            error_prod_sclad.config(foreground="red")

    def calculate_total(event):
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")

        sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}'" \
                       f"AND Код_складу = '{self.current_sclad_id}'"
        price = execute_sql_query_get(conn_str, sql_th_price)
        if enter_name.get():
            enter_price.delete(0, END)  # Clear the entry before inserting new price
            enter_price.insert(0, price[0][0])
        if enter_count.get() and enter_name.get():
            check_product_availability(None)
            if price and enter_count.get():
                try:
                    # Преобразуем строку цены в число
                    price_per_unit = price[0][0]

                    # Рассчитываем общую сумму как произведение цены за единицу на количество
                    general_sum = price_per_unit * int(enter_count.get())
                    print("Общая сумма:", general_sum)

                    # Помещаем рассчитанное значение суммы в соответствующий виджет
                    enter_sum.delete(0, END)  # Очищаем поле ввода суммы
                    enter_sum.insert(0, general_sum)  # Устанавливаем новое значение суммы
                except ValueError:
                    print("Ошибка: Неправильный формат цены за единицу или количества")
            else:
                error_lable_name = Label(popup, text="Такої продукції не має на складі")
                error_lable_name.place(x=180, y=143)
                error_lable_name.config(foreground="red")


    def open_add_prod_form():
        save_data_fottime()
        add_prod(popup,self)
        popup.withdraw()

    def open_add_dr_form():
        save_data_fottime()
        add_driver(popup,self)
        popup.withdraw()

    def open_add_avto_form():
        save_data_fottime()
        add_avto(popup,self)
        popup.withdraw()

    def open_add_cust_form():
        save_data_fottime()
        add_customer(popup,self)
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

        if hasattr(enter_sum, 'error_label'):
            enter_sum.error_label.destroy()
            enter_sum.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_price, 'error_label'):
            enter_price.error_label.destroy()
            enter_price.config(highlightbackground="lightgray", highlightcolor="black")
        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()
        summa = enter_sum.get().strip()
        price = enter_price.get().strip()
        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not price.isdigit():
            error_value_list.append(count_value)
            enter_price.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_price.error_label = error_label

        if not summa.isdigit():
            error_value_list.append(count_value)
            enter_sum.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_sum.error_label = error_label

        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label
        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Додавання ТТН", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер ТТН:", font=("Arial", 14))
    number_ord.place(x=10, y=65)
    enter_number_ord = Entry(popup, width=17, font=("Arial", 14))
    enter_number_ord.place(x=175, y=65)

    customers_all = None
    while customers_all is None:
        customers_all = execute_sql_query_get(conn_str, f"SELECT ПІБ_контактної_особи FROM Замовник")
    if not customers_all:
        not_found_ = Label(popup, text="Замовників не має", font=("Arial", 12))
        not_found_.place(x=150, y=455)
        not_found_.config(foreground="red")
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    customer_lbl = ttk.Label(popup, text="Замовник:", font=("Arial", 14))
    customer_lbl.place(x=10, y=115)
    cst_name = ttk.Combobox(popup, width=28, values=[el[0] for el in customers_all], style="TCombobox")
    cst_name.place(x=175, y=115)

    # "№", "Склад", "Номер", "Замовник", "Продукція", "Кількість", "Ціна/од", "Сума", "Водій", "Транспорт", "Дата"
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.place(x=10, y=165)

    enter_name = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_name.place(x=175, y=165)

    def load_data_prod(event):
        cat_names_upd = execute_sql_query_get(conn_str, f"SELECT Назва_продукції FROM Продукція WHERE Код_складу = '{self.current_sclad_id}'")
        if not cat_names_upd:
            not_found_prod = Label(popup, text="Продукція відсутня на складі", font=("Arial", 12))
            not_found_prod.place(x=150, y=455)
            not_found_prod.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_name['values'] = [el[0] for el in cat_names_upd]

    enter_name.bind("<Button-1>", load_data_prod)

   # enter_name.current(0)

    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=215)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.place(x=175, y=215)

    add_cat_btn = Button(popup, image=self.add_prod_im, command=open_add_prod_form, width=30, height=30)
    add_cat_btn.place(x=390, y=164)
    add_cat_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_dr_btn = Button(popup, image=self.add_prod_im, command=open_add_dr_form, width=30, height=30)
    add_dr_btn.place(x=390, y=313)
    add_dr_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_avto_btn = Button(popup, image=self.add_prod_im, command=open_add_avto_form, width=30, height=30)
    add_avto_btn.place(x=390, y=363)
    add_avto_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_cst_btn = Button(popup, image=self.add_prod_im, command=open_add_cust_form, width=30, height=30)
    add_cst_btn.place(x=390, y=113)
    add_cst_btn.config(background="White", highlightbackground="White", activebackground="white")


    price_lbl = ttk.Label(popup, text="Ціна/од:", font=("Arial", 14))
    price_lbl.place(x=10, y=265)
    enter_price = Entry(popup, width=17, font=("Arial", 14))
    enter_price.place(x=175, y=265)
    # Check if a price was found
    # Function to fetch and display price per unit when a product is selected


    driver_l = ttk.Label(popup, text="Водій:", font=("Arial", 14))
    driver_l.place(x=10, y=315)

    enter_driver = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_driver.place(x=175, y=315)

    def load_data_dr(event):
        dr_names_upd = execute_sql_query_get(conn_str,
                                              f"SELECT ПІБ_водія FROM Водій")
        if not dr_names_upd:
            not_found_dr = Label(popup, text="Водіїв немає", font=("Arial", 12))
            not_found_dr.place(x=150, y=495)
            not_found_dr.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_driver['values'] = [el[0] for el in dr_names_upd]

    enter_driver.bind("<Button-1>", load_data_dr)

    ts_lbl = ttk.Label(popup, text="Транспорт:", font=("Arial", 14))
    ts_lbl.place(x=10, y=365)

    enter_ts = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_ts.place(x=175, y=365)

    def load_data_ts(event):
        ts_names_upd = execute_sql_query_get(conn_str,
                                             f"SELECT Назва_транспорту FROM Автотранспорт")
        if not ts_names_upd:
            not_found_ts = Label(popup, text="Транспорту немає", font=("Arial", 12))
            not_found_ts.place(x=180, y=495)
            not_found_ts.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_ts['values'] = [el[0] for el in ts_names_upd]

    enter_ts.bind("<Button-1>", load_data_ts)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=415)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.place(x=175, y=415)

    sum_label = ttk.Label(popup, text="Сума:", font=("Arial", 14))
    sum_label.place(x=10, y=465)
    enter_sum = Entry(popup, width=17, font=("Arial", 14))
    enter_sum.place(x=175, y=465)

    enter_count.bind("<KeyRelease>", calculate_total)

    enter_name.bind("<<ComboboxSelected>>", calculate_total)

    def check_product_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_name.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)

        if not kod_pr:
            error_label_name = Label(popup, text="Такої продукції не має на складі")
            error_label_name.place(x=180, y=194)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_name.config(style="Custom.TCombobox")

    enter_name.bind("<KeyRelease>", check_product_availability)
    enter_name.bind("<<ComboboxSelected>>", calculate_total)
    enter_count.bind("<KeyRelease>", calculate_total)

    def check_customer_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(cst_name, 'error_label_name'):
            cst_name.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            cst_name.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_замовника FROM Замовник WHERE ПІБ_контактної_особи = '{cst_name.get()}' "
        kod_cst = execute_sql_query_get(conn_str, sql_name)

        if not kod_cst:
            error_label_name = Label(popup, text="Такого замовника не має на складі")
            error_label_name.place(x=180, y=143)
            error_label_name.config(foreground="red")
            cst_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            cst_name.config(style="Custom.TCombobox")
    # Проверяем, получена ли цена за единицу продукции
    cst_name.bind("<KeyRelease>", check_customer_availability)
    cst_name.bind("<<ComboboxSelected>>", check_customer_availability)

    def check_driver_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_driver, 'error_label_name'):
            enter_driver.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_driver.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_водія FROM Водій WHERE ПІБ_водія = '{enter_driver.get()}' "
        kod_dr = execute_sql_query_get(conn_str, sql_name)

        if not kod_dr:
            error_label_name = Label(popup, text="Такого водія немає")
            error_label_name.place(x=195, y=344)
            error_label_name.config(foreground="red")
            enter_driver.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_driver.config(style="Custom.TCombobox")

    # Проверяем, получена ли цена за единицу продукции
    enter_driver.bind("<<ComboboxSelected>>", check_driver_availability)
    enter_driver.bind("<KeyRelease>", check_driver_availability)


    def check_ts_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_ts, 'error_label_name'):
            enter_ts.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_ts.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_транспорту FROM Автотранспорт WHERE Назва_транспорту = '{enter_ts.get()}' "
        kod_ts = execute_sql_query_get(conn_str, sql_name)

        if not kod_ts:
            error_label_name = Label(popup, text="Такого транспорту немає")
            error_label_name.place(x=195, y=394)
            error_label_name.config(foreground="red")
            enter_ts.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_ts.config(style="Custom.TCombobox")
    # Проверяем, получена ли цена за единицу продукции
    enter_ts.bind("<KeyRelease>", check_ts_availability)
    enter_ts.bind("<<ComboboxSelected>>", check_ts_availability)

    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add_data)
    btn_go.place(x=190, y=510)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 605
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x() + 850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)


def change_ttn(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування")
    def calculate_total(event=None):
        if enter_count.get() and enter_name.get():
            sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}'" \
                           f"AND Код_складу = '{self.current_sclad_id}'"
            print("SQL query for price:", sql_th_price)
            price = execute_sql_query_get(conn_str, sql_th_price)
            print("Price:", price)

            if price and enter_count.get():
                try:
                    # Преобразуем строку цены в число
                    price_per_unit = price[0][0]

                    # Рассчитываем общую сумму как произведение цены за единицу на количество
                    general_sum = price_per_unit * int(enter_count.get())
                    print("Общая сумма:", general_sum)

                    # Помещаем рассчитанное значение суммы в соответствующий виджет
                    enter_sum.delete(0, END)  # Очищаем поле ввода суммы
                    enter_sum.insert(0, general_sum)  # Устанавливаем новое значение суммы
                except ValueError:
                    print("Ошибка: Неправильный формат цены за единицу или количества")
            #else:
               # error_lable_name = Label(popup, text="Такої продукції не має на складі")
               # error_lable_name.place(x=180, y=143)
                #error_lable_name.config(foreground="red")

    def save_data_fottime():
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_cst = cst_name.get()
        self.entered_data = enter_data.entry.get()
        self.entered_sum = enter_sum.get()
        self.entered_price = enter_price.get()
        self.entered_driver = enter_driver.get()
        self.entered_number_ord = enter_number_ord.get()
        self.entered_ts = enter_ts.get()

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
            if hasattr(popup, 'error_lable'):
                popup.error_lable.destroy()

            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_data.entry.config(style="Custom.TCombobox")
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            cst_name.config(style="Custom.TCombobox")
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_driver.config(style="Custom.TCombobox")
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_ts.config(style="Custom.TCombobox")

            enter_number_ord.config(highlightbackground="lightgray")
            enter_count.config(highlightbackground="lightgray")
            enter_price.config(highlightbackground="lightgray")

            all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(), enter_price.get(),
                          enter_name.get(), cst_name.get(), enter_driver.get(), enter_ts.get()]

            error_lable = Label(popup, text="")

            empty_fields = []
            for i, label in enumerate(all_labels):
                if not label:
                    empty_fields.append(i)

            order_number = enter_number_ord.get()
            sql_query = f"SELECT * FROM ТТН WHERE Номер_ТТН = '{order_number}'"
            result = execute_sql_query_get(conn_str, sql_query)

            if hasattr(enter_number_ord, 'error_label_name'):
                enter_number_ord.error_label_name.destroy()

            enter_number_ord.config(highlightbackground="lightgray", highlightcolor="lightgray")
            if len(result) > 0:
                error_label_name = Label(popup, text="Такий номер ТТН вже існує")
                error_label_name.place(x=200, y=93)
                error_label_name.config(foreground="red")
                enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                enter_number_ord.error_label_name = error_label_name

                return

            if empty_fields:
                style = ttk.Style()
                style.configure("Custom.TCombobox", bordercolor="red")
                print("Следующие поля не заполнены:")
                print(empty_fields)
                for field_index in empty_fields:
                    if field_index == 0:
                        enter_data.entry.config(style="Custom.TCombobox")
                    elif field_index == 1:
                        enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 2:
                        enter_count.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 3:
                        enter_price.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 4:
                        enter_name.config(style="Custom.TCombobox")
                    elif field_index == 5:
                        cst_name.config(style="Custom.TCombobox")
                    elif field_index == 6:
                        enter_driver.config(style="Custom.TCombobox")
                    elif field_index == 7:
                        enter_ts.config(style="Custom.TCombobox")

                error_lable.config(foreground="red", text="Пропущені поля")
                error_lable.place(x=190, y=550)
                popup.error_lable = error_lable  # Сохраняем ссылку на метку в объекте окна
                return
            else:
                if not check_validate():
                    return
                print("Все поля заполнены.")

            sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
            kod_pr = execute_sql_query_get(conn_str, sql_name)

            sql_name = f"SELECT Код_водія FROM Водій WHERE ПІБ_водія = '{enter_driver.get()}' "
            kod_dr = execute_sql_query_get(conn_str, sql_name)

            sql_name = f"SELECT Код_замовника FROM Замовник WHERE ПІБ_контактної_особи = '{cst_name.get()}' "
            kod_cst = execute_sql_query_get(conn_str, sql_name)

            sql_name = f"SELECT Код_транспорту FROM Автотранспорт WHERE Назва_транспорту = '{enter_ts.get()}' "
            kod_ts = execute_sql_query_get(conn_str, sql_name)
            # Получаем код продукции из базы данных

            sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
            print("SQL query for price:", sql_th_price)
            price = execute_sql_query_get(conn_str, sql_th_price)
            print("Price:", price)

            #INSERT INTO ТТН (Дата, Номер_ТТН, Кількість_палетів_, Ціна_за_од, Сума, Код_замовника, Код_складу, Код_продукції, Код_водія, Код_транспорту)
            sql_update_prod = f"""
                    UPDATE ТТН
                    SET Дата = '{enter_data.entry.get()}',
                        Номер_ТТН = '{enter_number_ord.get()}',
                        Кількість_палетів_ = '{enter_count.get()}',
                        Ціна_за_од = '{enter_price.get()}',
                        Сума = '{enter_sum.get()}',
                        Код_замовника = '{kod_cst[0][0]}',
                        Код_складу = '{self.current_sclad_id}',
                        Код_продукції = '{kod_pr[0][0]}',
                        Код_водія = '{kod_dr[0][0]}',
                        Код_транспорту = '{kod_ts[0][0]}'
                    WHERE Код_ТТН = '{self.item_text[0]}'
                """

            execute_sql_query_insert(conn_str, sql_update_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_ttn_menu()

        except TypeError:
            add_data()

    def open_add_prod_form():
        save_data_fottime()
        add_prod(popup,self)
        popup.withdraw()

    def open_add_th_form():
        save_data_fottime()
        add_save_th(popup,self)
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

        if hasattr(enter_sum, 'error_label'):
            enter_sum.error_label.destroy()
            enter_sum.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_price, 'error_label'):
            enter_price.error_label.destroy()
            enter_price.config(highlightbackground="lightgray", highlightcolor="black")
        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()
        summa = enter_sum.get().strip()
        price = enter_price.get().strip()
        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not price.isdigit():
            error_value_list.append(count_value)
            enter_price.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_price.error_label = error_label

        if not summa.isdigit():
            error_value_list.append(count_value)
            enter_sum.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_sum.error_label = error_label

        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=155, y=550)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label
        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Редагування ТТН", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер ТТН:", font=("Arial", 14))
    number_ord.place(x=10, y=65)
    enter_number_ord = Entry(popup, width=17, font=("Arial", 14))
    enter_number_ord.insert(0, f"{self.item_text[1]}")
    enter_number_ord.place(x=175, y=65)

    customers_all = None
    while customers_all is None:
        customers_all = execute_sql_query_get(conn_str, f"SELECT ПІБ_контактної_особи FROM Замовник")
    if not customers_all:
        not_found_ = Label(popup, text="Замовників не має", font=("Arial", 12))
        not_found_.place(x=150, y=455)
        not_found_.config(foreground="red")
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    customer_lbl = ttk.Label(popup, text="Замовник:", font=("Arial", 14))
    customer_lbl.place(x=10, y=115)
    cst_name = ttk.Combobox(popup, width=28, values=[el[0] for el in customers_all], style="TCombobox")
    cst_name.insert(0, f"{self.item_text[3]}")
    cst_name.place(x=175, y=115)

    # "№", "Склад", "Номер", "Замовник", "Продукція", "Кількість", "Ціна/од", "Сума", "Водій", "Транспорт", "Дата"
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.place(x=10, y=165)

    enter_name = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_name.insert(0, f"{self.item_text[4]}")
    enter_name.place(x=175, y=165)

    def load_data_prod(event):
        cat_names_upd = execute_sql_query_get(conn_str,
                                              f"SELECT Назва_продукції FROM Продукція WHERE Код_складу = '{self.current_sclad_id}'")
        if not cat_names_upd:
            not_found_prod = Label(popup, text="Продукція відсутня на складі", font=("Arial", 12))
            not_found_prod.place(x=150, y=455)
            not_found_prod.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_name['values'] = [el[0] for el in cat_names_upd]

    enter_name.bind("<Button-1>", load_data_prod)

    # enter_name.current(0)

    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=215)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.insert(0, f"{self.item_text[5]}")
    enter_count.place(x=175, y=215)

    add_cat_btn = Button(popup, image=self.add_prod_im, command=open_add_prod_form, width=30, height=30)
    add_cat_btn.place(x=390, y=265)
    add_cat_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_th_btn = Button(popup, image=self.add_prod_im, command=open_add_th_form, width=30, height=30)
    add_th_btn.place(x=390, y=265)
    add_th_btn.config(background="White", highlightbackground="White", activebackground="white")

    price_lbl = ttk.Label(popup, text="Ціна/од:", font=("Arial", 14))
    price_lbl.place(x=10, y=265)
    enter_price = Entry(popup, width=17, font=("Arial", 14))
    enter_price.insert(0, f"{self.item_text[6]}")
    enter_price.place(x=175, y=265)
    # Check if a price was found
    # Function to fetch and display price per unit when a product is selected

    driver_l = ttk.Label(popup, text="Водій:", font=("Arial", 14))
    driver_l.place(x=10, y=315)

    enter_driver = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_driver.insert(0, f"{self.item_text[8]}")
    enter_driver.place(x=175, y=315)

    def load_data_dr(event):
        dr_names_upd = execute_sql_query_get(conn_str,
                                             f"SELECT ПІБ_водія FROM Водій")
        if not dr_names_upd:
            not_found_dr = Label(popup, text="Водіїв немає", font=("Arial", 12))
            not_found_dr.place(x=150, y=495)
            not_found_dr.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_driver['values'] = [el[0] for el in dr_names_upd]

    enter_driver.bind("<Button-1>", load_data_dr)

    ts_lbl = ttk.Label(popup, text="Транспорт:", font=("Arial", 14))
    ts_lbl.place(x=10, y=365)

    enter_ts = ttk.Combobox(popup, width=28, style="TCombobox")
    enter_ts.insert(0, f"{self.item_text[9]}")
    enter_ts.place(x=175, y=365)

    def load_data_ts(event):
        ts_names_upd = execute_sql_query_get(conn_str,
                                             f"SELECT Назва_транспорту FROM Автотранспорт")
        if not ts_names_upd:
            not_found_ts = Label(popup, text="Транспорту немає", font=("Arial", 12))
            not_found_ts.place(x=150, y=495)
            not_found_ts.config(foreground="red")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_ts['values'] = [el[0] for el in ts_names_upd]

    enter_ts.bind("<Button-1>", load_data_ts)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=415)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.entry.delete(0,"end")
    enter_data.entry.insert(0, f"{self.item_text[10]}")
    enter_data.place(x=175, y=415)

    sum_label = ttk.Label(popup, text="Сума:", font=("Arial", 14))
    sum_label.place(x=10, y=465)
    enter_sum = Entry(popup, width=17, font=("Arial", 14))
    enter_sum.insert(0, f"{self.item_text[7]}")
    enter_sum.place(x=175, y=465)

    enter_count.bind("<KeyRelease>", calculate_total)

    enter_name.bind("<<ComboboxSelected>>", calculate_total)

    def check_product_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_name.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)

        if not kod_pr:
            error_label_name = Label(popup, text="Такої продукції не має на складі")
            error_label_name.place(x=180, y=194)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_name.config(style="Custom.TCombobox")

    enter_name.bind("<KeyRelease>", check_product_availability)
    enter_name.bind("<<ComboboxSelected>>", calculate_total)
    enter_count.bind("<KeyRelease>", calculate_total)

    def check_customer_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(cst_name, 'error_label_name'):
            cst_name.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            cst_name.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_замовника FROM Замовник WHERE ПІБ_контактної_особи = '{cst_name.get()}' "
        kod_cst = execute_sql_query_get(conn_str, sql_name)

        if not kod_cst:
            error_label_name = Label(popup, text="Такого замовника не має на складі")
            error_label_name.place(x=180, y=143)
            error_label_name.config(foreground="red")
            cst_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            cst_name.config(style="Custom.TCombobox")

    # Проверяем, получена ли цена за единицу продукции
    cst_name.bind("<KeyRelease>", check_customer_availability)
    cst_name.bind("<<ComboboxSelected>>", check_customer_availability)

    def check_driver_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_driver, 'error_label_name'):
            enter_driver.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_driver.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_водія FROM Водій WHERE ПІБ_водія = '{enter_driver.get()}' "
        kod_dr = execute_sql_query_get(conn_str, sql_name)

        if not kod_dr:
            error_label_name = Label(popup, text="Такого водія немає")
            error_label_name.place(x=195, y=344)
            error_label_name.config(foreground="red")
            enter_driver.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_driver.config(style="Custom.TCombobox")

    # Проверяем, получена ли цена за единицу продукции
    enter_driver.bind("<<ComboboxSelected>>", check_driver_availability)
    enter_driver.bind("<KeyRelease>", check_driver_availability)

    def check_ts_availability(event):
        new_combostyle = ttk.Style()
        new_combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
        if hasattr(enter_ts, 'error_label_name'):
            enter_ts.error_label_name.destroy()
            combostyle.configure("CustomGray.TCombobox", bordercolor="lightgray")
            enter_ts.config(style="CustomGray.TCombobox")

        sql_name = f"SELECT Код_транспорту FROM Автотранспорт WHERE Назва_транспорту = '{enter_ts.get()}' "
        kod_ts = execute_sql_query_get(conn_str, sql_name)

        if not kod_ts:
            error_label_name = Label(popup, text="Такого транспорту немає")
            error_label_name.place(x=195, y=394)
            error_label_name.config(foreground="red")
            enter_ts.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_ts.config(style="Custom.TCombobox")

    # Проверяем, получена ли цена за единицу продукции
    enter_ts.bind("<KeyRelease>", check_ts_availability)
    enter_ts.bind("<<ComboboxSelected>>", check_ts_availability)

    btn_go = Button(popup, text="Редагувати",font=("Arial",14),width=10, command=add_data)
    btn_go.place(x=195,y=500)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 600
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x()+850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)
