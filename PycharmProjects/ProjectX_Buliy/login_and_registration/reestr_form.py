import threading
from  tkinter import Tk, Label, StringVar, Entry, FLAT, Button, Canvas, Toplevel
from PIL import Image, ImageTk
from popups import *
from db_connect import *
from short_inf_popups import error_saving_psw, success_login


class RegistrationForm:
    def __init__(self, login_form_instance):
        self.window1_instance = login_form_instance
        self.new_window = Toplevel(login_form_instance.root)
        self.new_window.title("Реєстрація")
        self.new_window.configure(background="white")
        self.window_width = 500
        self.window_height = 600
        self.entry_widgets = {}
        self.error_labels = {}  # Initialize error_labels here
        self.center_window()
        self.configure_second_form()


    def open_login(self):
        self.new_window.withdraw()
        self.window1_instance.show()

    def login_button_clicked(self):
        self.b_entr.config(state="disabled")  # Disable the button
        self.new_window.after(2000, self.enable_button)  # Re-enable the button after 5000 milliseconds (5 seconds)
        threading.Thread(target=self.process_registration).start()

    def enable_button(self):
        self.b_entr.config(state="normal")  # Re-enable the button

    def contains_digits_or_symbols(self, text):
        return any(char.isdigit() or not char.isalpha() for char in text)

    def process_registration(self):
        for label in self.error_labels.values():
            label.destroy()

        father_name = self.entrf.get()
        psw = self.entr_psw.get()
        psw2 = self.entr_psw2.get()
        name = self.entry_name.get()
        lastname = self.entr2.get()
        email = self.entry_email.get()

        # Перевірка на наявність хоча б одного непорожнього поля

        fields = {'entry1': name, 'entry2': lastname, 'entryf': father_name, 'entry3': psw,
                  'entry4': psw2, 'entry_email': email}
        empty_fields = []


        for field_name, field_value in fields.items():
            entry_widget = self.entry_widgets[field_name]

            if not field_value:
                empty_fields.append(field_name)
                entry_widget.config(highlightbackground="red", highlightthickness=0.5)
                entry_x = entry_widget.winfo_x()
                entry_y = entry_widget.winfo_y()

                self.error_labels[field_name] = Label(self.new_window, font=("Arial", 8), text="Це поле обов'язкове!",
                                                      fg="red", bg="White")
                self.error_labels[field_name].place(x=entry_x + entry_widget.winfo_width() - 113,
                                                    y=entry_y + 35)
            else:
                entry_widget.config(highlightthickness=0)

        name_keys = ['entry1', 'entry2', 'entryf']

        for key, name_part in zip(name_keys, [name, lastname, father_name]):
            if name_part and not name_part.isalpha():
                entry_widget = self.entry_widgets[key]
                entry_widget.config(highlightbackground="red", highlightthickness=0.5)
                entry_x = entry_widget.winfo_x()
                entry_y = entry_widget.winfo_y()

                self.error_labels[key] = Label(self.new_window, font=("Arial", 8),
                                               text="Некоректне введення!",
                                               fg="red", bg="White")
                self.error_labels[key].place(x=entry_x + entry_widget.winfo_width() - 120,
                                                    y=entry_y + 35)
                return
        if len(psw) > 0 and len(psw) < 3:
            self.error_labels['entry3'] = Label(self.new_window, font=("Arial", 8),
                                                text="Занадто короткий пароль!",
                                                fg="red", bg="White")
            self.error_labels['entry3'].place(x=self.entry3.winfo_x() + self.entry3.winfo_width() - 140,
                                              y=self.entry3.winfo_y() + 35)
            return

        if psw2 != psw and len(psw)>0 and len(psw2)>0:
            error_saving_psw(self.new_window)
            return
        if not empty_fields:
            for field_name in self.error_labels.keys():
                if field_name not in empty_fields:
                    self.error_labels[field_name].destroy()
            sql_query = f"INSERT INTO Співробітник (ПІБ_співробітника, Пароль, e_mail) VALUES (N'{name} {lastname}" \
                        f" {father_name}', N'{psw}',N'{email}');"
            execute_sql_query_insert(conn_str, sql_query)

            self.open_login()
            success_login(self.new_window)

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.entry3.config(show="*")
            self.toggle_button.config(image=self.hide_image, compound="right", bd=0, relief=FLAT)
        else:
            self.entry3.config(show="")
            self.toggle_button.config(image=self.show_image, compound="right", bd=0, relief=FLAT)

    def toggle_password2(self):
        self.show_password2 = not self.show_password2
        if self.show_password2:
            self.entry4.config(show="*")
            self.toggle_button2.config(image=self.hide_image, compound="right", bd=0, relief=FLAT)
        else:
            self.entry4.config(show="")
            self.toggle_button2.config(image=self.show_image, compound="right", bd=0, relief=FLAT)

    def configure_second_form(self):
        self.show_password = True
        self.show_password2 = True

        self.label_descr1 = Label(self.new_window, text="Реєстрація", font=("Arial", 18), background="White")
        self.label_descr1.pack(pady=20)

        self.descr_name = Label(self.new_window, text="Ім'я", background="White")
        self.descr_name.pack(padx=(0, 228))

        self.entry_name = StringVar()
        self.entry1 = Entry(self.new_window, width=30, textvariable=self.entry_name, font=("Arial", 11), bd=1.0,background="alice blue")
        self.entry1.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entry1'] = self.entry1

        self.descr_f = Label(self.new_window, text="Прізвище", background="White")
        self.descr_f.pack(padx=(0, 195))

        self.entr2 = StringVar()
        self.entry2 = Entry(self.new_window, width=30, textvariable=self.entr2, font=("Arial", 11), bd=1.0,background="alice blue")
        self.entry2.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entry2'] = self.entry2

        self.descr_b = Label(self.new_window, text="По батькові", background="White")
        self.descr_b.pack(padx=(0, 195))

        self.entrf = StringVar()
        self.entryf = Entry(self.new_window, width=30, textvariable=self.entrf, font=("Arial", 11), bd=1.0,background="alice blue")
        self.entryf.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entryf'] = self.entryf

        self.descr_psw1 = Label(self.new_window, text="Пароль", background="White")
        self.descr_psw1.pack(padx=(0, 205))

        self.entr_psw = StringVar()
        self.entry3 = Entry(self.new_window, width=30, textvariable=self.entr_psw, show="*", font=("Arial", 11), bd=1.0,background="alice blue")
        self.entry3.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entry3'] = self.entry3

        self.descr_psw2 = Label(self.new_window, text="Введіть повторно пароль", background="White")
        self.descr_psw2.pack(padx=(0, 112))
        self.entr_psw2 = StringVar()
        self.entry4 = Entry(self.new_window, width=30, textvariable=self.entr_psw2, show="*", font=("Arial", 11), bd=1.0,background="alice blue")
        self.entry4.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entry4'] = self.entry4

        self.descr_email = Label(self.new_window, text="Введіть e-mail", background="White")
        self.descr_email.pack(padx=(0, 172))
        self.entry_email = StringVar()
        self.entry_em = Entry(self.new_window, width=30, textvariable=self.entry_email, font=("Arial", 11), bd=1.0,background="alice blue")
        self.entry_em.pack(pady=(0, 15), ipady=3)
        self.entry_widgets['entry_email'] = self.entry_em

        original_image_hide = Image.open('../images/closed.png')
        resized_image_hide = original_image_hide.resize((23, 22))
        self.hide_image = ImageTk.PhotoImage(resized_image_hide)

        original_image_show = Image.open('../images/showed.png')
        resized_image_show = original_image_show.resize((23, 22))
        self.show_image = ImageTk.PhotoImage(resized_image_show)

        self.toggle_button = Button(self.new_window, height=20, width=20, image=self.hide_image,
                                    command=self.toggle_password, background="white", bd=0)
        self.toggle_button.place(x=380, y=291)

        self.toggle_button2 = Button(self.new_window, height=20, width=20, image=self.hide_image,
                                     command=self.toggle_password2, activebackground="white", bd=0)
        self.toggle_button2.place(x=380, y=355)

        self.b_entr = Button(self.new_window, width=20, text="Зареєструватись", command=self.login_button_clicked,
                             background="DodgerBlue4", bd=1, font=("Arial", 12, "bold"), activebackground="white",
                             foreground="white")
        self.b_entr.pack(pady=20)
        marker1_image = Image.open('../images/free-icon-edit-4675243.png')
        res_marker1 = marker1_image.resize((30, 30))
        marker1 = ImageTk.PhotoImage(res_marker1)
        lmarker1 = Label(self.new_window, image=marker1, background="white")
        lmarker1.place(x=85, y=87)

        lmarker2 = Label(self.new_window, image=marker1, background="white")
        lmarker2.place(x=85, y=152)

        lmarker3 = Label(self.new_window, image=marker1, background="white")
        lmarker3.place(x=85, y=218)

        mark_lock = Image.open('../images/free-icon-lock-8472244.png')
        res_mark_lock = mark_lock.resize((37, 37))
        marker_lock = ImageTk.PhotoImage(res_mark_lock)

        lmarker4 = Label(self.new_window, image=marker_lock, background="white")
        lmarker4.place(x=80, y=278)

        lmarker5 = Label(self.new_window, image=marker_lock, background="white")
        lmarker5.place(x=80, y=342)

        mark_email = Image.open('../images/free-icon-close-note-70308.png')
        res_mark_email = mark_email.resize((25, 30))
        mark_em = ImageTk.PhotoImage(res_mark_email)
        lmarker6 = Label(self.new_window, image=mark_em, background="white")
        lmarker6.place(x=86, y=415)

        back_mark = Image.open('../images/free-icon-back-2099190.png')
        res_back_mark = back_mark.resize((40, 40))
        mark_back = ImageTk.PhotoImage(res_back_mark)

        button_back = Button(self.new_window, image=mark_back, command=self.open_login, background='white', bd=0, activebackground='white')
        button_back.place(x=30, y=20)

        self.new_window.mainloop()

    def center_window(self):
        screen_width = self.new_window.winfo_screenwidth()
        screen_height = self.new_window.winfo_screenheight()

        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        self.new_window.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")



