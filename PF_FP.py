import sqlite3
from tkinter import *
from tkinter import ttk
import importlib
newbookwindow = importlib.import_module("newbook")
memberwindow = importlib.import_module("newmember")
issuebookwindow = importlib.import_module("issuebook") 
con = sqlite3.connect("lms.db")
cur = con.cursor()


class Main(object):
    def __init__(self,master):
        self.master = master

        def show_summary(self):
            book_instock_counter = cur.execute("SELECT COUNT(book_id) FROM books WHERE  book_status = 0").fetchall()
            member_counter = cur.execute("SELECT COUNT(member_id) FROM members").fetchall()
            issued_counter = cur.execute("SELECT COUNT(book_id) FROM books WHERE book_status = 1").fetchall()
            self.lbl_book_count.config(text="IN STOCK: " + str(book_instock_counter[0][0]))
            self.lbl_member_counter.config(text="MEMBERS: " + str(member_counter[0][0]))
            self.lbl_taken_count.config(text="ISSUED: "+ str(issued_counter[0][0]))

        def showbooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()
            counter = 0
            for book in books:
                self.management_box.insert(counter,str(book[0] + "-" + book[1]))
                counter += 1
            
            def bookinfo(evt):
                value = str(self.management_box.get(self.management_box.curselection))
                id = value.split('-')[0]
                self.list_details.delete(0,'end')
                book = cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
                book_info = book.fetchall()    
                self.list_details.insert(0,"Book Name:" + book_info[0][1])
                self.list_details.insert(1,"Author:" + book_info[0][2])
                self.list_details.insert(2,"Pages:" + book_info[0][3])
                if (book_info[0][4] == 0):
                    self.list_details.insert(3,"Status: In Stock")
                else:
                    self.list_details.insert(3,"Status: Issued")

            self.management_box.bind("<<ListboxSelect>>", bookinfo)

        #main Frame
        mainFrame = Frame(self.master)
        mainFrame.pack()

        #Top Frame
        topFrame = Frame(mainFrame,width=900,height=70,borderwidth=2,relief=SUNKEN,padx=20)
        topFrame.pack(side=TOP,fill=X)

        #Add member Button
        self.btn_add_member = Button(topFrame,text=" New Member ",font="arial 12 bold",padx=10, command=self.new_member)
        self.btn_add_member.pack(side=LEFT)

        #Add Book Button
        self.btn_add_book = Button(topFrame,text=" New Book ",font="arial 12 bold",padx=10, command=self.new_book)
        self.btn_add_book.pack(side=LEFT)

        #Issue Book Button
        self.btn_issue_book = Button(topFrame,text=" Issue Book ",font="arial 12 bold",padx=10, command=self.issue_book)
        self.btn_issue_book.pack(side=LEFT)

        #centerFrame
        centerFrame = Frame(mainFrame,width=900,height=800,relief=RIDGE)
        centerFrame.pack(side=TOP)

        #left Frame
        leftFrame = Frame(centerFrame,width=600,height=700,relief=SUNKEN,borderwidth=2)
        leftFrame.pack(side=LEFT)
        self.leftab = ttk.Notebook(leftFrame, width=600, height=600)
        self.leftab.pack()
        self.tab1 = ttk.Frame(self.leftab)
        self.tab2 = ttk.Frame(self.leftab)
        self.leftab.add(self.tab1,text="Management")
        self.leftab.add(self.tab2,text="Summary")
        
        #management
        self.management_box = Listbox(self.tab1, width=40, height=30, font='times 12 bold')
        self.sb = Scrollbar(self.tab1,orient=VERTICAL)
        self.management_box.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.management_box.yview)
        self.management_box.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        self.list_details = Listbox(self.tab1,width=80,height=30,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)

        #summary
        self.lbl_book_count = Label(self.tab2,text="",pady=20,font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_counter = Label(self.tab2,text="",pady=20,font='verdana 14 bold')
        self.lbl_member_counter.grid(row=1,sticky=W)
        self.lbl_taken_count = Label(self.tab2,text="",pady=20,font='verdana 14 bold') 
        self.lbl_taken_count.grid(row=2,sticky=W )
         
        #right Frame
        rightFrame = Frame(centerFrame,width=300,height=700,relief=SUNKEN,borderwidth=2)
        rightFrame.pack()

        #Search Bar in rightFrame
        searchbar = LabelFrame(rightFrame,width=250,height=75,text=" Search ")
        searchbar.pack(fill=BOTH)
        self.lbl_search = Label (searchbar,text="Search Book: ",font="arial 12 bold")
        self.lbl_search.grid(row=0,column=0,padx=20,pady=10)
        self.ent_search = Entry(searchbar,width=30,bd=10)
        self.ent_search.grid(row=0,column=1,columnspan=3,padx=10)
        self.btn_search_btn = Button(searchbar,text="Seach Now",font="arial 12",command=self.search)
        self.btn_search_btn.grid(row=0,column=4,padx=20,pady=10)

        #list Bar
        list_bar = LabelFrame(rightFrame,width=280,height=200,text="Books List",bg="#fff")
        list_bar.pack(fill=BOTH)
        list_lbl = Label(list_bar,text="Sort By",font="times 16")
        list_lbl.grid(row=0,column=2)

        #radio button
        self.listchoice = IntVar()
        rb_all_book = Radiobutton(list_bar,text="Sort All Books",var=self.listchoice,value=1)
        rb_all_book.grid(row=1,column=0)
        rb_in_stock = Radiobutton(list_bar,text="In Stock",var=self.listchoice,value=2)
        rb_in_stock.grid(row=1,column=1)
        rb_issued_book = Radiobutton(list_bar,text="Issue Books",var=self.listchoice,value=3)
        rb_issued_book.grid(row=1,column=2)
        btn_show_books = Button(list_bar,text="Show Books", font='arial 12 bold', command=self.searchsort)
        btn_show_books.grid(row=1,column=3,padx=40,pady=10)

        '''
        #image
        welcome_image = Frame(rightFrame,width=300,height=400)
        welcome_image.pack(fill=BOTH)
        self.welcome_main_image = PhotoImage(file='images/welcome.PNG')
        self.imagelbl = Label(welcome_image, image=self.welcome_main_image)
        self.imagelbl.pack(row=1)
        '''
        showbooks(self)
        show_summary(self)

    def searchsort(self):
        value = self.listchoice.get()
        query = ""
        if value == 1:
            query = "SELECT * FROM books ORDER BY book_name ASC"
        elif value == 2:
            query = "SELECT * FROM books WHERE book_status = 0"
        else:
            query = "SELECT * FROM books WHERE book_status = 1"
        self.management_box.delete(0,END)
        counter = 0
        searchquery = cur.execute(query).fetchall()
        for book in searchquery:
            self.management_box.insert(counter,str(book[0]) + "-" + book[1]) 
            counter += 1

    def issue_book(self):
        add = issuebookwindow.IssueBook()

    def new_book(self):
        add = newbookwindow.StoreBook()
    
    def new_member(self):
        add = memberwindow.StoreMember()

    def search(self):
        value = self.ent_search.get()
        searchquery = cur.execute("SELECT * FROM books WHERE book_name LIKE ?",('%' + value + '%',)).fetchall()
        self.management_box.delete(0,END)
        counter = 0
        
        for book in searchquery:
            self.management_box.insert(counter,str(book[0]) + "-" + book[1]) 
            counter += 1

def main():
    mainwin = Tk()
    app = Main(mainwin)
    mainwin.title("LMS")
    mainwin.geometry('1300x900')
    mainwin.mainloop()
    
if __name__== '__main__':
    main()

