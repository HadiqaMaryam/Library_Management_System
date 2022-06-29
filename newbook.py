from tkinter import *
from tkinter import messagebox
import sqlite3
con = sqlite3.connect("lms.db")
cur = con.cursor()

class StoreBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("800x800")
        self.title("Store Book")
        self.resizable(False,False)
    
        
        self.top_frame = Frame(self,height=150,bg='grey')
        self.top_frame.pack(fill=X)
        heading = Label(self.top_frame,text='Add New Book',font='arial 18 bold',bg='grey',fg='white')
        heading.place(x=300,y=60)

        self.bodyframe = Frame(self,height=650,bg='white')
        self.bodyframe.pack(fill=X)

        self.lbl_name = Label(self.bodyframe,text='Enter book name:',font='arial 12 bold',bg='white ')
        self.lbl_name.place(x=40,y=40)

        self.txt_book_name = Entry(self.bodyframe,width=30,bd=2)
        self.txt_book_name.place(x=150,y=45)

        self.lbl_author = Label(self.bodyframe,text='Enter Author: ',font='arial 12 bold',bg='white')
        self.lbl_author.place(x=40,y=40)

        self.txt_book_author = Entry(self.bodyframe,width=30,bd=2)
        self.txt_book_author.place(x=200,y=80)

        self.lbl_pages = Label(self.bodyframe,text='Enter Pages: ',font='arial 12 bold',bg='white')
        self.lbl_pages.place(x=40,y=120)

        self.txt_book_pages = Entry(self.bodyframe,width=30,bd=2)
        self.txt_book_pages.place(x=200,y=80)

        savebutton = Button(self.bodyframe, text= "Save Now", command=self.savebook)
        savebutton.place(x=270,y=200)

    def savebook(self):
        bookname = self.txt_book_name.get()
        author = self.txt_book_author.get()
        pages = self.txt_book_pages.get()

        if(bookname and author and pages != ""):
            try:
                query = "INSERT INTO 'books'(book_name, book_author, book_pages )VALUES(?,?,?)"
                cur.execute(query,(bookname,author,pages))
                con.commit()
                messagebox.showinfo("Success","Book has bee saved successfully",icon='info')
            except:
                messagebox.showerror("ERROR","Transaction not commit", icon="warning")
        else:
            messagebox.showerror("ERROR","All fields are mandatory", icon="warning")
