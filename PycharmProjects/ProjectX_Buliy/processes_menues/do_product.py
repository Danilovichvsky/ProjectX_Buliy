from tkinter import Entry
import string
import random



from processes_menues.do_category import add_category
from processes_menues.do_save_thona import *
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *


def count_pallets(entry):
    try:
        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{entry.get().replace(' ','')}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        zona_code = kod_th[0][0]
        # Формируем SQL-запрос для подсчета количества палетов
        sql_count = f"SELECT SUM(Кількість_палетів_) FROM Продукція WHERE Код_зони_зберігання = {zona_code} "

        # Выполняем запрос
        result = execute_sql_query_get(conn_str, sql_count)

        # Получаем результат
        total_pallets = result[0][0] if result and result[0] else 0
        if total_pallets is None:
            total_pallets=0

        # Возвращаем результат
        return total_pallets
    except Exception as e:
        print(f"Ошибка при подсчете количества палетов: {e}")
        return 0


def add_prod(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування продукту")

    def on_close():
        # Здесь отключаем кнопку del_items
        self.del_items.config(state="normal")
        self.change_items.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)
    def generate_unique_article():
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            # Проверяем уникальность артикула в базе данных
            sql_check_article = f"SELECT COUNT(*) FROM Продукція WHERE Артикул = '{random_string}'"
            result = execute_sql_query_get(conn_str, sql_check_article)
            if result[0][0] == 0:  # Если артикул уникален
                return random_string

    def add_data():
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_category.config(style="Custom.TCombobox")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_th.config(style="Custom.TCombobox")

        enter_name.config(highlightbackground="lightgray")
        enter_price.config(highlightbackground="lightgray")
        enter_count.config(highlightbackground="lightgray")

        if hasattr(popup, 'error_lable'):
            popup.error_lable.destroy()

        random_string = generate_unique_article()
        print(random_string)

        all_labels = [enter_name.get(), enter_count.get(), enter_price.get(), enter_category.get(), enter_th.get()]

        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)

        error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
        popup.error_lable = error_lable
        if error_lable.winfo_ismapped():
            error_lable.destroy()


        if empty_fields:
            for field_index in empty_fields:
                if field_index == 0:
                    enter_name.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 1:
                    enter_count.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 2:
                    enter_price.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_category.config(style="Custom.TCombobox")
                elif field_index == 4:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_th.config(style="Custom.TCombobox")

            error_lable.place(x=190, y=328)
            error_lable.config(foreground="red")

            return
        else:
            if not check_validate():
                return

        # enter_count.config(highlightbackground=None, highlightthickness=0.5)

        # Получаем код категории из базы данных
        sql_cat = f"SELECT Код_категорії FROM Категорія WHERE Категорія = '{enter_category.get()}' "
        kod_cat = execute_sql_query_get(conn_str, sql_cat)

        # Получаем код зоны зберігання из базы данных
        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        sql_paletu = f"SELECT Місткість_палетів_ FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        paletu = execute_sql_query_get(conn_str, sql_paletu)

        if not kod_cat or not kod_th:
            wrong_data(popup)
            if not kod_cat:
                combostyle.configure("Custom.TCombobox", bordercolor="red")
                enter_category.config(style="Custom.TCombobox")
            if not kod_th:
                combostyle.configure("Custom.TCombobox", bordercolor="red")
                enter_th.config(style="Custom.TCombobox")
            return

        total_count = count_pallets(enter_th)

        # if not total_count:
        # total_count = 0
        def back_form():
            popup.destroy()
            # root.deiconify()
            self.btn_add_prod.config(state="normal")

        if (int(enter_count.get().replace(" ", "")) + total_count) <= paletu[0][0]:
            # SQL-запрос для добавления новой записи в таблицу Продукція
            sql_add_prod = f"""
                    INSERT INTO Продукція (Назва_продукції, Кількість_палетів_, Код_категорії, Ціна_за_од,
                                            Код_зони_зберігання, Код_складу, Артикул)
                    VALUES ('{enter_name.get()}', '{enter_count.get()}', '{kod_cat[0][0]}',
                            '{enter_price.get()}', '{kod_th[0][0]}', '{self.current_sclad_id}', '{random_string}');
                """

            execute_sql_query_insert(conn_str, sql_add_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            back_form()

            if self.zapas_menu.winfo_ismapped():
                self.zapas_menu.forget()
                self.open_zapas_menu()

        else:
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_lable = Label(popup, text="ПОМИЛКА: Кіл-ть палетів більше ніж має зона зберігання")
            error_lable.place(x=90, y=328)
            error_lable.config(foreground="red")

    def back_form():
        popup.destroy()
        self.btn_add_prod.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        #root.deiconify()

    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(enter_count, 'error_label'):
            enter_count.error_label.destroy()
            enter_count.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_price, 'error_label'):
            enter_price.error_label.destroy()
            enter_price.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        price_value = enter_price.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=325)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not price_value.isdigit():
            error_value_list.append(price_value)
            enter_price.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=325)
            error_label.config(foreground="red")
            enter_price.error_label = error_label

        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True

    ttk.Label(popup, text="Додавання продукту", font=("Arial", 20, "bold")).pack()

    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.pack(anchor="nw", padx=10, pady=30)

    # Устанавливаем текст по умолчанию в Entry
    enter_name = Entry(popup, width=17, font=("Arial", 14))
    enter_name.place(x=175, y=65)

    count_prod = ttk.Label(popup, text="Кількість(палетів):", font=("Arial", 14))
    count_prod.pack(anchor="nw", padx=10, pady=1)
    enter_count = Entry(popup, width=17, font=("Arial", 14))
    enter_count.place(x=175, y=123)

    cat_names = execute_sql_query_get(conn_str, "SELECT Код_категорії, Категорія FROM Категорія")
    categ_prod = ttk.Label(popup, text="Категорія:", font=("Arial", 14))
    categ_prod.pack(anchor="nw", padx=10, pady=30)
    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 16))
    enter_category = ttk.Combobox(popup, width=28, values=[el[1] for el in cat_names], style="TCombobox")
    enter_category.place(x=175, y=180)
    print("Selected value:", enter_category.get())
    im = self.back
    add_cat_btn = Button(popup, image=self.add_prod_im, command=lambda: add_category(popup, self), width=30, height=30)
    add_cat_btn.place(x=390, y=180)
    add_cat_btn.config(background="White", highlightbackground="White", activebackground="white")

    price_prod = ttk.Label(popup, text="Ціна (за од.):", font=("Arial", 14))
    price_prod.pack(anchor="nw", padx=10, pady=3)
    enter_price = Entry(popup, width=17, font=("Arial", 14))
    enter_price.place(x=175, y=237)

    saving_prod = ttk.Label(popup, text="Зона зберігання:", font=("Arial", 14))
    saving_prod.pack(anchor="nw", padx=10, pady=25)
    save_th = execute_sql_query_get(conn_str, f"SELECT Код_зони_зберігання, Назва_зони_зберігання FROM Зона_зберігання"
                                              f" WHERE Код_складу = {self.current_sclad_id}")
    th_el = {el for el in save_th}
    print(th_el)
    enter_th = ttk.Combobox(popup, width=28, values=[el[1] for el in save_th])
    enter_th.place(x=175, y=294)
    add_th = Button(popup, image=self.add_prod_im, command=lambda: add_save_th(popup, self), width=30, height=30)

    add_th.place(x=390, y=294)
    add_th.config(background="White", highlightbackground="White", activebackground="white")

    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0, activebackground='red',
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=23)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    def load_data_cat(event):
        cat_names_upd = execute_sql_query_get(conn_str, "SELECT Категорія FROM Категорія")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_category['values'] = [el[0] for el in cat_names_upd]

    enter_category.bind("<Button-1>", load_data_cat)

    def load_data_th(event):
        cat_names_upd = execute_sql_query_get(conn_str, f"SELECT Назва_зони_зберігання FROM Зона_зберігання"
                                                        f" WHERE Код_складу = {self.current_sclad_id}")
        # Обновление значений Combobox, а не создание нового экземпляра
        enter_th['values'] = [el[0] for el in cat_names_upd]

    enter_th.bind("<Button-1>", load_data_th)
    def check_cat_availability(event):

        if hasattr(enter_category, 'error_label_name'):
            enter_category.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_category.config(style="Custom.TCombobox")

        sql_cat = f"SELECT Код_категорії FROM Категорія WHERE Категорія = '{enter_category.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_cat)

        if not kod_th:
            error_label_name = Label(popup, text="Такої категорії  не існує на складі")
            error_label_name.place(x=150, y=225)
            error_label_name.config(foreground="red")
            enter_category.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_category.config(style="Custom.TCombobox")

    enter_category.bind("<KeyRelease>", check_cat_availability)
    enter_category.bind("<<ComboboxSelected>>", check_cat_availability)

    def check_thona_availability(event):

        if hasattr(enter_th, 'error_label_name'):
            enter_th.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_th.config(style="Custom.TCombobox")

        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        if not kod_th:
            error_label_name = Label(popup, text="Такої зони зберігання  не існує на складі")
            error_label_name.place(x=150, y=325)
            error_label_name.config(foreground="red")
            enter_th.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_th.config(style="Custom.TCombobox")

    enter_th.bind("<KeyRelease>", check_thona_availability)
    enter_th.bind("<<ComboboxSelected>>", check_thona_availability)

    def check_prod_availability(event):

        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()

        sql_paletu = f"SELECT Назва_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        prod_names = execute_sql_query_get(conn_str, sql_paletu)

        if prod_names:
            error_label_name = Label(popup, text="Така продукція вже існує")
            error_label_name.place(x=150, y=325)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета

            return

    enter_name.bind("<KeyRelease>", check_prod_availability)

    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add_data)
    btn_go.pack(pady=10)

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


def change_prod(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Редагування продукту")

    def on_close():
        # Здесь отключаем кнопку del_items
        self.btn_add_prod.config(state="normal")
        self.del_items.config(state="normal")
        self.change_items.config(state="normal")
        self.main_menu_but.config(state="normal")
        self.menu_button.config(state="normal")
        self.menu_button_dovidku.config(state="normal")
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    def generate_unique_article():
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            # Проверяем уникальность артикула в базе данных
            sql_check_article = f"SELECT COUNT(*) FROM Продукція WHERE Артикул = '{random_string}'"
            result = execute_sql_query_get(conn_str, sql_check_article)
            if result[0][0] == 0:  # Если артикул уникален
                return random_string

    def add_data():
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_category.config(style="Custom.TCombobox")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        enter_th.config(style="Custom.TCombobox")

        enter_name.config(highlightbackground="lightgray")
        enter_price.config(highlightbackground="lightgray")
        enter_count.config(highlightbackground="lightgray")

        if hasattr(popup, 'error_lable'):
            popup.error_lable.destroy()

        random_string = generate_unique_article()
        print(random_string)

        all_labels = [enter_name.get(), enter_count.get(), enter_price.get(), enter_category.get(), enter_th.get()]

        empty_fields = []
        for i, label in enumerate(all_labels):
            if not label:
                empty_fields.append(i)

        error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля")
        popup.error_lable = error_lable
        if error_lable.winfo_ismapped():
            error_lable.destroy()

        if empty_fields:
            for field_index in empty_fields:
                if field_index == 0:
                    enter_name.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 1:
                    enter_count.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 2:
                    enter_price.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_category.config(style="Custom.TCombobox")
                elif field_index == 4:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    enter_th.config(style="Custom.TCombobox")

            error_lable.place(x=190, y=328)
            error_lable.config(foreground="red")

            return
        else:
            if not check_validate():
                return

        # enter_count.config(highlightbackground=None, highlightthickness=0.5)

        sql_cat = f"SELECT Код_категорії FROM Категорія WHERE Категорія = '{enter_category.get()}' "
        kod_cat = execute_sql_query_get(conn_str, sql_cat)

        # Получаем код зоны зберігання из базы данных
        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        if not kod_cat or not kod_th:
            wrong_data(popup)
            if not kod_cat:
                combostyle.configure("Custom.TCombobox", bordercolor="red")
                enter_category.config(style="Custom.TCombobox")
            if not kod_th:
                combostyle.configure("Custom.TCombobox", bordercolor="red")
                enter_th.config(style="Custom.TCombobox")
            return
        sql_paletu = f"SELECT Місткість_палетів_ FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        paletu = execute_sql_query_get(conn_str, sql_paletu)

        sql_current_prod_c = f"SELECT Кількість_палетів_ FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        added_count =execute_sql_query_get(conn_str, sql_current_prod_c)

        total_count = count_pallets(enter_th)
        if added_count:
            if (total_count+int(enter_count.get())-added_count[0][0])<= paletu[0][0]:
                sql_update_prod = f"""
                        UPDATE Продукція
                        SET Назва_продукції = '{enter_name.get()}',
                            Кількість_палетів_ = '{enter_count.get()}',
                            Код_категорії = '{kod_cat[0][0]}',
                            Ціна_за_од = '{enter_price.get()}',
                            Код_зони_зберігання = '{kod_th[0][0]}',
                            Код_складу = '{self.current_sclad_id}'
                        WHERE Код_продукції = '{self.item_text[0]}'
                    """
                execute_sql_query_insert(conn_str, sql_update_prod)
                self.main_menu_but.config(state="normal")
                self.menu_button.config(state="normal")
                self.menu_button_dovidku.config(state="normal")
                self.open_zapas_menu()
            else:
                enter_count.config(highlightbackground="red", highlightthickness=0.5)
                error_lable = Label(popup, text="ПОМИЛКА: Кіл-ть палетів більше ніж має зона зберігання")
                error_lable.place(x=90, y=328)
                error_lable.config(foreground="red")
        else:
            sql_update_prod2 = f"""
                                    UPDATE Продукція
                                    SET Назва_продукції = '{enter_name.get()}',
                                        Кількість_палетів_ = '{enter_count.get()}',
                                        Код_категорії = '{kod_cat[0][0]}',
                                        Ціна_за_од = '{enter_price.get()}',
                                        Код_зони_зберігання = '{kod_th[0][0]}',
                                        Код_складу = '{self.current_sclad_id}'
                                    WHERE Код_продукції = '{self.item_text[0]}'
                                """
            execute_sql_query_insert(conn_str, sql_update_prod2)
            self.open_zapas_menu()


    def back_form():
        popup.destroy()
        root.deiconify()
    def check_validate():
        error_value_list = []
        if hasattr(popup, 'error_label'):
            popup.error_label.destroy()
        # Удаляем предыдущие метки ошибок и сбрасываем цвета фона
        if hasattr(enter_count, 'error_label'):
            enter_count.error_label.destroy()
            enter_count.config(highlightbackground="lightgray", highlightcolor="black")

        if hasattr(enter_price, 'error_label'):
            enter_price.error_label.destroy()
            enter_price.config(highlightbackground="lightgray", highlightcolor="black")

        # Проверяем типы данных введенных значений
        count_value = enter_count.get().strip()  # Удаляем пробелы в начале и конце строки
        price_value = enter_price.get().strip()

        error_label = Label(popup, text="Невірний формат введення")

        if not count_value.isdigit():
            error_value_list.append(count_value)
            enter_count.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            enter_count.error_label = error_label

        if not price_value.isdigit():
            error_value_list.append(price_value)
            enter_price.config(highlightbackground="red", highlightthickness=0.5)
            error_label.place(x=180, y=205)
            error_label.config(foreground="red")
            enter_price.error_label = error_label

        popup.error_label = error_label
        if error_value_list != []:
            return False
        else:
            return True
    ttk.Label(popup, text="Редагування продукту", font=("Arial", 20, "bold")).pack()

    name_prod = ttk.Label(popup, text="Назва продукту:", font=("Arial", 14))
    name_prod.pack(anchor="nw", padx=10, pady=30)

    # Устанавливаем текст по умолчанию в Entry
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.insert(0, f"{self.item_text[1]}")
    enter_name.place(x=175, y=65)

    count_prod = ttk.Label(popup, text="Кількість(палетів):", font=("Arial", 14))
    count_prod.pack(anchor="nw",padx=10,pady=1)
    enter_count = Entry(popup, width=20,font=("Arial",12))
    enter_count.insert(0, f"{self.item_text[2]}")
    enter_count.place(x=175, y=123)

    cat_names = execute_sql_query_get(conn_str,"SELECT Код_категорії, Категорія FROM Категорія")
    categ_prod = ttk.Label(popup, text="Категорія:", font=("Arial", 14))
    categ_prod.pack(anchor="nw", padx=10, pady=30)
    combostyle = ttk.Style()
    combostyle.configure("TCombobox",font=("Arial", 16))
    enter_category = ttk.Combobox(popup,width=28,values=[el[1] for el in cat_names],style="TCombobox")
    enter_category.insert(0, f"{self.item_text[7]}")
    enter_category.place(x=175, y=180)
    print("Selected value:", enter_category.get())
    im = self.back
    add_cat_btn = Button(popup,image=self.add_prod_im,command=lambda :add_category(popup,self),width=30,height=30)
    add_cat_btn.place(x=390, y=180)
    add_cat_btn.config(background="White", highlightbackground="White", activebackground="white")

    price_prod = ttk.Label(popup, text="Ціна (за од.):", font=("Arial", 14))
    price_prod.pack(anchor="nw", padx=10, pady=3)
    enter_price = Entry(popup, width=20,font=("Arial",12))
    enter_price.insert(0, f"{self.item_text[3]}")
    enter_price.place(x=175, y=237)

    saving_prod = ttk.Label(popup, text="Зона зберігання:", font=("Arial", 14))
    saving_prod.pack(anchor="nw", padx=10, pady=25)
    save_th = execute_sql_query_get(conn_str,f"SELECT Код_зони_зберігання, Назва_зони_зберігання FROM Зона_зберігання"
                                             f" WHERE Код_складу = {self.current_sclad_id}")
    th_el = {el for el in save_th}
    print(th_el)
    enter_th = ttk.Combobox(popup, width=28,values=[el[1] for el in save_th])
    enter_th.insert(0, f"{self.item_text[4]}")
    enter_th.place(x=175, y=294)
    add_th = Button(popup,image=self.add_prod_im,command=lambda : add_save_th(popup,self),width=30,height=30)

    add_th.place(x=390,y=294)
    add_th.config(background="White", highlightbackground="White", activebackground="white")

    button_back = Button(popup, image=im, width=30, height=30, background='white', bd=0, activebackground='red',
                         highlightthickness=0, highlightbackground='white', command=back_form)

    button_back.place(x=20, y=23)
    button_back.config(background="White", highlightbackground="White", activebackground="white")

    def check_cat_availability(event):

        if hasattr(enter_category, 'error_label_name'):
            enter_category.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_category.config(style="Custom.TCombobox")

        sql_cat = f"SELECT Код_категорії FROM Категорія WHERE Категорія = '{enter_category.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_cat)

        if not kod_th:
            error_label_name = Label(popup, text="Такої категорії  не існує на складі")
            error_label_name.place(x=150, y=225)
            error_label_name.config(foreground="red")
            enter_category.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_category.config(style="Custom.TCombobox")

    enter_category.bind("<KeyRelease>", check_cat_availability)
    enter_category.bind("<<ComboboxSelected>>", check_cat_availability)

    def check_thona_availability(event):

        if hasattr(enter_th, 'error_label_name'):
            enter_th.error_label_name.destroy()
            combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
            enter_th.config(style="Custom.TCombobox")

        sql_th = f"SELECT Код_зони_зберігання FROM Зона_зберігання WHERE Назва_зони_зберігання = '{enter_th.get()}' "
        kod_th = execute_sql_query_get(conn_str, sql_th)

        if not kod_th:
            error_label_name = Label(popup, text="Такої зони зберігання  не існує на складі")
            error_label_name.place(x=150, y=325)
            error_label_name.config(foreground="red")
            enter_th.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета
            combostyle.configure("Custom.TCombobox", bordercolor="red")
            enter_th.config(style="Custom.TCombobox")

    enter_th.bind("<KeyRelease>", check_thona_availability)
    enter_th.bind("<<ComboboxSelected>>", check_thona_availability)

    def check_prod_availability(event):

        if hasattr(enter_name, 'error_label_name'):
            enter_name.error_label_name.destroy()

        sql_paletu = f"SELECT Назва_продукції FROM Продукція WHERE Назва_продукції = '{enter_name.get()}' "
        prod_names = execute_sql_query_get(conn_str, sql_paletu)

        if prod_names:
            error_label_name = Label(popup, text="Така продукція вже існує")
            error_label_name.place(x=150, y=325)
            error_label_name.config(foreground="red")
            enter_name.error_label_name = error_label_name  # Сохраняем ссылку на виджет в объекте виджета

            return

    enter_name.bind("<KeyRelease>", check_prod_availability)


    btn_go = Button(popup, text="Редагувати",font=("Arial",14),width=10, command=add_data)
    btn_go.pack(pady=10)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 400
    # Вычисляем координаты для центрирования
    x_coordinate = popup.winfo_x()+850 + (root_width - popup_width) // 2
    y_coordinate = popup.winfo_y() + 400 + (root_height - popup_height) // 2

    # Размещаем всплывающее окно по центру
    popup.geometry(f"{popup_width}x{popup_height}+{x_coordinate}+{y_coordinate}")
    popup.resizable(False, False)

