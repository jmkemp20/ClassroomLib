try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont, END, messagebox  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import json
from BookParser import *


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        self.resizable(False, False)

        self.title("Classroom Card Catalogue")
        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.text_font = tkfont.Font(family='Helvetica', size=14, weight="bold")

        self.studentname = ""

        try:
            f = open("students.json", 'r')
            self.studentdata = json.load(f)
            f.close()
        except FileNotFoundError:
            print("Could not find file: students.json")
            exit(1)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, CheckInPage, CheckInPage2, CheckOutPage, CheckOutPage2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_frame(self, page_name):
        return self.frames[page_name]

    def refresh_json(self):
        try:
            f = open("students.json", 'r')
            self.studentdata = json.load(f)
            f.close()
        except FileNotFoundError:
            print("Could not find file: students.json")
            exit(1)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Classroom Card Catalogue", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Check In", font=controller.text_font,
                            command=lambda: controller.show_frame("CheckInPage"))
        button2 = tk.Button(self, text="Check Out", font=controller.text_font,
                            command=lambda: controller.show_frame("CheckOutPage"))
        button1.pack(side="left", fill="both", expand=True)
        button2.pack(side="right", fill="both", expand=True)


class CheckInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Check In - Choose Your Name", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        return_button = tk.Button(self, text="Return to Main Menu",
                                  command=lambda: controller.show_frame("StartPage"))
        return_button.pack(side="bottom", fill="x")

        checkin_button = tk.Button(self, text="Select", pady=10, font=self.controller.text_font,
                                   command=lambda: self.check_in())
        checkin_button.pack(side="bottom", fill="x")

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        # TODO Move this so it updates everytime the frame is brought forward
        self.nameslist = tk.Listbox(self, yscrollcommand=scrollbar.set, font=controller.text_font)
        for line in controller.studentdata["students"]:
            self.nameslist.insert(END, str(line["name"]) + " (" + str(len(line["book_list"])) + ")")
        self.nameslist.pack(padx=5, pady=5, fill="both", expand=True)
        scrollbar.config(command=self.nameslist.yview)

    def check_in(self):
        if self.nameslist.get(tk.ANCHOR) == "":
            return
        self.controller.studentname = self.nameslist.get(tk.ANCHOR)
        self.controller.show_frame("CheckInPage2")
        CheckInPage2.render(self.controller.get_frame("CheckInPage2"))


class CheckInPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Check In - Choose the Book", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)

        return_button = tk.Button(self, text="Return to Main Menu",
                                  command=lambda: self.go_back())
        return_button.pack(side="bottom", fill="x")

    def render(self):
        print("CheckInPage2: " + self.controller.studentname)
        self.label.destroy()
        self.label = tk.Label(self, text="Check In - " + self.controller.studentname, font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)

        self.checkin_button = tk.Button(self, text="Check In", pady=10, font=self.controller.text_font,
                                        command=lambda: self.check_in())
        self.checkin_button.pack(side="bottom", fill="x")

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        self.student = next(
            (x for x in self.controller.studentdata["students"] if x["name"] == self.controller.studentname), None)

        self.booklist = tk.Listbox(self, yscrollcommand=self.scrollbar.set, font=self.controller.text_font)
        for isbn in self.student["book_list"]:
            temp_string = "\"" + bp.get_title(isbn) + "\" - " + bp.get_author(isbn)
            self.booklist.insert(END, temp_string)
        self.booklist.pack(padx=5, pady=5, fill="both", expand=True)
        self.scrollbar.config(command=self.booklist.yview)

    def go_back(self):
        self.controller.show_frame("StartPage")
        self.scrollbar.destroy()
        self.checkin_button.destroy()
        self.booklist.destroy()

    def check_in(self):
        if self.booklist.get(tk.ANCHOR) != "":
            answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to check in?")
            if answer:
                print("Checking in: " + self.booklist.get(tk.ANCHOR))
                with open('students.json', 'r') as student_data:
                    data = json.load(student_data)

                student = next(
                    (x for x in data["students"] if x["name"] == self.controller.studentname),
                    None)
                for books in range(len(student["book_list"])):
                    if student["book_list"][books]["title"] == self.booklist.get(tk.ANCHOR):
                        del student["book_list"][books]
                        break

                with open('students.json', 'w') as student_data:
                    json.dump(data, student_data)

                self.controller.refresh_json()
                self.go_back()
            else:
                print("Chose not to proceed")
                return
        else:
            print("No Book from list selected")
            return


class CheckOutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Check Out - Choose Your Name", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Return to Main Menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", fill="x")

        checkout_button = tk.Button(self, text="Select", pady=10, font=self.controller.text_font,
                                    command=lambda: self.check_out())
        checkout_button.pack(side="bottom", fill="x")

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.nameslist = tk.Listbox(self, yscrollcommand=scrollbar.set, font=controller.text_font)
        for line in controller.studentdata["students"]:
            self.nameslist.insert(tk.END, str(line["name"]))
        self.nameslist.pack(padx=5, pady=5, fill="both", expand=True)
        scrollbar.config(command=self.nameslist.yview)

    def check_out(self):
        if self.nameslist.get(tk.ANCHOR) == "":
            return
        self.controller.studentname = self.nameslist.get(tk.ANCHOR)
        self.controller.show_frame("CheckOutPage2")
        CheckOutPage2.render(self.controller.get_frame("CheckOutPage2"))


class CheckOutPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Check Out - " + self.controller.studentname, font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)

        return_button = tk.Button(self, text="Return to Main Menu",
                                  command=lambda: self.go_back())
        return_button.pack(side="bottom", fill="x")

    def render(self):
        print("CheckOutPage2: " + self.controller.studentname)
        self.label.destroy()
        self.label = tk.Label(self, text="Check Out - " + self.controller.studentname, font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)

        self.text_label = tk.Label(self, text="Scan Barcode Now:", font=self.controller.text_font)
        self.text_label.pack(side="top", fill="x", pady=20)

        self.isbntext = tk.StringVar(self, value="")

        self.isbn = tk.Entry(self, textvariable=self.isbntext)
        self.isbn.pack(padx=10, pady=10)
        self.isbn.focus()

        self.checkout_button = tk.Button(self, text="Check Out", pady=50, font=self.controller.text_font, command=lambda: self.checkout())
        self.checkout_button.pack(side="bottom", fill="x")

    def checkout(self):
        #: TODO Regular expression for accepting valid ISBN or Input
        #: Do not know what the actual input of the scanner device will be
        isbn = self.isbn.get()
        if isbn == "":
            tk.messagebox.showerror(title="No Input", message="Please scan the barcode on the back of the book")
            return
        elif len(isbn) != 10 and len(isbn) != 13:
            self.isbntext.set("")
            tk.messagebox.showerror(title="Invalid Scan", message="Invalid Scan - Please scan again")
            return
        if not bp.valid_isbn(isbn): # : Checks to see if ISBN is in library
            # TODO Maybe add functionality of adding a book to the library (using set password) - uses api
            self.isbntext.set("")
            tk.messagebox.showerror(title="Invalid ISBN", message="This Book is not part of the library")
            return
        answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to check out?")
        if answer:
            print("Checking out: " + isbn + " for " + self.controller.studentname)
            # TODO This all might change depending on input from scanner device

            with open('students.json', 'r') as student_data:
                data = json.load(student_data)

            student = next(
                (x for x in data["students"] if x["name"] == self.controller.studentname),
                None)
            temp_book = isbn
            book_list = student["book_list"]
            book_list.append(temp_book)

            student["book_list"] = book_list

            with open('students.json', 'w') as student_data:
                json.dump(data, student_data)

            self.controller.refresh_json()
            self.go_back()

    def go_back(self):
        self.isbn.destroy()
        self.checkout_button.destroy()
        self.text_label.destroy()
        self.controller.show_frame("StartPage")


if __name__ == "__main__":
    bp = BookParser("books.csv")
    bp.print_fields()
    bp.print_rows()
    app = SampleApp()
    app.mainloop()
