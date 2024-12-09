import tkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk

from menu.the_menu_avto import menu_avto
from menu.the_menu_customer import menu_customer
from menu.the_menu_driver import menu_driver
from menu.the_menu_order_sell import menu_order_sell
from menu.the_menu_spus import menu_spus
from menu.the_menu_ttn import menu_ttn
from processes_menues.do_order_come import *
from processes_menues.do_product import *
from menu.the_menu_category import menu_cat
from menu.the_menu_order_income import menu_order
from menu.the_menu_saveThona import menu_thonas
from menu.the_menu_zapas import menu_zap
from popups import *
from processes_menues.do_category import *
from processes_menues.do_order_come import count_pallets as sum_of_pal

class WarehouseAplc:
    def __init__(self, login_form_instance):
        self.login_form_instance = login_form_instance
        self.new_window = tk.Toplevel(self.login_form_instance.root)
        self.new_window.title("Склад")
        self.new_window.configure(background="white")
        self.new_window.resizable(False, False)
        self.window_width = 1000
        self.window_height = 550
        self.center_window()
        self.frame = ttk.Frame(self.new_window, bootstyle="dark", width=1000, height=35)
        self.frame.pack()
        self.frame_menu = tk.Frame(self.new_window, bg="White")
        self.empty_frame = tk.Frame(self.new_window, bg="White")
        self.zapas_menu = tk.Frame(self.new_window, bg="White")
        self.thona_frame = Frame(self.new_window, bg="White")
        self.categ_frame = Frame(self.new_window, bg="White")
        self.avto_frame = Frame(self.new_window, bg="White")
        self.driver_frame = Frame(self.new_window, bg="White")
        self.oreder_come_menu = tk.Frame(self.new_window, bg="White")
        self.spus_frame = Frame(self.new_window, bg="White")
        self.oreder_sell_menu = tk.Frame(self.new_window, bg="White")
        self.customer_frame = Frame(self.new_window, bg="White")
        self.ttn_frame = Frame(self.new_window, bg="White")
        self.menu_list()
        self.sep = ttk.Separator(self.frame_menu, bootstyle="dark")
        self.sep.pack(padx=400, pady=75, fill=ttk.X)
        self.sclad_names = self.get_scl()
        self.open_image()
        self.check_and_show_menu()
        self.label_text = None
        self.chosen_name = None


    def center_window(self):
        screen_width = self.new_window.winfo_screenwidth()
        screen_height = self.new_window.winfo_screenheight()

        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        self.new_window.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

    def check_and_show_menu(self):
        if len(self.sclad_names) == 0:
            self.create_empty_frame()
            # Приховуємо frame_menu, якщо таблиця порожня
            self.frame.pack_forget()
        else:
            self.new_window.withdraw()
            choose_manu(self.new_window,self)



    def open_image(self):
        try:
            original_image_prod = Image.open('../images/free-icon-product-3712193.png')
            resized_image_prod = original_image_prod.resize((60, 60))
            self.prod = ImageTk.PhotoImage(resized_image_prod)

            original_image_plus = Image.open('../images/free-icon-plus-1828819.png')
            resized_image_plus = original_image_plus.resize((40, 40))
            self.plus = ImageTk.PhotoImage(resized_image_plus)

            original_image_plus2 = Image.open('../images/free-icon-plus-4315609.png')
            plus_small = original_image_plus2.resize((15,15))
            self.plusic = ImageTk.PhotoImage(plus_small)

            original_image_minus = Image.open('../images/free-icon-minus-7080604.png')
            minus = original_image_minus.resize((15, 15))
            self.minus = ImageTk.PhotoImage(minus)

            original_image_new = Image.open('../images/free-icon-new-arrivals-2038989.png')
            resized_image_new = original_image_new.resize((60, 60))
            self.new_pr = ImageTk.PhotoImage(resized_image_new)

            original_image_del = Image.open('../images/free-icon-economy-3258522.png')
            resized_image_del = original_image_del.resize((60, 60))
            self.del_pr = ImageTk.PhotoImage(resized_image_del)

            original_image_zam = Image.open('../images/free-icon-costumer-service-8401035.png')
            resized_image_zam = original_image_zam.resize((60, 60))
            self.zam = ImageTk.PhotoImage(resized_image_zam)

            original_image_empty = Image.open('../images/emp.jpg')
            resized_image_empty = original_image_empty.resize((170, 180))
            self.empty_box = ImageTk.PhotoImage(resized_image_empty)

            original_image_spus = Image.open('../images/free-icon-remove-folder-circular-button-9000447.png')
            resized_image_spus = original_image_spus.resize((95, 95))
            self.spus = ImageTk.PhotoImage(resized_image_spus)

            original_image_nak = Image.open('../images/free-icon-delivered-1433287.png')
            resized_image_nak = original_image_nak.resize((60, 60))
            self.nak = ImageTk.PhotoImage(resized_image_nak)

            original_image_back = Image.open('../images/free-icon-left-arrow-3272639.png')
            resized_image_back= original_image_back.resize((30, 30))
            self.back = ImageTk.PhotoImage(resized_image_back)

            original_image_add = Image.open('../images/free-icon-add-button-777.png')
            resized_image_add = original_image_add.resize((30, 30))
            self.add_prod_im = ImageTk.PhotoImage(resized_image_add)

            original_addprodmain = Image.open('../images/free-icon-add-cart-8414806.png')
            resized_addprodmain = original_addprodmain.resize((45, 45))
            self.add_prodmain = ImageTk.PhotoImage(resized_addprodmain)

            original_del_prod= Image.open('../images/free-icon-remove-folder-circular-button-9000447.png')
            resized_del_prod = original_del_prod.resize((60, 60))
            self.del_prodmain = ImageTk.PhotoImage(resized_del_prod)

            original_cnahge_prod = Image.open('../images/free-icon-pen-10976933.png')
            resized_cnahge_prod = original_cnahge_prod.resize((40, 40))
            self.change_prodmain = ImageTk.PhotoImage(resized_cnahge_prod)

            original_find = Image.open('../images/free-icon-search-4024513.png')
            resized_cnahge_find = original_find.resize((25, 25))
            self.find = ImageTk.PhotoImage(resized_cnahge_find)

            original_find = Image.open('../images/free-icon-edit-1040228.png')
            resized_cnahge_find = original_find.resize((25, 25))
            self.edit_scl = ImageTk.PhotoImage(resized_cnahge_find)

            original_find = Image.open('../images/free-icon-delete-6932392.png')
            resized_cnahge_find = original_find.resize((40, 40))
            self.del_scl = ImageTk.PhotoImage(resized_cnahge_find)

            original_find = Image.open('../images/free-icon-clean-up-11261598.png')
            resized_cnahge_find = original_find.resize((40, 40))
            self.delete_all = ImageTk.PhotoImage(resized_cnahge_find)

            original_find = Image.open('../images/free-icon-paper-printer-4388519.png')
            resized_cnahge_find = original_find.resize((40, 40))
            self.printer = ImageTk.PhotoImage(resized_cnahge_find)

            original_find = Image.open('../images/free-icon-stamp-5442020.png')
            resized_cnahge_find = original_find.resize((40, 40))
            self.printer2 = ImageTk.PhotoImage(resized_cnahge_find)

        except Exception as e:
            print(f"Error loading images: {e}")

    def create_empty_frame(self):
        # Создаем новый фрейм
        self.empty_frame.pack(fill='both', expand=True)
        # Создаем и размещаем виджеты в фрейме
        label_box = tk.Label(self.empty_frame, bg="White", image=self.empty_box)
        label_box.place(x=415, y=100)

        label_name_empt = tk.Label(self.empty_frame, bg="White", font=("Arial", 18),
                                   text="Жодного складу не виявлено...")
        label_name_empt.place(x=320, y=50)

        label_name_empt2 = tk.Label(self.empty_frame, bg="White", font=("Arial", 16), text="Бажаєте додати?")
        label_name_empt2.place(x=425, y=300)

        label_plus = tk.Button(self.empty_frame, image=self.plus,command=lambda: entry_data(self.new_window, self))
        label_plus.place(x=490, y=340)
        label_plus.config(background="White",highlightbackground="White",activebackground="white")

        label_plus.mainloop()
    def choos_manu(self):
        self.show_menu()


    def menu_list(self):
        style = ttk.Style()
        style.configure("success.TButton",
                        padding=(8, 8))  # Перший аргумент - відступ вгору і вниз, другий - відступ ліворуч і праворуч
        self.menu_button = ttk.Button(self.frame, text="Склад", command=self.choos_manu, style="success.TButton")
        self.menu_button.place(x=1, y=1)

        self.main_menu_but = ttk.Button(self.frame, text="Головне меню", command=self.show_main_manu,padding=(8,8))
        self.main_menu_but.place(x=55, y=1)



        self.menu_button_dovidku = ttk.Button(self.frame, text="Довідки", command=self.dovidku,padding=(8,8))
        self.menu_button_dovidku.place(x=157, y=1)


    def open_category_menu(self):
        menu_cat(self)
    def open_driver_menu(self):
        menu_driver(self)
    def open_avto_menu(self):
        menu_avto(self)
    def open_save_menu(self):
        menu_thonas(self)
    def open_zapas_menu(self):
        menu_zap(self)
    def open_spus_menu(self):
        menu_spus(self)
    def open_order_incm_menu(self):
        menu_order(self)
    def open_order_sell_menu(self):
        menu_order_sell(self)
    def open_customer_menu(self):
        menu_customer(self)
    def open_ttn_menu(self):
        menu_ttn(self)

    def show_main_manu(self):
        if self.zapas_menu.winfo_ismapped():
            self.zapas_menu.pack_forget()
            self.menu(self.chosen_name)

        if self.oreder_come_menu.winfo_ismapped():
            self.oreder_come_menu.pack_forget()
            self.menu(self.chosen_name)

        if self.thona_frame.winfo_ismapped():
            self.thona_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.categ_frame.winfo_ismapped():
            self.categ_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.avto_frame.winfo_ismapped():
            self.avto_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.driver_frame.winfo_ismapped():
            self.driver_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.customer_frame.winfo_ismapped():
            self.customer_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.oreder_sell_menu.winfo_ismapped():
            self.oreder_sell_menu.pack_forget()
            self.menu(self.chosen_name)

        if self.spus_frame.winfo_ismapped():
            self.spus_frame.pack_forget()
            self.menu(self.chosen_name)

        if self.ttn_frame.winfo_ismapped():
            self.ttn_frame.pack_forget()
            self.menu(self.chosen_name)

    def menu(self,chosen_name):
        def del_c_scl():
            sql_query = f"""SELECT Код_складу FROM Склад WHERE  Назва_складу = %s"""
            params = (self.chosen_name,)
            scl_id = execute_sql_query_get(conn_str, sql_query, params)
            print(scl_id[0][0])

            sql_queries = [
                "DELETE FROM Акт_списання WHERE Код_складу = %s;",
                "DELETE FROM ТТН WHERE Код_складу = %s;",
                "DELETE FROM Ордер_вибуття WHERE Код_складу = %s;",
                "DELETE FROM Ордер_надходження WHERE Код_складу = %s;",
                "DELETE FROM Продукція WHERE Код_складу = %s;",
                "DELETE FROM Категорія WHERE Код_складу = %s;",
                "DELETE FROM Зона_зберігання WHERE Код_складу = %s;",
                "DELETE FROM Склад WHERE Код_складу = %s;"
            ]

            # Виконання SQL-запитів для очищення таблиць
            for sql_query in sql_queries:
                params = (scl_id[0][0],)
                execute_sql_query_insert(conn_str, sql_query, params)
            if len(get_scl())>=1:
                self.menu(get_scl()[0][-1])
            else:
                self.frame_menu.pack_forget()
                self.create_empty_frame()

        self.frame_menu.pack_forget()
        self.frame_menu.pack(fill='both', expand=True)
        self.chosen_name = chosen_name
        if hasattr(self, 'name'):
            self.name.destroy()
        self.name = tk.Label(self.frame_menu, bg="White", bd=0, text=self.chosen_name, font=("Arial", 25))
        self.name.place(relx=0.5, rely=0.1, anchor="center")

        self.del_current_scl = Button(self.frame_menu,image=self.del_scl,command=del_c_scl,background="White")
        self.del_current_scl.place(x=357, y=36)
        self.del_current_scl.config(background="White", highlightbackground="White", activebackground="white")

        self.edit_scl_name = Button(self.frame_menu,image=self.edit_scl,background="White",command=lambda :change_scl(self,self.new_window,chosen_name))
        self.edit_scl_name.place(x=600,y=40)
        self.edit_scl_name.config(background="White", highlightbackground="White", activebackground="white")


        label1 = tk.Label(self.frame_menu, image=self.prod, bg="White")
        label1.place(x=190, y=120)

        button_product = tk.Button(self.frame_menu, background="White", text="Запаси товарів", font=("Arial", 16),
                                   bd=3, bg="cornsilk1", command=self.open_zapas_menu, height=2, width=15,
                                   highlightbackground="black", borderwidth=2, relief=tk.RIDGE)
        button_product.place(x=270, y=120)

        label2 = tk.Label(self.frame_menu, image=self.new_pr, bg="White")
        label2.place(x=190, y=200)

        button_new_product = tk.Button(self.frame_menu, background="White", text="Надходження", font=("Arial", 16),
                                       bd=3, bg="cornsilk1", command=self.open_order_incm_menu, height=2, width=15,
                                       highlightbackground="black", borderwidth=2, relief=tk.RIDGE)
        button_new_product.place(x=270, y=200)

        label3 = tk.Label(self.frame_menu, image=self.del_pr, bg="White")
        label3.place(x=185, y=280)

        button_del_product = tk.Button(self.frame_menu, background="White", text="Продаж", font=("Arial", 16),
                                       bd=3, bg="cornsilk1", command=self.open_order_sell_menu, height=2, width=15,
                                       highlightbackground="black", borderwidth=2, relief=tk.RIDGE)
        button_del_product.place(x=270, y=280)

        label4 = tk.Label(self.frame_menu, image=self.zam, bg="White")
        label4.place(x=750, y=283)

        button_zam = tk.Button(self.frame_menu, background="White", text="Клієнти", font=("Arial", 16),
                               bd=3, bg="cornsilk1", command=self.open_customer_menu, height=2, width=15,
                               highlightbackground="black", borderwidth=2, relief=tk.RIDGE)
        button_zam.place(x=540, y=280)

        label5 = tk.Label(self.frame_menu, image=self.spus, bg="White")
        label5.place(x=740, y=187)

        button_spus = tk.Button(self.frame_menu, background="White", text="Списання", font=("Arial", 16),
                               bd=3, bg="cornsilk1", command=self.open_spus_menu, height=2, width=15,
                               highlightbackground="black", borderwidth=2, relief=tk.RIDGE)
        button_spus.place(x=540, y=200)

        label6 = tk.Label(self.frame_menu, image=self.nak, bg="White")
        label6.place(x=750, y=117)

        button_nak = tk.Button(self.frame_menu, background="White", font=("Arial", 16),
                                bd=3, bg="cornsilk1", command=self.open_ttn_menu, height=2, width=15,
                                highlightbackground="black", borderwidth=2, relief=tk.RIDGE,
                               text="ТТН")
        button_nak.place(x=540, y=120)

        def on_close_child_window():
            # Уничтожаем окно при его закрытии
            self.login_form_instance.root.destroy()

        # Назначаем обработчик закрытия окна
        self.new_window.protocol("WM_DELETE_WINDOW", on_close_child_window)

    def get_scl(self):
        sql_query = "SELECT * FROM Склад;"
        return execute_sql_query_get(conn_str, sql_query)

    def get_th(self):
        sql_query = "SELECT * FROM Зона_зберігання;"
        return execute_sql_query_get(conn_str, sql_query)

    def show_menu(self):
        def dow(name):
            #self.current_sclad_id = name[0]
            self.frame_menu.forget()
            self.menu(name)
            self.update_label(name)
            if self.zapas_menu.winfo_ismapped():
                self.zapas_menu.forget()
                self.open_zapas_menu()

            if self.oreder_come_menu.winfo_ismapped():
                self.oreder_come_menu.forget()
                self.open_order_incm_menu()

            if self.thona_frame.winfo_ismapped():
                self.thona_frame.forget()
                self.open_save_menu()

            if self.categ_frame.winfo_ismapped():
                self.categ_frame.forget()
                self.open_category_menu()

            if self.avto_frame.winfo_ismapped():
                self.avto_frame.forget()
                self.open_avto_menu()

            if self.driver_frame.winfo_ismapped():
                self.driver_frame.forget()
                self.open_driver_menu()

            if self.customer_frame.winfo_ismapped():
                self.customer_frame.forget()
                self.open_customer_menu()

            if self.spus_frame.winfo_ismapped():
                self.spus_frame.forget()
                self.open_spus_menu()

            if self.ttn_frame.winfo_ismapped():
                self.ttn_frame.forget()
                self.open_ttn_menu()

            if self.oreder_sell_menu.winfo_ismapped():
                self.oreder_sell_menu.forget()
                self.open_order_sell_menu()


        menu = tk.Menu(self.frame, tearoff=0)
        submenu = tk.Menu(menu, tearoff=0)
        submenu.configure(bg="white", fg="black", activebackground="cornflower blue", activeforeground="black")
        for index, name_tuple in enumerate(self.get_scl()):
            name = [name_tuple[0], name_tuple[1]]
            submenu.add_command(label=name[1], command = lambda name=name_tuple[1]: dow(name))  # Правильна функція lambda
            submenu.add_separator()  # Add separator after each submenu item

        menu.add_cascade(label="Завантажити", menu=submenu)
        menu.add_command(label="Додати", image=self.plusic, compound="right",
                         command=lambda: entry_data(self.new_window, self))

        menu.configure(bg="white", fg="black", activebackground="cornflower blue", activeforeground="black")

        x = self.new_window.winfo_rootx()
        y = self.new_window.winfo_rooty()

        menu.post(x, y + 35)

    def dovidku(self):

        menu = tk.Menu(self.frame, tearoff=0)

        menu.add_command(label="Зони зберігання", compound="right",
                         command=self.open_save_menu)
        menu.add_command(label="Категорії", command=self.open_category_menu)
        menu.add_command(label="Водії", compound="right",command=self.open_driver_menu)
        menu.add_command(label="Авто", compound="right",command=self.open_avto_menu)

        menu.configure(bg="white", fg="black", activebackground="cornflower blue", activeforeground="black")

        x = self.new_window.winfo_rootx()
        y = self.new_window.winfo_rooty()

        menu.post(x + 156, y + 35)

    def delete_data(self):
        delete_scl(self.new_window,self)

    def update_label(self, new_text):
        self.chosen_name = new_text

        # Update the text of the warehouse name in the main menu
        if self.frame_menu.winfo_ismapped():
            self.name.config(text=self.chosen_name)
        else:
            self.menu(new_text)

    def check_data(self):
        existing_names = [name[1] for name in get_scl()]
        if not existing_names:
            self.frame_menu.pack_forget()
            self.create_empty_frame()
        else:
            self.empty_frame.pack_forget()
            #self.menu(existing_names[-1])




