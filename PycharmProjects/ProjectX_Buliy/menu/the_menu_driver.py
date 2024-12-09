
from fpdf import FPDF
from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *
from popups import ToolTip
from processes_menues.do_driver import add_driver, change_driver
from short_inf_popups import delete_error


def menu_driver(self):
    self.frame_menu.pack_forget()
    if self.oreder_come_menu.winfo_ismapped():
        self.oreder_come_menu.pack_forget()

    if self.zapas_menu.winfo_ismapped():
        self.zapas_menu.pack_forget()

    if self.thona_frame.winfo_ismapped():
        self.thona_frame.pack_forget()

    if self.categ_frame.winfo_ismapped():
        self.categ_frame.pack_forget()

    if self.avto_frame.winfo_ismapped():
        self.avto_frame.pack_forget()

    if self.spus_frame.winfo_ismapped():
        self.spus_frame.pack_forget()

    if self.customer_frame.winfo_ismapped():
        self.customer_frame.pack_forget()

    if self.ttn_frame.winfo_ismapped():
        self.ttn_frame.pack_forget()

    for widget in self.driver_frame.winfo_children():
        widget.destroy()
    self.driver_frame.pack(fill='both', expand=True)

    self.driver_name = tk.Label(self.driver_frame, bg="White", bd=0, text="Водії", font=("Arial", 25))
    self.driver_name.pack(pady=20)


    def populate_tree(tree, data):
        for row in data:
            tree.insert("", "end", values=row)

    def delete_all_data():
        try:
            execute_sql_query_insert(conn_str, "DELETE FROM Водій")
            self.open_driver_menu()
        except Exception:
            delete_error(self.driver_frame)

    start_1 = Button(self.driver_frame,image=self.delete_all,command=delete_all_data)
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
        title_text = "Водії"

        # Определяем ширину текста заголовка
        title_width = pdf.get_string_width(title_text)

        # Вычисляем позицию для выравнивания по центру
        x_position = (page_width - title_width) / 2

        # Устанавливаем позицию X для центрирования заголовка
        pdf.set_x(x_position)

        # Печатаем заголовок
        pdf.set_font("DejaVuSansMono",  size=16)  # Устанавливаем жирный шрифт с размером 12
        pdf.cell(10, 10, title_text, 0, 1, 'C')  # Выводим заголовок
        pdf.set_font("DejaVuSansMono", size=10)

        x_shift = 40
        pdf.set_x(x_shift)

        # Заголовки столбцов
        columns = ("№", "ПІБ","Телефон")

        # Печать заголовков
        for col, text in enumerate(columns):
            pdf.cell(40, 10, text, border=1, ln=False)

        pdf.ln()


        # Получаем данные из ttk.Treeview и печатаем их (предполагается что tree - это объект ttk.Treeview)
        for row_id in tree.get_children():
            x_shift = 40
            pdf.set_x(x_shift)
            values = tree.item(row_id, "values")
            for value in values:
                pdf.cell(40, 10, str(value), border=1, ln=False)
            pdf.ln()

        # Сохраняем PDF-файл с использованием UTF-8 кодировки
        pdf.output("drivers.pdf")


    # Пример использования:
    # Предполагается, что 'tree' - это объект ttk.Treeview, содержащий данные для печати в PDF

    print_doc = Button(self.driver_frame, image=self.printer, command=print_to_pdf)
    print_doc.place(x=87, y=63)
    print_doc.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(print_doc, text="Друк")


    columns = ("№", "ПІБ","Телефон")
    tree = ttk.Treeview(self.driver_frame, columns=columns, show="headings")

    def add_driver_():
        add_driver(self.new_window, self)
        self.btn_add_prod.config(state="disabled")

    def delete_th():
        sql_del = f"DELETE FROM Водій WHERE Код_водія = {self.item_text[0]}"
        execute_sql_query_insert(conn_str, sql_del)
        menu_driver(self)

    def add_change_driver():
        self.add_change_window = self.avto_frame
        change_driver(self.add_change_window, self)
        self.change_items.config(state="disabled")

    self.del_items = Button(self.driver_frame, image=self.del_prodmain, command=delete_th)
    self.del_items.config(background="White", highlightbackground="White", activebackground="white")

    self.change_items = Button(self.driver_frame, image=self.change_prodmain, command=add_change_driver)
    self.change_items.config(background="White", highlightbackground="White", activebackground="white")

    def on_treeview_select(event):
        # Определяем, был ли клик внутри строки таблицы или вне ее
        item = tree.identify_row(event.y)
        if item:
            # Если клик был на строке таблицы, обрабатываем выделение элемента
            selected_items = tree.selection()
            if selected_items:
                # Получаем значения выбранного элемента
                self.item_text = tree.item(selected_items[0])['values']
                print("Выбрано:", self.item_text)
                # Если выбран хотя бы один элемент, включаем кнопки
                self.del_items.place(x=850, y=55)
                self.change_items.place(x=790, y=63)
                ToolTip(self.change_items, "Редагування")
                ToolTip(self.del_items, "Видалення")
        else:
            # Если клик был вне строк таблицы, снимаем выделение со всех элементов и отключаем кнопки
            tree.selection_remove(tree.selection())
            self.del_items.place_forget()
            self.change_items.place_forget()

    tree.bind("<ButtonRelease-1>", on_treeview_select)

    def on_form(event):
        if not entry_find.get():
            entry_find.insert(0, "Прізвище")  # Вставка текста обратно, если Entry пустой
            entry_find.config(fg="gray")  # Изменение цвета текста обратно на серый
        self.del_items.place_forget()
        self.change_items.place_forget()
        selected_items = tree.selection()
        if selected_items:
            tree.selection_remove(tree.selection())

    self.driver_frame.bind("<ButtonRelease-1>", on_form)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    sql_get_prod2 = f"""
            SELECT "Код_водія",
            "ПІБ_водія","Телефон_водія" FROM "Водій";"""
    data = None
    while data is None:
        data = execute_sql_query_get(conn_str, sql_get_prod2)
    populate_tree(tree, data)

    for row in data:
        print(row)

    tree.pack(fill="both", padx=50, pady=50, expand=True)

    def find():
        search_term = entry_find.get().lower()  # Get the search term from the entry widget
        # Clear existing data in the treeview
        tree.delete(*tree.get_children())
        # Execute SQL query to retrieve filtered data based on the search term
        sql_find = f"""
             SELECT "Код_водія",
            "ПІБ_водія","Телефон_водія" FROM "Водій"
            WHERE LOWER("ПІБ_водія") LIKE '%{search_term}%';
            """
        filtered_data = execute_sql_query_get(conn_str, sql_find)
        if filtered_data is not None and filtered_data:  # Проверяем, есть ли отфильтрованные данные
            populate_tree(tree, filtered_data)  # Заполняем дерево данными
        else:
            # Если отфильтрованных данных нет, можно просто обновить дерево без записей
            populate_tree(tree, '')

    def on_entry_click(event):
        if entry_find.get() == "Назва":
            entry_find.delete(0, "end")  # Удаление текста при фокусировке
            entry_find.config(fg="black")

    entry_find = Entry(self.driver_frame, width=13, font=("Arial", 12))
    entry_find.insert(0, "Прізвище")  # Установка значения по умолчанию
    entry_find.config(fg="gray")  # Установка цвета текста по умолчанию
    entry_find.bind("<Button-1>", on_entry_click)

    entry_find.place(x=440, y=70)

    btn_find = Button(self.driver_frame, image=self.find, command=find)
    btn_find.place(x=565, y=69)
    btn_find.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(btn_find, "Пошук водія")

    # btn_sort = Button(self.zapas_menu,text="SORT")
    # btn_sort.place(x=500,y=80)

    def sort_treeview_column(tree, col, reverse=False):
        # Проверяем, является ли столбец "Ціна" или "Кількість палетів"
        if col == "№":
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

    self.btn_add_prod = Button(self.driver_frame, image=self.add_prodmain,
                               command=add_driver_)
    self.btn_add_prod.place(x=930, y=60)
    self.btn_add_prod.config(background="White", highlightbackground="White", activebackground="white")
    ToolTip(self.btn_add_prod, "Додавання водія")

    # btn_sort = Button(self.zapas_menu,text="SORT")
    # btn_sort.place(x=500,y=80)

    # Призначення обробника подій кліку на заголовок стовпця
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview_column(tree, c))

        def print_doc():
            ...

