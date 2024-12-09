import tkinter as tk
from fpdf import FPDF
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from popups import ToolTip
from processes_menues.do_ttn import add_ttn, change_ttn
from short_inf_popups import delete_error


def menu_ttn(self):
    self.frame_menu.pack_forget()
    for widget in self.ttn_frame.winfo_children():
        widget.destroy()
    self.ttn_frame.pack(fill='both', expand=True)
    self.ttn_name = tk.Label(self.ttn_frame, bg="White", bd=0, text="Товаро-транспорта накладна", font=("Arial", 25))
    self.ttn_name.pack(pady=20)

    get_current_sclad_query = f"SELECT Код_складу FROM Склад WHERE Назва_складу = '{self.chosen_name}'"
    print(self.chosen_name)
    current_sclad = execute_sql_query_get(conn_str, get_current_sclad_query)

    if current_sclad:
        self.current_sclad_id = current_sclad[0][0]
        print("Current Sclad ID:", self.current_sclad_id)
        self.sep_name = ttk.Separator(self.ttn_frame, bootstyle="dark")
        self.sep_name.place(x=25 ,y=60 ,anchor="nw", width=120)
        # Додаємо мітку з назвою складу
        self.name_scl = tk.Label(self.ttn_frame, bg="White", bd=0, text=self.chosen_name, font=("Arial", 25))
        self.name_scl.place(x=80, y=40 ,anchor="center")
    else:
        print("Склад з такою назвою не знайдено.")

    def populate_tree(tree, data):
        for row in data:
            tree.insert("", "end", values=row)

    def delete_all_data():
        try:
            execute_sql_query_insert(conn_str, "DELETE FROM ТТН")
            self.open_ttn_menu()
        except:
            delete_error(self.ttn_frame)

    def print_to_pdf():
        # Создаем новый PDF-документ
        pdf = FPDF()
        pdf.add_page()

        # Определяем путь к файлу шрифта
        font_path = r"C:\Users\Данил\PycharmProjects\ProjectX_Buliy\_fonts\DejaVuSansMono.ttf"

        # Добавляем шрифт с указанием кодировки (utf-8)
        pdf.add_font("DejaVuSansMono", fname=font_path, style="", uni=True)

        pdf.set_font("DejaVuSansMono", size=10)

        # Определяем ширину страницы и текст для заголовка
        page_width = pdf.w
        title_text = "Товаро-транспортна накладна"

        # Определяем ширину текста заголовка
        title_width = pdf.get_string_width(title_text)

        # Вычисляем позицию для выравнивания по центру
        x_position = (page_width - title_width) / 2

        # Устанавливаем позицию X для центрирования заголовка
        pdf.set_x(x_position+20)

        # Печатаем заголовок

        pdf.set_font("DejaVuSansMono",  size=16)  # Устанавливаем жирный шрифт с размером 12
        pdf.cell(10, 10, title_text, 0, 1, 'C')  # Выводим заголовок
        pdf.set_font("DejaVuSansMono", size=8)

        x_shift = 5
        pdf.set_x(x_shift)

        # Заголовки столбцов
        columns = ("№", "Номер","Склад","Замовник","Продукція","Кіл-ть","Ціна/од","Сума","Водій","Транспорт","Дата")

        # Печать заголовков
        x_shift = 5
        pdf.set_x(x_shift)
        pdf.cell(10, 10, columns[0], border=1, ln=False)  # Изменено с 22 на 30 для увеличения ширины первого столбца
        for col, text in enumerate(columns[1:]):
            pdf.cell(19, 10, text, border=1, ln=False)

        pdf.ln()

        for row_id in tree.get_children():
            x_shift = 5
            pdf.set_x(x_shift)
            values = tree.item(row_id, "values")
            pdf.cell(10, 10, values[0], border=1, ln=False)
            for value in values[1:]:
                pdf.cell(19, 10, str(value), border=1, ln=False)

            pdf.ln()

        # Сохраняем PDF-файл с использованием UTF-8 кодировки
        pdf.output("ttn.pdf")

    print_doc = Button(self.ttn_frame, image=self.printer, command=print_to_pdf)
    print_doc.place(x=87, y=63)
    print_doc.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(print_doc, text="Друк")

    def print_to_pdf2():
        # Создаем новый PDF-документ
        pdf = FPDF()
        pdf.add_page()

        # Определяем путь к файлу шрифта
        font_path = r"C:\Users\Данил\PycharmProjects\ProjectX_Buliy\_fonts\DejaVuSansMono.ttf"

        # Добавляем шрифт с указанием кодировки (utf-8)
        pdf.add_font("DejaVuSansMono", fname=font_path, style="", uni=True)

        pdf.set_font("DejaVuSansMono", size=10)

        # Определяем ширину страницы и текст для заголовка
        page_width = pdf.w
        title_text = "Товаро-транспортна накладна"

        # Определяем ширину текста заголовка
        title_width = pdf.get_string_width(title_text)

        # Вычисляем позицию для выравнивания по центру
        x_position = (page_width - title_width) / 2

        # Устанавливаем позицию X для центрирования заголовка
        pdf.set_x(x_position + 20)

        # Печатаем заголовок
        pdf.set_font("DejaVuSansMono", size=16)  # Устанавливаем жирный шрифт с размером 12
        pdf.cell(10, 10, title_text, 0, 1, 'C')  # Выводим заголовок
        pdf.set_font("DejaVuSansMono", size=8)

        pdf.set_x(x_position + 17)
        pdf.set_font("DejaVuSansMono", size=16)  # Устанавливаем жирный шрифт с размером 12
        # Додаємо лінію
        pdf.set_draw_color(0, 0, 0)  # Встановлюємо колір лінії на чорний

        pdf.set_x(x_position + 75)
        pdf.cell(10, 10, f"Дата: {self.item_text[10]}", 0, 1, 'C')  # Выводим заголовок
        pdf.line(x_position + 70, pdf.get_y() - 1, x_position + 60 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_x(x_position + 19)
        pdf.cell(10, 10, f"Номер ТТН {self.item_text[1]}", 0, 1, 'C')  # Выводим заголовок
        pdf.line(x_position + 37, pdf.get_y() - 1, x_position + 15 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_font("DejaVuSansMono", size=12)

        pdf.set_x(12)
        client_text = f"Замовник:".ljust(10)
        pdf.cell(10, 10, client_text, 0, 0, 'C')  # Выводим заголовок
        pdf.set_x(50)
        pdf.cell(10, 10, f"{self.item_text[3]}", 0, 1, 'C')  # Выводим заголовок
        pdf.line(28, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_x(33)
        pdf.cell(10, 10, "Відправник: ПрАТ 'Оболонь'", 0, 1, 'C')  # Выводим заголовок
        pdf.line(34, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        adress = execute_sql_query_get(conn_str, f"""
           SELECT "Адреса"
            FROM "Замовник"
            WHERE "ПІБ_контактної_особи" = '{self.item_text[3]}';
                    """)

        pdf.set_x(13)
        adress_text = f"Адреса:".ljust(10)
        pdf.cell(10, 10, adress_text, 0, 0, 'C')  # Выводим заголовок
        pdf.set_x(50)
        pdf.cell(10, 10, f" {adress[0][0]}", 0, 1, 'C')
        pdf.line(25, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_x(14)
        car_text = f"Автомобіль:".ljust(10)
        pdf.cell(10, 10, car_text, 0, 0, 'C')  # Выводим заголовок
        pdf.set_x(50)
        pdf.cell(10, 10, f" {self.item_text[9]}", 0, 1, 'C')  # Выводим значение из self.item_text[8] с переходом на новую строку
        pdf.line(35, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_x(13)
        driver_text = f"Водій:".ljust(10)  # Устанавливаем ширину 10 символов для текста "Водій:"
        pdf.cell(10, 10, driver_text, 0, 0, 'C')  # Выводим текст "Водій:" без перехода на новую строку
        pdf.set_x(50)
        pdf.cell(10, 10, f" {self.item_text[8]}", 0, 1,'C')  # Выводим значение из self.item_text[8] с переходом на новую строку

        pdf.line(20, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.set_x(x_position+20)
        pdf.cell(10, 10, "Відомості про товар", 0, 1, 'C')  # Выводим заголовок

        x_position = 20  # Начальная позиция X
        x_shift = 25  # Смещение от начальной позиции X

        # Позиция для заголовков столбцов
        x_header = x_position + x_shift

        # Задаем начальную позицию X для вывода заголовков столбцов
        pdf.set_x(x_header)

        # Заголовки столбцов
        columns = (
            "№", "Продукція", "Кіл-ть", "Ціна/од", "Сума")

        # Печать заголовков
        pdf.cell(10, 10, columns[0], border=1, ln=False)
        pdf.cell(25, 10, columns[1], border=1, ln=False)
        pdf.cell(20, 10, columns[2], border=1, ln=False)
        pdf.cell(20, 10, columns[3], border=1, ln=False)
        pdf.cell(20, 10, columns[4], border=1, ln=True)

        pdf.set_x(x_header)
        pdf.cell(10, 10, str(self.item_text[0]), border=1, ln=False)
        pdf.cell(25, 10, str(self.item_text[4]), border=1, ln=False)
        pdf.cell(20, 10, str(self.item_text[5]), border=1, ln=False)
        pdf.cell(20, 10, str(self.item_text[6]), border=1, ln=False)
        pdf.cell(20, 10, str(self.item_text[7]), border=1, ln=False)

        numb_of_ph = execute_sql_query_get(conn_str, f"""
                           SELECT "Телефон_водія"
                            FROM "Водій"
                            WHERE "ПІБ_водія" = '{self.item_text[8]}';
                                    """)

        pdf.set_y(130)
        pdf.set_x(15)
        numb_of_car_text = f"Номер водія:".ljust(10)  # Устанавливаем ширину 10 символов для текста "Водій:"
        pdf.cell(10, 10, numb_of_car_text, 0, 0, 'C')  # Выводим текст "Водій:" без перехода на новую строку
        pdf.set_x(50)
        pdf.cell(10, 10, f" {numb_of_ph[0][0]}", 0, 1,
                 'C')  # Выводим значение из self.item_text[8] с переходом на новую строку

        pdf.line(37, pdf.get_y() - 1, 35 + title_width, pdf.get_y() - 1)  # Малюємо лінію

        pdf.output("ttn2.pdf")

    start_1 = Button(self.ttn_frame,image=self.delete_all,command=delete_all_data)
    start_1.place(x=25,y=63)
    start_1.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(start_1,text="Очистити таблицю")

    columns = ("№", "Номер","Склад", "Замовник", "Продукція", "Кількість" , "Ціна/од", "Сума","Водій","Транспорт","Дата")
    tree = ttk.Treeview(self.ttn_frame, columns=columns, show="headings")

    def open_add_ttn():
        self.add_prod_window = self.ttn_frame
        # add_prod(self.add_prod_window, self)
        add_ttn(self.add_prod_window, self)
        self.btn_add_prod.config(state="disabled")

    def delete_ttn():
        sql_del = f"DELETE FROM ТТН WHERE Код_ТТН = {self.item_text[0]}"
        execute_sql_query_insert(conn_str, sql_del)
        self.open_ttn_menu()

    def add_change_ttn():
        self.add_change_window = self.ttn_frame
        change_ttn(self.add_change_window, self)
        self.change_items.config(state="disabled")

    self.del_items = Button(self.ttn_frame, image=self.del_prodmain ,command=delete_ttn)
    self.del_items.config(background="White", highlightbackground="White", activebackground="white")

    self.change_items = Button(self.ttn_frame, image=self.change_prodmain ,command=add_change_ttn)
    self.change_items.config(background="White", highlightbackground="White", activebackground="white")

    self.print_with_items = Button(self.ttn_frame, image=self.printer2, command=print_to_pdf2)
    self.print_with_items.config(background="White", highlightbackground="White", activebackground="white")


    def on_treeview_select(event):
        # Определяем, был ли клик внутри строки таблицы или вне ее
        item = tree.identify_row(event.y)
        if item:
            # Если клик был на строке таблицы, обрабатываем выделение элемента
            selected_items = tree.selection()
            if selected_items:
                row_index = tree.index(selected_items)
                # Получаем значения выбранного элемента
                self.item_text = tree.item(selected_items[0])['values']
                print("Выбрано:", self.item_text)
                # Если выбран хотя бы один элемент, включаем кнопки
                self.del_items.place(x=850, y=55)
                self.change_items.place(x=790, y=63)
                self.print_with_items.place(x=723,y=63)
                ToolTip(self.change_items ,"Редагування")
                ToolTip(self.del_items, "Видалення")
                ToolTip(self.print_with_items, "Друк")
        else:
            # Если клик был вне строк таблицы, снимаем выделение со всех элементов и отключаем кнопки
            tree.selection_remove(tree.selection())
            self.del_items.place_forget()
            self.change_items.place_forget()
            self.print_with_items.place_forget()

    tree.bind("<ButtonRelease-1>", on_treeview_select)

    def on_form(event):
        if not entry_find.get():
            entry_find.insert(0, "Номер ТТН")  # Вставка текста обратно, если Entry пустой
            entry_find.config(fg="gray")  # Изменение цвета текста обратно на серый
        self.del_items.place_forget()
        self.change_items.place_forget()
        selected_items = tree.selection()
        if selected_items:
            tree.selection_remove(tree.selection())
    self.ttn_frame.bind("<ButtonRelease-1>", on_form)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=50 ,anchor="center")

    #"№", "Склад", "Номер", "Замовник", "Продукція", "Кількість", "Ціна/од", "Сума", "Водій", "Транспорт", "Дата"
    sql_get_prod2 = f"""
        SELECT ord."Код_ТТН",
               ord."Номер_ТТН",
               s."Назва_складу" AS "Склад",
               cst."ПІБ_контактної_особи",
               p."Назва_продукції",
               ord."Кількість_палетів_",
               ord."Ціна_за_од",
               ord."Сума",
               d."ПІБ_водія",
               ts."Назва_транспорту",
               ord."Дата"
        FROM public."ТТН" AS ord
        INNER JOIN "Склад" AS s ON ord."Код_складу" = s."Код_складу"
        INNER JOIN "Замовник" AS cst ON ord."Код_замовника" = cst."Код_замовника"
        INNER JOIN "Продукція" AS p ON ord."Код_продукції" = p."Код_продукції"
        INNER JOIN "Водій" AS d ON ord."Код_водія" = d."Код_водія"
        INNER JOIN "Автотранспорт" AS ts ON ord."Код_транспорту" = ts."Код_транспорту"
        WHERE p."Код_складу" = {self.current_sclad_id};
    """
    data = None
    while data is None:
        data = execute_sql_query_get(conn_str ,sql_get_prod2)

    populate_tree(tree, data)

    for row in data:
        print(row)

    tree.pack(fill="both" ,padx=2, pady=40 ,expand=True)

    def find():
        search_term = entry_find.get().lower()  # Get the search term from the entry widget
        # Clear existing data in the treeview
        tree.delete(*tree.get_children())
        # Execute SQL query to retrieve filtered data based on the search term
        sql_find = f"""
               SELECT ord."Код_ТТН",
                   ord."Номер_ТТН",
                   s."Назва_складу" AS "Склад",
                   cst."ПІБ_контактної_особи",
                   p."Назва_продукції",
                   ord."Кількість_палетів_",
                   ord."Ціна_за_од",
                   ord."Сума",
                   d."ПІБ_водія",
                   ts."Назва_транспорту",
                   ord."Дата"
            FROM public."ТТН" AS ord
            INNER JOIN "Склад" AS s ON ord."Код_складу" = s."Код_складу"
            INNER JOIN "Замовник" AS cst ON ord."Код_замовника" = cst."Код_замовника"
            INNER JOIN "Продукція" AS p ON ord."Код_продукції" = p."Код_продукції"
            INNER JOIN "Водій" AS d ON ord."Код_водія" = d."Код_водія"
            INNER JOIN "Автотранспорт" AS ts ON ord."Код_транспорту" = ts."Код_транспорту"
            WHERE "Код_складу" = {self.current_sclad_id} AND Номер_ТТН = {search_term};
            """
        filtered_data = execute_sql_query_get(conn_str, sql_find)
        if filtered_data is not None and filtered_data:  # Проверяем, есть ли отфильтрованные данные
            populate_tree(tree, filtered_data)  # Заполняем дерево данными
        else:
            # Если отфильтрованных данных нет, можно просто обновить дерево без записей
            populate_tree(tree, '')


    def on_entry_click(event):
        if entry_find.get() == "Номер ТТН":
            entry_find.delete(0, "end")  # Удаление текста при фокусировке
            entry_find.config(fg="black")


    entry_find = Entry(self.ttn_frame, width=13, font=("Arial", 12))
    entry_find.insert(0, "Номер ТТН")  # Установка значения по умолчанию
    entry_find.config(fg="gray")  # Установка цвета текста по умолчанию
    entry_find.bind("<Button-1>", on_entry_click)

    entry_find.place(x=440, y=70)


    btn_find = Button(self.ttn_frame, image=self.find, command=find)
    btn_find.place(x=565, y=69)
    btn_find.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(btn_find, "Пошук ТТН")

    def sort_treeview_column(tree, col, reverse=False):
        # Проверяем, является ли столбец "Ціна" или "Кількість палетів"
        if col in ["Кількість" ,"Номер" ,"Сума" ,"№"]:
            # Получаем данные из всех строк в столбце
            data = [(float(tree.set(child, col)), child) for child in tree.get_children('')]
            # Сортируем данные
            data.sort(reverse=reverse)

            # Перемещаем строки в дереве
            for index, (val, child) in enumerate(data):
                tree.move(child, '', index)

            # Устанавливаем команду сортировки для заголовка столбца
            tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))
        else:
            # Получаем данные из всех строк в столбце
            data = [(tree.set(child, col).lower(), child) for child in tree.get_children('')]
            # Сортируем данные
            data.sort(reverse=reverse)
            # Перемещаем строки в дереве
            for index, (val, child) in enumerate(data):
                tree.move(child, '', index)
            # Устанавливаем команду сортировки для заголовка столбца
            tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))

    # Призначення обробника подій кліку на заголовок стовпця
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview_column(tree, c))

    self.btn_add_prod = Button(self.ttn_frame, image=self.add_prodmain, command=open_add_ttn)
    self.btn_add_prod.place(x=930, y=60)
    self.btn_add_prod.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(self.btn_add_prod ,"Додавання ТТН")

    # btn_sort = Button(self.zapas_menu,text="SORT")
    # btn_sort.place(x=500,y=80)


    # Призначення обробника подій кліку на заголовок стовпця
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview_column(tree, c))

        def print_doc():
            ...