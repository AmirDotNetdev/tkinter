import tkinter
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

selected = False

window = tkinter.Tk()
window.geometry("1250x500")
window.title("User Form")

side1 = Frame(window)
side1.grid(row=0, column=0, sticky="nesw")
side2 = Frame(window)
side2.grid(row=0, column=1, sticky="nesw")

con = mysql.connector.connect(host='localhost', user='root', password='amir09135335139')
cur = con.cursor(buffered=True)

try:
    cur.execute('USE registration')
except:
    cur.execute('CREATE DATABASE registration')
    cur.execute('USE registration')
try:
    cur.execute("DESCRIBE persons")
except:
    cur.execute(
        "CREATE TABLE persons(id int primary key auto_increment, name varchar(20), family varchar(20), personid varchar(20), address varchar(50), phonenumber varchar(20))")


def Registration():
    global id
    query_check = "SELECT * FROM persons WHERE id = %s"
    query_insert = (
        "INSERT INTO persons (name, family, personid, address, phonenumber) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    values_check = (id,)

    try:
        cur.execute(query_check, values_check)
        existing_record = cur.fetchone()

        if existing_record:
           confrimed = messagebox.showerror("Error","Record already exists, skipping insertion.")
           if confrimed:
               id = None
        else:
            values_insert = (eName.get(), eFamily.get(), ePersonId.get(), eAddress.get(), ePhoneNumber.get())
            cur.execute(query_insert, values_insert)
            con.commit()
            messagebox.askyesno("Success", "Registration successful!")
            ClearTrv()
            RefreshTrv()

    except Exception as e:
        con.rollback()
        print(f"Error during registration: {e}")



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
    cur.execute("SELECT * FROM persons")
    users = cur.fetchall()
    for row in users:
        trv.insert('', END, values=row)


def Search():
    ClearTrv()
    val = eSearch.get()
    cur.execute("SELECT * FROM persons WHERE name like %s",(val,))
    users = cur.fetchall()
    for row in users:
        trv.insert('', END, values=row)

def ClearEntry():
    eName.delete(0, END)
    eFamily.delete(0, END)
    eAddress.delete(0, END)
    ePersonId.delete(0, END)
    ePhoneNumber.delete(0, END)


def OnDoubleClick(self, event=None):
    ClearEntry()
    global selected
    selected = trv.focus()
    values = trv.item(selected, 'values')
    global id
    id = values[0]
    eName.insert(0, values[1])
    eFamily.insert(0, values[2])
    ePersonId.insert(0, values[3])
    eAddress.insert(0, values[4])
    ePhoneNumber.insert(0, values[5])


def UpdateUser():
    global selected
    if selected:
        confirmed = messagebox.askyesno("Confirm Update", "Are you sure you want to update this item?")
        if confirmed:
            name_value = eName.get()
            family_value = eFamily.get()
            personid_value = ePersonId.get()
            address_value = eAddress.get()
            phonenumbmer_value = ePhoneNumber.get()
            cur.execute("""UPDATE persons 
                          SET name = %s,
                              family = %s,
                              personid = %s,
                              address = %s,
                              phonenumber = %s
                          WHERE id = %s""",
                        (name_value, family_value, personid_value, address_value, phonenumbmer_value, id))

            con.commit()
    else:
        messagebox.showwarning("No Selection", "Please select an item to update.")


    RefreshTrv()
    ClearEntry()
    selected = False

btnUpdate = tkinter.Button(side1, text="Update", command=UpdateUser,width=10,bg='yellow')
btnUpdate.grid(row=8, column=2,padx=(0,0),pady=(20,0))

def DeleteUser():
    global selected
    if selected:
        confirmed = messagebox.askyesno("Confirm Update", "Are you sure you want to update this item?")
        if confirmed:
            selected_item = trv.selection()
            trv.delete(selected_item)
            cur.execute("""DELETE FROM persons 
                WHERE id = %s""", (id,))
            con.commit()
    else:
        messagebox.showwarning("No Selection", "Please select an item to update.")

    RefreshTrv()
    ClearEntry()
    selected = False

btnDelete = tkinter.Button(side1, text="Delete", command=DeleteUser,width=10,bg='red')
btnDelete.grid(row=8, column=3,padx=(0,60),pady=(20,0))

window.after_idle(Find)

lbName = tkinter.Label(side1, text="نام")
lbFamily = tkinter.Label(side1, text="نام خانوادگی")
lbPersonId = tkinter.Label(side1, text="کدملی")
lbAddress = tkinter.Label(side1, text="آدرس")
lbPhoneNumber = tkinter.Label(side1, text="تلفن")

lbName.grid(row=3, column=1,pady=(30,0))
lbFamily.grid(row=4, column=1,pady=(10,0))
lbPersonId.grid(row=5, column=1,pady=(10,0))
lbAddress.grid(row=6, column=1,pady=(10,0))
lbPhoneNumber.grid(row=7, column=1,pady=(10,0))

eName = tkinter.Entry(side1, width=30)
eFamily = tkinter.Entry(side1, width=30)
ePersonId = tkinter.Entry(side1, width=30)
eAddress = tkinter.Entry(side1, width=30)
ePhoneNumber = tkinter.Entry(side1, width=30)

eName.grid(row=3, column=2,pady=(50,0))
eFamily.grid(row=4, column=2,pady=(10,0))
ePersonId.grid(row=5, column=2,pady=(10,0))
eAddress.grid(row=6, column=2,pady=(10,0))
ePhoneNumber.grid(row=7, column=2,pady=(10,0))

btnAdd = tkinter.Button(side1, text="Add", command=Registration,width=10,bg='green')
btnAdd.grid(row=8, column=1,padx=(100,0),pady=(20,0))

lbSearch = tkinter.Label(side2, text="Search", font=12)
eSearch = tkinter.Entry(side2,width=50)
btnSearch = tkinter.Button(side2, text='search', bg='blue', fg='#ffffff', command=Search,width=9)

trv = ttk.Treeview(side2, columns=(1, 2, 3, 4, 5, 6), height=15, show="headings")
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
eSearch.grid(row=1, column=2,padx=10)
btnSearch.grid(row=1, column=3,padx=(0,200))

trv.grid(row=2, column=1, columnspan=3,pady=20)
trv.bind("<Double-1>", OnDoubleClick)
window.mainloop()
