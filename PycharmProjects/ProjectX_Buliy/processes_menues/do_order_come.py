from datetime import date
from tkinter import Button,Label,Entry, Toplevel, END

from processes_menues.do_save_thona import add_save_th
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from processes_menues.do_product import add_prod
from short_inf_popups import wrong_data


def update_product_stock(product_name, pallets_count):
    # Получаем информацию о продукции по названию
    get_product_info_query = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{product_name}'"
    product_info = execute_sql_query_get(conn_str, get_product_info_query)

    if product_info:
        # Получаем текущее количество палетов продукции
        current_pallets_count = product_info[0][0]  # Предполагается, что количество палетов находится на второй позиции

        # Обновляем количество палетов, добавляя количество палетов из ордера
        updated_pallets_count = current_pallets_count + pallets_count

        # Обновляем запись в таблице Продукція
        update_query = f"UPDATE Продукція SET Кількість_палетів_ = {updated_pallets_count} " \
                       f"WHERE Назва_продукції = '{product_name}'"
        execute_sql_query_insert(conn_str, update_query)

        # Выводим сообщение об успешном обновлении
        print(f"Количество палетов для продукции '{product_name}' успешно обновлено.")
    else:
        print(f"Продукция с названием '{product_name}' не найдена.")
def count_pallets(entry):
    try:
        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{entry}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        zona_code = kod_th[0][0]
        # Формируем SQL-запрос для подсчета количества палетов
        sql_count = f"SELECT SUM(Кількість_палетів_) FROM Продукція WHERE Код_зони_зберігання = {zona_code} "

        # Выполняем запрос
        result = execute_sql_query_get(conn_str, sql_count)
        total_pallets = 0
        # Получаем результат
        total_pallets += result[0][0] if result and result[0] else 0
        if total_pallets is None:
            total_pallets=0

        # Возвращаем результат
        return total_pallets
    except Exception as e:
        print(f"Ошибка при подсчете количества палетов: {e}")
        return 0
def add_order_come(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Нове надходження")

    def save_data_fottime():
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_thona = enter_thona.get()
        self.entered_data = enter_data.entry.get()
        self.entered_sum = enter_sum.get()
        self.entered_ceh = enter_ceh.get()
        self.entered_number_ord = enter_number_ord.get()
        self.entered_number_part = enter_number_part.get()


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
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()

        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_thona.config(style="Custom.TCombobox")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_name.config(style="Custom.TCombobox")

        enter_number_ord.config(highlightbackground="lightgray")
        enter_count.config(highlightbackground="lightgray")
        enter_ceh.config(highlightbackground="lightgray")
        enter_number_part.config(highlightbackground="lightgray")

        all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(), enter_ceh.get(),
                      enter_name.get(), enter_thona.get(), enter_number_part.get()]

        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)
        sql_number = f"SELECT * FROM Ордер_надходження WHERE Номер_ордеру_надходження = '{enter_number_ord.get()}'"
        present_n = execute_sql_query_get(conn_str, sql_number)
        if hasattr(enter_number_ord, 'error_lable_name'):
            enter_number_ord.error_lable_name.destroy()



        if present_n:
            error_lable_name = Label(popup, text="Такий номер ордеру вже існує")
            error_lable_name.place(x=200, y=93)
            error_lable_name.config(foreground="red")
            enter_number_ord.config(highlightbackground="red", highlightcolor="red")
            enter_number_ord.error_lable_name = error_lable_name
            return

        error_lable = Label(popup, text="")

        if empty_fields:
            print("Следующие поля не заполнены:")
            for field_index in empty_fields:
                if field_index == 0:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_data.entry.config(style="Custom.TCombobox")
                    #today_date = date.today()
                    #formatted_date = today_date.strftime("%d.%m.%Y")
                    #enter_data.entry.insert(0,formatted_date)  # Вставить новый текст
                    #popup_default_data()

                elif field_index == 1:
                    enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 2:
                    enter_count.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    enter_ceh.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 4:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_name.config(style="Custom.TCombobox")
                elif field_index == 5:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_thona.config(style="Custom.TCombobox")
                elif field_index == 6:
                    enter_number_part.config(highlightbackground="red", highlightcolor="red")


            error_lable.config(foreground="red", text="Пропущені поля")
            error_lable.place(x=165, y=470)
            popup.error_label = error_lable  # Сохраняем ссылку на метку в объекте окна
            return
        else:
            if not check_validate():
                return
            print("Все поля заполнены.")

        sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        kod_pr = execute_sql_query_get(conn_str, sql_name)
        # Получаем код продукции из базы данных

        # Получаем код зоны зберігання из базы данных
        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_thona.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)
        print("Код зоны зберігання:", kod_th[0][0])

        sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        print("SQL query for price:", sql_th_price)
        price = execute_sql_query_get(conn_str, sql_th_price)
        print("Price:", price)

        sql_paletu = f"SELECT Місткість_палетів_ FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_thona.get()}' "
        paletu = execute_sql_query_get(conn_str, sql_paletu)
        print("Місткість палетів:", paletu[0][0])
        print("Кількість:", enter_count.get())

        if not kod_th:
            wrong_data(popup)
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_thona.config(style="Custom.TCombobox")
            return

        total_count = count_pallets(enter_thona.get())
        remain_places = paletu[0][0] - total_count
        print("sum of prod", total_count)
        print(f"Залишилось місць  = {remain_places}")
        sql_current_prod_c = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        added_count = execute_sql_query_get(conn_str, sql_current_prod_c)
        #print(total_count+int(enter_count.get()),"added")


        try:
            if total_count+int(enter_count.get()) <= paletu[0][0]:
                # SQL-запрос для добавления новой записи в таблицу Продукція
                sql_add_prod = f"""
                                    INSERT INTO Ордер_надходження (Дата, Номер_ордеру_надходження,
                                     Кількість_палетів_, Сума, Цех, Номер_партії,Код_складу,Код_продукції,Код_зони_зберігання)
                                    VALUES ('{enter_data.entry.get()}', '{enter_number_ord.get()}', '{enter_count.get()}',
                                            '{enter_sum.get()}', '{enter_ceh.get()}', '{enter_number_part.get()}',
                                             '{self.current_sclad_id}', '{kod_pr[0][0]}', '{kod_th[0][0]}');"""

                execute_sql_query_insert(conn_str, sql_add_prod)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                update_product_stock(enter_name.get(),int(enter_count.get()))
                self.open_order_incm_menu()
            else:
                enter_count.config(highlightbackground="red", highlightthickness=0.5)
                error_label = Label(popup, text="ПОМИЛКА: Кіл-ть палетів більше ніж має зона зберігання")
                error_label.place(x=90, y=328)
                error_label.config(foreground="red")
                popup.error_label = error_label
        except Exception as e:
            error_lable_name = Label(popup, text="ПОМИЛКА: Кіл-ть палетів більше ніж має зона зберігання")
            error_lable_name.place(x=90, y=328)
            error_lable_name.config(foreground="red")


    def calculate_total(event):
        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_name.config(style="Custom.TCombobox")

        if enter_count.get() and enter_name.get():
            check_product_availability(None)
            sql_th_price = f"SELECT Ціна_за_од FROM Продукція WHERE Назва_продукції = '{enter_name.get()}'" \
                           f"AND Код_складу = '{self.current_sclad_id}'"

            price = execute_sql_query_get(conn_str, sql_th_price)

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

    # Привязываем функцию к событиям изменения в полях ввода количества и названия продукции


    # Привязываем функцию к событиям изменения в полях ввода цены за единицу и количества

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

        if hasattr(enter_number_part, 'error_label'):
            enter_number_part.error_label.destroy()
            enter_number_part.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()
        number_part = enter_number_part.get().strip()
        summa = enter_sum.get().strip()
        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=520)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not summa.isdigit():
            error_value_list.append(count_value)
            enter_sum.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=145, y=520)
            error_label.config(foreground="red")
            enter_sum.error_label = error_label

        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=520)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label

        if not number_part.isdigit():
            error_value_list.append(number_part)
            enter_number_part.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=450)
            error_label.config(foreground="red")
            enter_number_part.error_label = error_label
        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Додавання надходження", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер ордеру:", font=("Arial", 14))
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

   # enter_name.current(0)

    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=165)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.place(x=175, y=165)

    add_cat_btn = Button(popup, image=self.add_prod_im, command=open_add_prod_form, width=30, height=30)
    add_cat_btn.place(x=390, y=115)
    add_cat_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_th_btn = Button(popup, image=self.add_prod_im, command=open_add_th_form, width=30, height=30)
    add_th_btn.place(x=390, y=215)
    add_th_btn.config(background="White", highlightbackground="White", activebackground="white")

    thona_names = None
    while thona_names is None:
        thona_names = execute_sql_query_get(conn_str, "SELECT Назва_зони_зберігання FROM Зона_зберігання"
                                                      f" WHERE Код_складу = '{self.current_sclad_id}' ")
    thona = ttk.Label(popup, text="Зона зберігання:", font=("Arial", 14))
    thona.place(x=10, y=215)
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 12))
    enter_thona = ttk.Combobox(popup, width=28, values=[el[0] for el in thona_names], style="TCombobox")
    enter_thona.place(x=175, y=215)

    ceh_name = ttk.Label(popup, text="Цех:", font=("Arial", 14))
    ceh_name.place(x=10, y=265)
    enter_ceh = Entry(popup, width=17, font=("Arial", 14))
    enter_ceh.place(x=175, y=265)

    number_part = ttk.Label(popup, text="Номер партії:", font=("Arial", 14))
    number_part.place(x=10, y=315)
    enter_number_part = Entry(popup, width=17, font=("Arial", 14))
    enter_number_part.place(x=175, y=315)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=365)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.place(x=175, y=365)

    sum_label = ttk.Label(popup, text="Сума:", font=("Arial", 14))
    sum_label.place(x=10, y=415)
    enter_sum = Entry(popup, width=17, font=("Arial", 14))
    enter_sum.place(x=175, y=415)

    enter_count.bind("<KeyRelease>", calculate_total)

    enter_name.bind("<<ComboboxSelected>>", calculate_total)



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
    enter_name.bind("<<ComboboxSelected>>", calculate_total)
    enter_count.bind("<KeyRelease>", calculate_total)

    def check_thona_availability(event):

        if hasattr(enter_thona, 'error_label_name'):
            enter_thona.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_thona.config(style="Custom.TCombobox")

        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_thona.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        if not kod_th:
            error_label_name = Label(popup, text="Такої зони зберігання  не існує на складі")
            error_label_name.place(x=170, y=243)
            error_label_name.config(foreground="red")
            enter_thona.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_thona.config(style="Custom.TCombobox")

    enter_thona.bind("<KeyRelease>", check_thona_availability)
    enter_thona.bind("<<ComboboxSelected>>", check_thona_availability)
    # Проверяем, получена ли цена за единицу продукции


    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add_data)
    btn_go.place(x=190, y=515)

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


def change_order_come(root, self):
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
        #enter_name.delete(0, "end")
        #enter_count.delete(0, "end")
        self.entered_name_prod = enter_name.get()
        self.entered_count_prod = enter_count.get()
        self.entered_thona = enter_thona.get()
        self.entered_data = enter_data.entry.get()
        self.entered_sum = enter_sum.get()
        self.entered_ceh = enter_ceh.get()
        self.entered_number_ord = enter_number_ord.get()
        self.entered_number_part = enter_number_part.get()

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

            all_labels = [enter_data.entry.get(), enter_number_ord.get(), enter_count.get(), enter_ceh.get(),
                          enter_name.get(), enter_thona.get(), enter_number_part.get()]


            empty_fields = []
            for i, label in enumerate(all_labels):
                if not label:
                    empty_fields.append(i)

            error_lable = Label(popup, text="")

            if empty_fields:
                print("Следующие поля не заполнены:")
                for field_index in empty_fields:
                    if field_index == 0:
                        today_date = date.today()
                        enter_data.entry.insert(0, today_date)  # Вставить новый текст
                    elif field_index == 1:
                        enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 2:
                        enter_count.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 3:
                        enter_ceh.config(highlightbackground="red", highlightcolor="red")
                    elif field_index == 4:
                        combostyle.configure("Custom.TCombobox", bordercolor="red")
                        enter_name.config(style="Custom.TCombobox")
                    elif field_index == 5:
                        combostyle.configure("Custom.TCombobox", bordercolor="red")
                        enter_thona.config(style="Custom.TCombobox")
                    elif field_index == 6:
                        enter_number_part.config(highlightbackground="red", highlightcolor="red")


                error_lable.config(foreground="red", text="Пропущені поля")
                error_lable.place(x=165, y=470)
                popup.error_label = error_lable  # Сохраняем ссылку на метку в объекте окна
                return
            else:
                if not check_validate():
                    return


            # Получаем код категории из базы данных
            sql_name = f"SELECT Код_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
            kod_prod = execute_sql_query_get(conn_str, sql_name)

            # Получаем код зоны зберігання из базы данных
            sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = " \
                     f"'{enter_thona.get()}' "
            kod_th = execute_sql_query_get(conn_str, sql_th)

            # SQL-запрос для обновления записи в таблице Продукція
            sql_paletu = f"SELECT Місткість_палетів_ FROM Зона_зберігання WHERE Назва_зони_зберігання = " \
                         f"'{enter_thona.get()}' "
            paletu = execute_sql_query_get(conn_str, sql_paletu)


            if not kod_th:
                wrong_data(popup)
                combostyle.configure("Custom.TCombobox", bordercolor="red")
                enter_thona.config(style="Custom.TCombobox")
                return

            total_count = count_pallets(enter_thona.get())

            print("sum",total_count)
            remain_places = paletu[0][0] - total_count
            print("sum of prod", total_count)
            print(f"Залишилось місць  = {remain_places}")

            order_number = enter_number_ord.get()
            sql_query = f"SELECT * FROM Ордер_надходження WHERE Номер_ордеру_надходження = '{order_number}'"
            result = execute_sql_query_get(conn_str, sql_query)

            if hasattr(enter_number_ord, 'error_label_name'):
                enter_number_ord.error_label_name.destroy()
            enter_count.config(highlightbackground="lightgray", highlightthickness=0.5)
            enter_number_ord.config(highlightbackground="lightgray", highlightcolor="lightgray")
            if len(result) > 0:
                error_label_name = Label(popup, text="Такий номер ордеру вже існує")
                error_label_name.place(x=200, y=93)
                error_label_name.config(foreground="red")
                enter_number_ord.config(highlightbackground="red", highlightcolor="red")
                enter_number_ord.error_label_name = error_label_name
                return

            error_lable = Label(popup, text="")
            if int(enter_count.get())+total_count<= paletu[0][0]:
                sql_update_prod = f"""
                        UPDATE Ордер_надходження
                        SET Дата = '{enter_data.entry.get()}',
                            Номер_ордеру_надходження = '{enter_number_ord.get()}',
                            Кількість_палетів_ = '{enter_count.get()}',
                            Сума = '{enter_sum.get()}',
                            Цех = '{enter_ceh.get()}',
                            Код_складу = '{self.current_sclad_id}',
                            Номер_партії = '{enter_number_part.get()}',
                            Код_продукції = '{kod_prod[0][0]}',
                            Код_зони_зберігання = '{kod_th[0][0]}'
                        WHERE Код_ордеру_надходження = '{self.item_text[0]}'
                    """

                execute_sql_query_insert(conn_str, sql_update_prod)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                update_product_stock(enter_name.get(), int(enter_count.get()))
                self.open_order_incm_menu()
            else:
                enter_count.config(highlightbackground="red", highlightthickness=0.5)
                error_lable = Label(popup,text="ПОМИЛКА: Кіл-ть палетів більше ніж має зона зберігання")
                error_lable.place(x=90,y=455)
                error_lable.config(foreground="red")
                popup.error_lable = error_lable
        except Exception as ex:
            print(ex)

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

        if hasattr(enter_number_part, 'error_label'):
            enter_number_part.error_label.destroy()
            enter_number_part.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_sum, 'error_label'):
            enter_sum.error_label.destroy()
            enter_sum.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        number_value = enter_number_ord.get().strip()
        number_part = enter_number_part.get().strip()
        summa = enter_sum.get().strip()
        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=450)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not number_value.isdigit():
            error_value_list.append(number_value)
            enter_number_ord.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=450)
            error_label.config(foreground="red")
            enter_number_ord.error_label = error_label

        if not summa.isdigit():
            error_value_list.append(count_value)
            enter_sum.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=145, y=348)
            error_label.config(foreground="red")
            enter_sum.error_label = error_label

        if not number_part.isdigit():
            error_value_list.append(number_part)
            enter_number_part.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=165, y=450)
            error_label.config(foreground="red")
            enter_number_part.error_label = error_label



        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Редагування надходження", font=("Arial", 20, "bold")).pack()

    number_ord = ttk.Label(popup, text="Номер ордеру:", font=("Arial", 14))
    number_ord.place(x=10, y=65)
    enter_number_ord = Entry(popup, width=17, font=("Arial", 14))
    enter_number_ord.insert(0, f"{self.item_text[1]}")
    enter_number_ord.place(x=175, y=65)

    prod_names = execute_sql_query_get(conn_str, f"SELECT Назва_продукції FROM Продукція"
                                                 f" WHERE Код_складу = '{self.current_sclad_id}'")
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.place(x=10, y=115)
    enter_name = ttk.Combobox(popup, width=28, values=[el[0] for el in prod_names], style="TCombobox")
    enter_name.insert(0, f"{self.item_text[2]}")
    enter_name.place(x=175, y=115)


    count_prod = ttk.Label(popup, text="Кількість:", font=("Arial", 14))
    count_prod.place(x=10, y=165)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.insert(0, f"{self.item_text[3]}")
    enter_count.place(x=175, y=165)


    add_prod_btn = Button(popup, image=self.add_prod_im, command=open_add_prod_form, width=30, height=30)
    add_prod_btn.place(x=390, y=115)
    add_prod_btn.config(background="White", highlightbackground="White", activebackground="white")

    add_th_btn = Button(popup, image=self.add_prod_im, command=open_add_th_form, width=30, height=30)
    add_th_btn.place(x=390, y=215)
    add_th_btn.config(background="White", highlightbackground="White", activebackground="white")

    thona_names = execute_sql_query_get(conn_str, "SELECT Назва_зони_зберігання FROM Зона_зберігання"
                                                  f" WHERE Код_складу = '{self.current_sclad_id}' ")
    thona = ttk.Label(popup, text="Зона зберігання:", font=("Arial", 14))
    thona.place(x=10, y=215)
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 12))
    enter_thona = ttk.Combobox(popup, width=28, values=[el[0] for el in thona_names], style="TCombobox")
    enter_thona.insert(0, f"{self.item_text[5]}")
    enter_thona.place(x=175, y=215)


    im = self.back

    ceh_name = ttk.Label(popup, text="Цех:", font=("Arial", 14))
    ceh_name.place(x=10, y=265)
    enter_ceh = Entry(popup, width=17, font=("Arial", 14))
    enter_ceh.insert(0, f"{self.item_text[6]}")
    enter_ceh.place(x=175, y=265)

    number_part = ttk.Label(popup, text="Номер партії:", font=("Arial", 14))
    number_part.place(x=10, y=315)
    enter_number_part = Entry(popup, width=17, font=("Arial", 14))
    enter_number_part.insert(0, f"{self.item_text[7]}")
    enter_number_part.place(x=175, y=315)

    data_time = ttk.Label(popup, text="Дата:", font=("Arial", 14))
    data_time.place(x=10, y=365)
    enter_data = ttk.DateEntry(popup, width=24, borderwidth=1)
    enter_data.entry.delete(0, "end")
    enter_data.entry.insert(0, f"{self.item_text[8]}")
    enter_data.place(x=175, y=365)

    sum_label = ttk.Label(popup, text="Сума:", font=("Arial", 14), state='disabled')
    sum_label.place(x=10, y=415)
    enter_sum = Entry(popup, width=17, font=("Arial", 14))
    enter_sum.place(x=175, y=415)
    calculate_total()


    enter_count.bind("<KeyRelease>", calculate_total)
    enter_name.bind("<<ComboboxSelected>>", calculate_total)

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
    enter_name.bind("<<ComboboxSelected>>", check_product_availability)

    def check_product_availability(event):

        if hasattr(enter_thona, 'error_label_name'):
            enter_thona.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_thona.config(style="Custom.TCombobox")

        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_thona.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        if not kod_th:
            error_label_name = Label(popup, text="Такої зони зберігання  не існує на складі")
            error_label_name.place(x=170, y=243)
            error_label_name.config(foreground="red")
            enter_thona.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_thona.config(style="Custom.TCombobox")

    enter_thona.bind("<KeyRelease>", check_product_availability)
    enter_thona.bind("<<ComboboxSelected>>", check_product_availability)

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
