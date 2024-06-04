
from fpdf import FPDF
from processes_menues.do_order_come import add_order_come, change_order_come
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from popups import ToolTip
from short_inf_popups import delete_error


def menu_order(self):
    self.frame_menu.pack_forget()
    for widget in self.oreder_come_menu.winfo_children():
        widget.destroy()
    self.oreder_come_menu.pack(fill='both', expand=True)
    self.oreder_name = tk.Label(self.oreder_come_menu, bg="White", bd=0, text="Надходження товару", font=("Arial", 25))
    self.oreder_name.pack(pady=20)

    get_current_sclad_query = f"SELECT Код_складу FROM Склад WHERE Назва_складу = '{self.chosen_name}'"
    print(self.chosen_name)
    current_sclad = execute_sql_query_get(conn_str, get_current_sclad_query)

    if current_sclad:
        self.current_sclad_id = current_sclad[0][0]
        print("Current Sclad ID:", self.current_sclad_id)
        self.sep_name = ttk.Separator(self.oreder_come_menu)
        self.sep_name.place(x=25 ,y=60 ,anchor="nw", width=120)
        # Додаємо мітку з назвою складу
        self.name_scl = tk.Label(self.oreder_come_menu, bg="White", bd=0, text=self.chosen_name, font=("Arial", 25))
        self.name_scl.place(x=80, y=40 ,anchor="center")
    else:
        print("Склад з такою назвою не знайдено.")

    def populate_tree(tree, data):
        for row in data:
            tree.insert("", "end", values=row)

    def delete_all_data():
        try:
            execute_sql_query_insert(conn_str, "DELETE FROM Ордер_надходження")
            self.open_order_incm_menu()
        except Exception:
            delete_error(self.oreder_come_menu)

    start_1 = Button(self.oreder_come_menu,image=self.delete_all,command=delete_all_data)
    start_1.place(x=25,y=63)
    start_1.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(start_1,text="Очистити таблицю")

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
        title_text = "Надходження"

        # Определяем ширину текста заголовка
        title_width = pdf.get_string_width(title_text)

        # Вычисляем позицию для выравнивания по центру
        x_position = (page_width - title_width) / 2

        # Устанавливаем позицию X для центрирования заголовка
        pdf.set_x(x_position)

        # Печатаем заголовок
        pdf.set_font("DejaVuSansMono",  size=16)  # Устанавливаем жирный шрифт с размером 12
        pdf.cell(10, 10, title_text, 0, 1, 'C')  # Выводим заголовок
        pdf.set_font("DejaVuSansMono", size=8)

        x_shift = 7
        pdf.set_x(x_shift)

        # Заголовки столбцов
        columns = ("№", "Номер","Продукція","Кіл-ть","Склад","Зона збер.","Цех","Номер партії","Дата","Сума")

        # Печать заголовков
        pdf.cell(10, 10, columns[0], border=1, ln=False)  # Изменено с 22 на 30 для увеличения ширины первого столбца
        for col, text in enumerate(columns[1:9]):
            pdf.cell(22, 10, text, border=1, ln=False)
        pdf.cell(10, 10, columns[9], border=1, ln=False)

        pdf.ln()

        for row_id in tree.get_children():
            x_shift = 7
            pdf.set_x(x_shift)
            values = tree.item(row_id, "values")
            pdf.cell(10, 10, str(values[0]), border=1, ln=False)
            for value in values[1:9]:
                pdf.cell(22, 10, str(value), border=1, ln=False)
            pdf.cell(10, 10, str(values[9]), border=1, ln=False)
            pdf.ln()

        # Сохраняем PDF-файл с использованием UTF-8 кодировки
        pdf.output("order_come.pdf")

    print_doc = Button(self.oreder_come_menu, image=self.printer, command=print_to_pdf)
    print_doc.place(x=87, y=63)
    print_doc.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(print_doc, text="Друк")

    columns = ("№", "Номер ордеру", "Продукт", "Кількість" ,"Склад",
               "Зона зберігання" ,"Цех", "Номер партії", "Дата", "Сума")
    tree = ttk.Treeview(self.oreder_come_menu, columns=columns, show="headings")

    def open_add_prod():
        self.add_prod_window = self.oreder_come_menu
        # add_prod(self.add_prod_window, self)
        add_order_come(self.add_prod_window, self)
        self.btn_add_prod.config(state="disabled")

    def delete_order():
        sql_del = f"DELETE FROM Ордер_надходження WHERE Код_ордеру_надходження = {self.item_text[0]}"
        execute_sql_query_insert(conn_str, sql_del)
        self.open_order_incm_menu()

    def add_change_prod():
        self.add_change_window = self.oreder_come_menu
        change_order_come(self.add_change_window, self)
        self.change_items.config(state="disabled")

    self.del_items = Button(self.oreder_come_menu, image=self.del_prodmain ,command=delete_order)
    self.del_items.config(background="White", highlightbackground="White", activebackground="white")

    self.change_items = Button(self.oreder_come_menu, image=self.change_prodmain ,command=add_change_prod)
    self.change_items.config(background="White", highlightbackground="White", activebackground="white")


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
                ToolTip(self.change_items ,"Редагування")
                ToolTip(self.del_items, "Видалення")
        else:
            # Если клик был вне строк таблицы, снимаем выделение со всех элементов и отключаем кнопки
            tree.selection_remove(tree.selection())
            self.del_items.place_forget()
            self.change_items.place_forget()

    tree.bind("<ButtonRelease-1>", on_treeview_select)

    def on_form(event):
        if not entry_find.get():
            entry_find.insert(0, "Номер ордеру")  # Вставка текста обратно, если Entry пустой
            entry_find.config(fg="gray")  # Изменение цвета текста обратно на серый
        self.del_items.place_forget()
        self.change_items.place_forget()
        selected_items = tree.selection()
        if selected_items:
            tree.selection_remove(tree.selection())
    self.oreder_come_menu.bind("<ButtonRelease-1>", on_form)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=50 ,anchor="center")

    sql_get_prod2 = f"""
    SELECT ord."Код_ордеру_надходження",
    ord."Номер_ордеру_надходження",
    p."Назва_продукції",
    ord."Кількість_палетів_",
    s."Назва_складу" AS "Склад",
    z."Назва_зони_зберігання" AS "Зона зберігання",
    ord."Цех",
    ord."Номер_партії",
    ord."Дата",
    ord."Сума"
    FROM public."Ордер_надходження" AS ord
    INNER JOIN "Склад" AS s ON ord."Код_складу" = s."Код_складу"
    INNER JOIN "Зона_зберігання" AS z ON ord."Код_зони_зберігання" = z."Код_зони_зберігання"
    INNER JOIN "Продукція" AS p ON ord."Код_продукції" = p."Код_продукції"
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
            SELECT ord."Код_ордеру_надходження",
            ord."Номер_ордеру_надходження",
            p."Назва_продукції",
            ord."Кількість_палетів_",
            s."Назва_складу" AS "Склад",
            z."Назва_зони_зберігання" AS "Зона зберігання",
            ord."Цех",
            ord."Номер_партії",
            ord."Дата",
            ord."Сума"
            FROM public."Ордер_надходження" AS ord
            INNER JOIN "Склад" AS s ON ord."Код_складу" = s."Код_складу"
            INNER JOIN "Зона_зберігання" AS z ON ord."Код_зони_зберігання" = z."Код_зони_зберігання"
            INNER JOIN "Продукція" AS p ON ord."Код_продукції" = p."Код_продукції"
            WHERE "Код_складу" = {self.current_sclad_id} AND Номер_ордеру_надходження = {search_term};
            """
        filtered_data = execute_sql_query_get(conn_str, sql_find)
        if filtered_data is not None and filtered_data:  # Проверяем, есть ли отфильтрованные данные
            populate_tree(tree, filtered_data)  # Заполняем дерево данными
        else:
            # Если отфильтрованных данных нет, можно просто обновить дерево без записей
            populate_tree(tree, '')


    def on_entry_click(event):
        if entry_find.get() == "Номер ордеру":
            entry_find.delete(0, "end")  # Удаление текста при фокусировке
            entry_find.config(fg="black")


    entry_find = Entry(self.oreder_come_menu, width=13, font=("Arial", 12))
    entry_find.insert(0, "Номер ордеру")  # Установка значения по умолчанию
    entry_find.config(fg="gray")  # Установка цвета текста по умолчанию
    entry_find.bind("<Button-1>", on_entry_click)

    entry_find.place(x=440, y=70)


    btn_find = Button(self.oreder_come_menu, image=self.find, command=find)
    btn_find.place(x=565, y=69)
    btn_find.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(btn_find, "Пошук ордеру")

    def sort_treeview_column(tree, col, reverse=False):
        # Проверяем, является ли столбец "Ціна" или "Кількість палетів"
        if col in ["Кількість палетів" ,"Номер ордеру" ,"Цех" ,"№"]:
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

    self.btn_add_prod = Button(self.oreder_come_menu, image=self.add_prodmain, command=open_add_prod)
    self.btn_add_prod.place(x=930, y=60)
    self.btn_add_prod.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(self.btn_add_prod ,"Додавання надходження")

    # btn_sort = Button(self.zapas_menu,text="SORT")
    # btn_sort.place(x=500,y=80)


    # Призначення обробника подій кліку на заголовок стовпця
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview_column(tree, c))

        def print_doc():
            ...