from login_and_registration.reestr_form import *
import ttkbootstrap as ttk
from db_connect import *


def add_customer(root, self):
    self.main_menu_but.config(state="disabled")
    self.menu_button.config(state="disabled")
    self.menu_button_dovidku.config(state="disabled")

    popup = Toplevel(root)
    popup.title("Новий замовник")

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
        enter_company.config(highlightbackground="lightgray")
        enter_edrpu.config(highlightbackground="lightgray")
        enter_payment.config(highlightbackground="lightgray")
        enter_e_mail.config(highlightbackground="lightgray")
        enter_adress.config(highlightbackground="lightgray")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        stat.config(style="Custom.TCombobox")

        all_labels = [enter_name.get(), enter_number.get(), enter_company.get(),stat.get(),enter_e_mail.get(),
                      enter_adress.get(),enter_edrpu.get(),enter_payment.get()]

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
                elif field_index == 2:
                    enter_company.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    stat.config(style="Custom.TCombobox")
                elif field_index == 4:
                    enter_e_mail.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 5:
                    enter_adress.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 6:
                    enter_edrpu.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 7:
                    enter_payment.config(highlightbackground="red", highlightcolor="red")

            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля",font=("Arial",12))
            error_lable.place(x=145, y=450)
            error_lable.config(foreground="red")
            return
        else:
            print("Все поля заполнены.")
        # Получаем значение из поля ввода
        try:
            sql_add = f"""
                    INSERT INTO Замовник (ПІБ_контактної_особи, Телефон_замовника,
                     Статус_замовника, e_mail, Назва_підприємства, Адреса,Реквізити_розрахунковий_рахунок_,Код_ЄДРПОУ)
                    VALUES ('{enter_name.get()}', '{enter_number.get()}', '{stat.get()}',
                            '{enter_e_mail.get()}', '{enter_company.get()}', '{enter_adress.get()}',
                             '{enter_payment.get()}', '{enter_edrpu.get()}');"""
            execute_sql_query_insert(conn_str, sql_add)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_customer_menu()
            back_form()
        except Exception as e:
            # Обрабатываем ошибку при выполнении SQL-запроса
            print(f"Ошибка при добавлении категории: {e}")

    ttk.Label(popup, text="Додавання замовника", font=("Arial", 20, "bold")).pack(pady=3)

    new_cust = Label(popup, text="ПІБ замовника:", font=("Arial", 14))
    new_cust.pack(anchor="nw", padx=10, pady=20)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.place(x=210, y=65)

    number_cust = Label(popup, text="Телефон замовника:", font=("Arial", 14))
    number_cust.pack(anchor="nw", padx=10, pady=2)
    enter_number = Entry(popup, width=20, font=("Arial", 12))
    enter_number.place(x=210, y=115)

    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    status = Label(popup, text="Статус замовника: ", font=("Arial", 14))
    status.pack(anchor="nw", padx=10, pady=20)
    stat = ttk.Combobox(popup, width=27,height=3,font=("Arial",8),style="TCombobox")
    stat['values'] = ['Активний','Неактивний']
    stat.place(x=210, y=165)

    email_lbl = Label(popup, text="Пошта:", font=("Arial", 14))
    email_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_e_mail = Entry(popup, width=20, font=("Arial", 12))
    enter_e_mail.place(x=210, y=215)

    company_lbl = Label(popup, text="Підприємство:", font=("Arial", 14))
    company_lbl.pack(anchor="nw", padx=10, pady=20)
    enter_company = Entry(popup, width=20, font=("Arial", 12))
    enter_company.place(x=210, y=265)

    adress_lbl = Label(popup, text="Адреса:", font=("Arial", 14))
    adress_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_adress = Entry(popup, width=20, font=("Arial", 12))
    enter_adress.place(x=210, y=315)

    payment_lbl = Label(popup, text="Реквізити:", font=("Arial", 14))
    payment_lbl.pack(anchor="nw", padx=10, pady=20)
    enter_payment = Entry(popup, width=20, font=("Arial", 12))
    enter_payment.place(x=210, y=365)

    edrpu_lbl = Label(popup, text="Код ЄДРПОУ:", font=("Arial", 14))
    edrpu_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_edrpu = Entry(popup, width=20, font=("Arial", 12))
    enter_edrpu.place(x=210, y=415)

    btn_go = Button(popup, text="Додати", font=("Arial", 14), width=10, command=add)
    btn_go.place(x=185,y=490)

    root_width = popup.winfo_reqwidth()
    root_height = popup.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 550
    # Вычисляем координаты для центрирования
    x_coordinate = self.new_window.winfo_x() + 400 + (root_width - popup_width) // 2
    y_coordinate = self.new_window.winfo_y() + 176 + (root_height - popup_height) // 2

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

def change_customer(root, self):
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
        enter_company.config(highlightbackground="lightgray")
        enter_edrpu.config(highlightbackground="lightgray")
        enter_payment.config(highlightbackground="lightgray")
        enter_e_mail.config(highlightbackground="lightgray")
        enter_adress.config(highlightbackground="lightgray")
        combostyle.configure("Custom.TCombobox", bordercolor="lightgray")
        stat.config(style="Custom.TCombobox")

        all_labels = [enter_name.get(), enter_number.get(), enter_company.get(), stat.get(), enter_e_mail.get(),
                      enter_adress.get(), enter_edrpu.get(), enter_payment.get()]

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
                elif field_index == 2:
                    enter_company.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 3:
                    combostyle.configure("Custom.TCombobox", bordercolor="red")
                    stat.config(style="Custom.TCombobox")
                elif field_index == 4:
                    enter_e_mail.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 5:
                    enter_adress.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 6:
                    enter_edrpu.config(highlightbackground="red", highlightcolor="red")
                elif field_index == 7:
                    enter_payment.config(highlightbackground="red", highlightcolor="red")

            error_lable = Label(popup, text="ПОМИЛКА: Пропущені поля", font=("Arial", 12))
            error_lable.place(x=145, y=450)
            error_lable.config(foreground="red")
            return
        else:
            print("Все поля заполнены.")
        # Получаем значение из поля ввода

        try:

            sql_update_prod = f"""
                    UPDATE Замовник
                    SET ПІБ_контактної_особи = '{enter_name.get()}',
                    Телефон_замовника = '{enter_number.get()}',
                    Статус_замовника = '{stat.get()}',
                    e_mail = '{enter_e_mail.get()}',
                    Назва_підприємства = '{enter_company.get()}',
                    Адреса = '{enter_adress.get()}',
                    Реквізити_розрахунковий_рахунок_ = '{enter_payment.get()}',
                    Код_ЄДРПОУ = '{enter_edrpu.get()}'
                    WHERE Код_замовника = '{self.item_text[0]}'
                """

            execute_sql_query_insert(conn_str, sql_update_prod)
            self.main_menu_but.config(state="normal")
            self.menu_button.config(state="normal")
            self.menu_button_dovidku.config(state="normal")
            self.open_customer_menu()
            back_form()
        except Exception as ex:
            print("Error228: ", ex)

    ttk.Label(popup, text="Редагування замовника", font=("Arial", 20, "bold")).pack()

    new_cust = Label(popup, text="ПІБ замовника:", font=("Arial", 14))
    new_cust.pack(anchor="nw", padx=10, pady=20)
    enter_name = Entry(popup, width=20, font=("Arial", 12))
    enter_name.insert(0, f"{self.item_text[1]}")
    enter_name.place(x=210, y=65)

    number_cust = Label(popup, text="Телефон замовника:", font=("Arial", 14))
    number_cust.pack(anchor="nw", padx=10, pady=2)
    enter_number = Entry(popup, width=20, font=("Arial", 12))
    enter_number.insert(0, f"{self.item_text[2]}")
    enter_number.place(x=210, y=115)

    combostyle = ttk.Style()
    combostyle.configure("TCombobox", font=("Arial", 14))
    status = Label(popup, text="Статус замовника: ", font=("Arial", 14))
    status.pack(anchor="nw", padx=10, pady=20)
    stat = ttk.Combobox(popup, width=27, height=3, font=("Arial", 8), style="TCombobox")
    stat['values'] = ['Активний', 'Неактивний']
    stat.insert(0, f"{self.item_text[3]}")
    stat.place(x=210, y=165)

    email_lbl = Label(popup, text="Пошта:", font=("Arial", 14))
    email_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_e_mail = Entry(popup, width=20, font=("Arial", 12))
    enter_e_mail.insert(0, f"{self.item_text[4]}")
    enter_e_mail.place(x=210, y=215)

    company_lbl = Label(popup, text="Підприємство:", font=("Arial", 14))
    company_lbl.pack(anchor="nw", padx=10, pady=20)
    enter_company = Entry(popup, width=20, font=("Arial", 12))
    enter_company.insert(0, f"{self.item_text[5]}")
    enter_company.place(x=210, y=265)

    adress_lbl = Label(popup, text="Адреса:", font=("Arial", 14))
    adress_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_adress = Entry(popup, width=20, font=("Arial", 12))
    enter_adress.insert(0, f"{self.item_text[6]}")
    enter_adress.place(x=210, y=315)

    payment_lbl = Label(popup, text="Реквізити:", font=("Arial", 14))
    payment_lbl.pack(anchor="nw", padx=10, pady=20)
    enter_payment = Entry(popup, width=20, font=("Arial", 12))
    enter_payment.insert(0, f"{self.item_text[7]}")
    enter_payment.place(x=210, y=365)

    edrpu_lbl = Label(popup, text="Код ЄДРПОУ:", font=("Arial", 14))
    edrpu_lbl.pack(anchor="nw", padx=10, pady=2)
    enter_edrpu = Entry(popup, width=20, font=("Arial", 12))
    enter_edrpu.insert(0, f"{self.item_text[8]}")
    enter_edrpu.place(x=210, y=415)

    btn_go = Button(popup, text="Редагувати", font=("Arial", 14), width=10, command=add)
    btn_go.place(x=185, y=490)

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    # Получаем размеры всплывающего окна
    popup_width = 500
    popup_height = 550
    # Вычисляем координаты для центрирования
    x_coordinate = self.new_window.winfo_x() + 5 + (root_width - popup_width) // 2
    y_coordinate = self.new_window.winfo_y() + 10 + (root_height - popup_height) // 2

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