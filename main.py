import tkinter
import mysql.connector
from tkinter import *
from  tkinter import ttk

id = -1
con = mysql.connector.connect(host='localhost', user='root', password= 'amir09135335139')
cur = con.cursor(buffered=True)
try:
    cur.execute('USE registration')
except:
    cur.execute('CREATE DATABASE registration')
    cur.execute('USE registration')
try:
    cur.execute("DESCRIBE persons")
except:
    cur.execute("CREATE TABLE persons(id int primary key auto_increment, name varchar(20), family varchar(20), personid varchar(20), address varchar(50), phonenumber varchar(20))")

def Registration():
    cur.execute(f"INSERT IGNORE INTO persons(name, family, personid, address, phonenumber)VALUES ('{eName.get()}', '{eFamily.get()}', '{ePersonId.get()}', '{eAddress.get()}', '{ePhoneNumber.get()}')")
    con.commit()
    ClearTrv()

def ClearTrv():
    for item in trv.get_children():
        trv.delete(item)
def RefreshTrv():
    ClearTrv()
    cur.execute("SELECT * FROM persons")
    users = cur.fetchall()
    for row in users:
        trv.insert('', END, values=row)

def Find():
    ClearTrv()
    val = eSearch.get()
    cur.execute("SELECT * FROM persons")
    users = cur.fetchall()
    for row in users:
        trv.insert('', END, values=row)

def ClearEntry():
    eName.delete(0,END)
    eFamily.delete(0,END)
    eAddress.delete(0,END)
    ePersonId.delete(0,END)
    ePhoneNumber.delete(0,END)

def OnDoubleClick(event):
    ClearEntry()
    selected = trv.focus()
    values = trv.item(selected, 'values')

    eName.insert(0, values[1])
    eFamily.insert(0, values[2])
    ePersonId.insert(0, values[3])
    eAddress.insert(0, values[4])
    ePhoneNumber.insert(0, values[5])


def UpdateUser():
    name = eName.get()
    family = eFamily.get()
    personid = ePersonId.get()
    address = eAddress.get()
    phonenumbmer = ePhoneNumber.get()

    cur.execute(f"Update persons SET name = {name}, family = {family}, personid = {personid}, address = {address}, phonenumber = {phonenumbmer} WHERE id = {id}")
    RefreshTrv()


window = tkinter.Tk()
window.after_idle(Find)
window.geometry("500x500")
window.title("User Form")

side1 = Frame(window,)
side1.grid(row= 0, column= 0, sticky="nesw")
side2 = Frame(window)
side2.grid(row= 0, column= 1, sticky="nesw")

lbName = tkinter.Label(side1, text="نام")
lbFamily = tkinter.Label(side1, text="نام خانوادگی")
lbPersonId = tkinter.Label(side1, text="کدملی")
lbAddress = tkinter.Label(side1, text="آدرس")
lbPhoneNumber = tkinter.Label(side1, text="تلفن")

lbName.grid(row=1, column=1)
lbFamily.grid(row=2, column=1)
lbPersonId.grid(row=3, column=1)
lbAddress.grid(row=4, column=1)
lbPhoneNumber.grid(row=5, column=1)

eName = tkinter.Entry(side1)
eFamily = tkinter.Entry(side1)
ePersonId = tkinter.Entry(side1)
eAddress= tkinter.Entry(side1)
ePhoneNumber = tkinter.Entry(side1)

eName.grid(row=1, column=2)
eFamily.grid(row=2, column=2)
ePersonId.grid(row=3, column=2)
eAddress.grid(row=4, column=2)
ePhoneNumber.grid(row=5, column=2)

btnAdd = tkinter.Button(side1, text="Add", command=Registration)
btnAdd.grid(row= 6, column=1)

lbSearch = tkinter.Label(side2, text= "Search", font=12)
eSearch = tkinter.Entry(side2)
btnSearch = tkinter.Button(side2, text='search', font=12, bg='blue', fg='#ffffff', command=Find)

trv = ttk.Treeview(side2, columns=(1,2,3,4,5,6), height=15, show="headings")
trv.column(1, anchor=CENTER, stretch=NO, width=100)
trv.column(2, anchor=CENTER, stretch=NO, width=100)
trv.column(3, anchor=CENTER, stretch=NO, width=100)
trv.column(4, anchor=CENTER, stretch=NO, width=100)
trv.column(5, anchor=CENTER, stretch=NO, width=100)
trv.column(6, anchor=CENTER, stretch=NO, width=100)


trv.heading(1, text='ID')
trv.heading(2, text='First Name')
trv.heading(3, text='Last Name')
trv.heading(4, text='Person Id')
trv.heading(5, text='Address')
trv.heading(6, text='Phone Number')

lbSearch.grid(row=1, column=1)
eSearch.grid(row=1, column=2)
btnSearch.grid(row=1, column=3)

trv.grid(row=2, column=1, columnspan=3)
trv.bind("<Double-1>", OnDoubleClick)
window.mainloop()