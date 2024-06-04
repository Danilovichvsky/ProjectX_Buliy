from tkinter import *

from PIL import ImageTk

from reestr_form import RegistrationForm
from menu.main_menu import WarehouseAplc
from popups import *

class LoginForm:
    hide_image = None

    def __init__(self):
        self.root = Tk()
        self.root.title('Вхід')
        #self.open_form3()
        self.window_width = 700
        self.window_height = 400
        self.center_window()
        self.root.configure(background='white')
        self.show_password = True
        self.entry_widgets = {}
        self.error_labels = {}
        self.data_wrong = Label(self.root, font=('Arial', 8), text="Такого користувача не має",
                                fg='red', bg='White')

        try:
            self.original_image_hide = Image.open('../images/closed.png')
            resized_image_hide = self.original_image_hide.resize((23, 22))
            self.hide_image = ImageTk.PhotoImage(resized_image_hide)

            self.original_image_show = Image.open('../images/showed.png')
            resized_image_show = self.original_image_show.resize((23, 22))
            self.show_image = ImageTk.PhotoImage(resized_image_show)

            self.auth = Image.open('../images/aut.jpg')
            resized_image_auth = self.auth.resize((230, 400))
            self.auth_image = ImageTk.PhotoImage(resized_image_auth)
        except Exception as e:
            print(f'Error loading images: {e}')

        self.create_widgets()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.entry2.config(show='*')
            self.toggle_button.config(image=self.hide_image, compound='right', bd=0, relief=FLAT)
        else:
            self.entry2.config(show='')
            self.toggle_button.config(image=self.show_image, compound='right', bd=0, relief=FLAT)

    def go_log(self):
        #self.show_loading_label()
        #threading.Thread(target=self.login_button_clicked_threaded).start()
        self.login_button_clicked_threaded()

    def login_button_clicked_threaded(self):
        self.data_wrong.place_forget()  # Hide the error message if login_and_registration successful
        # Отримуємо значення з полів вводу
        name = self.entr1.get()
        password = self.entr2.get()

        # Проверяем, существует ли атрибут data_wrong

        fields = {'entry1': name, 'entry2': password}
        empty_fields = []
        for field_name, field_value in fields.items():
            entry_widget = self.entry_widgets[field_name]

            if not field_value:
                empty_fields.append(field_name)
                entry_widget.config(highlightbackground="red", highlightthickness=0.5)
                entry_x = entry_widget.winfo_x()
                entry_y = entry_widget.winfo_y()

                # Якщо мітка помилки не існує, створіть її
                if field_name not in self.error_labels:
                    self.error_labels[field_name] = Label(self.root, font=('Arial', 8), text="Це поле обов'язкове!",
                                                          fg='red', bg='White')
                    self.error_labels[field_name].place(x=entry_x + 175, y=entry_y + 25)
            else:
                entry_widget.config(highlightthickness=0)  # Скидаємо рамку, якщо поле не пусте
                if field_name in self.error_labels:
                    self.error_labels[field_name].destroy()
                    del self.error_labels[field_name]

        # Якщо є порожні поля, припиняємо обробку
        if empty_fields:
            return

        # Виконуємо SQL-запит з використанням параметризованого запиту
        sql_query = "SELECT * FROM Співробітник WHERE ПІБ_співробітника = %s AND Пароль = %s;"
        params = (name, password)
        res = execute_sql_query_get(conn_str, sql_query, params)
        if res and len(res) > 0:
            self.open_form3()
        else:
            self.data_wrong.place(x=462, y=185)  # Размещаем метку, если данные введены неверно

    def open_second_window(self):
        self.root.withdraw()
        RegistrationForm(self)

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    def open_form3(self):
        self.root.withdraw()
        WarehouseAplc(self)


    def create_widgets(self):
        aut_label = Label(self.root, image=self.auth_image, background='White')
        aut_label.place(x=30, y=5)

        descr = Label(self.root, text='Вхід', font=('Arial', 18, 'bold'), background='White')
        descr.place(x=432, y=20)

        self.entr1 = StringVar()
        self.entry1 = Entry(self.root, textvariable=self.entr1, width=35, font=('Arial', 11), background='alice blue')
        self.entry1.place(x=320, y=100)
        self.entry_widgets['entry1'] = self.entry1

        self.entr2 = StringVar()
        self.entry2 = Entry(self.root, textvariable=self.entr2, width=35, show='*', font=('Arial', 11),
                            background='alice blue')
        self.entry2.place(x=320, y=160)
        self.entry_widgets['entry2'] = self.entry2

        descr_f = Label(self.root, text='Співробітник', font=('Arial', 8), background='White')
        descr_f.place(x=320, y=80)
        descr_s = Label(self.root, text='Пароль', font=('Arial', 8), background='White')
        descr_s.place(x=320, y=140)

        self.toggle_button = Button(self.root, height=20, width=20, image=self.hide_image, command=self.toggle_password,
                                    bd=0)
        self.toggle_button.place(x=620, y=159)

        b_entr = Button(self.root, width=30, text='Увійти', command=self.go_log)
        b_entr.place(x=350, y=220)

        can = Canvas(self.root)
        can.create_line(20, 25, 95, 25)
        can.configure(background='White', highlightbackground='White')
        can.place(x=331, y=250)

        label_or = Label(self.root, text='Або', background='White')
        label_or.place(x=442, y=265)

        can2 = Canvas(self.root)
        can2.create_line(15, 25, 95, 25)  # Adjusted coordinates for the shorter line
        can2.configure(background='White', highlightbackground='White')
        can2.place(x=474, y=250)

        reestr_but = Button(self.root, text='Реєстрація', width=30, command=self.open_second_window)
        reestr_but.place(x=350, y=302)

        def on_close_child_window():
            # Уничтожаем окно при его закрытии
            self.root.destroy()

        # Назначаем обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", on_close_child_window)

        self.root.resizable(False, False)

        self.root.mainloop()

if __name__ == "__main__":
    start = LoginForm()


