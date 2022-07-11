from operator import sub
import sqlite3 as sl
#importing SQL tools for manipulating the database
import os.path
#importing os tools to check for files
import tkinter as tk

from pyparsing import col
#importing parts for the UI

#This declares and set up the initial login window
login_window = tk.Tk()
login_window.geometry("300x150")


# Database Initialization
#This section of code runs on startup and cheaks to make sure that the database that is used in this project does exsist.
#It returns the location of the database so other fuctions that use the data have access too it.
#------------------------------------------------------------------------------------------------------------------
def db_initialization():
    global con 
    db_check = os.path.exists('login.db') #Cheaks the local directory for the database. Returns true or false based on the finding
    #If database check finds a database it runs the following if statement
    if db_check == 1:
        print('db in place')
        con = sl.connect('login.db')

    #if database check does not find a database, the following code is run
    if db_check == 0:
        admin_level = 0
        con = sl.connect('login.db') # This line creates the actual database
        with con:
            #This section of code creates tables in the database
            con.execute("""
                        CREATE TABLE USER (
                            name TEXT NOT NULL PRIMARY KEY,
                            password TEXT,
                            level INTEGER
                            );
                        """)
            con.execute("""
                        CREATE TABLE PATIENT (
                            name TEXT NOT NULL PRIMARY KEY
                            );
                        """)
        #Once the database and tables have been made, the database creates a admin level account for the user
        con.execute(f"INSERT INTO USER VALUES ('admin','admin', {admin_level})")
        con.commit()
#------------------------------------------------------------------------------------------------------------------


#Database data reading and manipulation
#The following fuctions relate to manipulating, adding and deleting data within the database
#------------------------------------------------------------------------------------------------------------------
#This function is used to allow a user to create another user. It checks to see if said user exists and if not, creates the user.
def create_user(cr_name_var, cr_passw_var, cr_level_var):

    username = cr_name_var.get()
    password = cr_passw_var.get()
    level = cr_level_var.get()

    print(username + password + level)

    for row in con.execute(f'SELECT name FROM USER'):
        if username == row[0]:
            print('Username already exsits. Try again')
            return
            
    con.execute(f"INSERT INTO USER VALUES ('{username}','{password}', '{level}')")
    con.commit()


#This fuction needs to find if the user is in the database. If the user is not it needs to end or allow the user on more try
#This fuction should also return the access level of the user so the proper UI elements are displayed depending on the users access level
def get_login_info(name_var, passw_var, password_location):

    global user_info
    user_info = [ ]
    name = name_var.get()
    password = passw_var.get()

    for row in con.execute('SELECT * FROM USER'):
        if name == row[0]:
            if password == row[1]:
                user_info = row
                login_window.destroy()
                login_success_page()

            else:
                greetingl4 = tk.Label(
                    login_window,
                    text="Password Incorrct",
                    fg='red')
                
                greetingl4.grid(row = 5, column= 1)
                password_location.delete(0, tk.END)

#------------------------------------------------------------------------------------------------------------------

#Login
#This group of functions deal with the ability for the user to login
#------------------------------------------------------------------------------------------------------------------
#This is a test function only. It will later be overhauled into part of the UI
"""def initial_login(con):
    print('Welcome to EW Hospital')
    print('Please enter your Username to login')
    print('Unautherized access is illegal')
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')

    response = get_login_info(username, password, con)"""

def login_window_creation():
    #Variable storage
    name_var=tk.StringVar()
    passw_var=tk.StringVar()

#Text Lines
#------------------------------------------------------------------------------------------------------------------
    greetingl1 = tk.Label(
        login_window,
        text="Welcome to CH Solutions")
    greetingl2 = tk.Label(
        login_window,
        text="Please login below:")
    greetingl3 = tk.Label(
        login_window,
        text="Username: ")
    greetingl4 = tk.Label(
        login_window,
        text="Password: ")

#User Input
#------------------------------------------------------------------------------------------------------------------  
    entry_username = tk.Entry(login_window,
        textvariable = name_var)
    entry_password = tk.Entry(login_window,
        textvariable = passw_var, 
        show = '*')

#Clickable buttons
#------------------------------------------------------------------------------------------------------------------
    button = tk.Button(
        login_window,
        text="Login",
        command=lambda:[
            get_login_info(name_var, passw_var, entry_password)
            ],
        )

#Screen Creation
#------------------------------------------------------------------------------------------------------------------       
    greetingl1.grid(row = 0, column= 1)
    greetingl2.grid(row = 1, column= 1)
    greetingl3.grid(row = 2, column= 0)
    entry_username.grid(row = 2, column= 1)
    greetingl4.grid(row = 3, column= 0)
    entry_password.grid(row = 3, column= 1)
    button.grid(row = 4, column= 1)
    login_window.mainloop()

#This section deals with creating other windows outide of the main login page
#------------------------------------------------------------------------------------------------------------------
def login_success_page():
    login_success_window = tk.Tk()
    login_success_window.geometry("100x50")

    greetingl1 = tk.Label(
        login_success_window,
        text="Login Successful")
    greetingl1.pack()
    button = tk.Button(
        login_success_window,
        text="ok",
        command=lambda: [
            login_success_window.destroy(),
            main_menu_page()
            ],
        )
    greetingl1.pack()
    button.pack()
    login_success_window.mainloop()

def main_menu_page():
    menu_window = tk.Tk()
    menu_window.geometry("100x50")

    user_greeting = tk.Label(
        menu_window,
        text = (f"Welcome {user_info[0]}")
    )

    button = tk.Button(
        menu_window,
        text = "Create New User",
        command = lambda: [
            menu_window.destroy(),
            create_user_page()
        ])
    
    
    user_greeting.pack()
    if user_info[2] == 0:
        button.pack()
    menu_window.mainloop()

def create_user_page():
    create_user_window = tk.Tk()
    create_user_window.geometry("300x150")


    cr_name_var = tk.StringVar()
    cr_passw_var = tk.StringVar()
    cr_level_var = tk.StringVar()

    header_txt = tk.Label(
        create_user_window,
        text = "Welcome to User Creation")
    username_txt = tk.Label(
        create_user_window,
        text = "Username: ")
    password_txt = tk.Label(
        create_user_window,
        text = "Password: ")
    clearance_txt = tk.Label(
        create_user_window,
        text = "Clearance Level: " 
    )

    entry_username = tk.Entry(create_user_window,
        textvariable = cr_name_var)
    entry_password = tk.Entry(create_user_window,
        textvariable = cr_passw_var)
    entry_clearance = tk.Entry(create_user_window,
        textvariable = cr_level_var)

    cru_button = tk.Button(
        create_user_window,
        text="Create User",
        command=lambda:[
            create_user(cr_name_var, cr_passw_var, cr_level_var)
            ]
        )   
    ext_button = tk.Button(
        create_user_window,
        text="Exit",
        command=lambda:[
            create_user_window.destroy(),
            main_menu_page()
            ],
        )
    clearenceinfo_button = tk.Button(
        create_user_window,
        text="Info",
        command=lambda:[
            clearance_info()
            ],
        )

    header_txt.grid(row = 0, column = 1)
    username_txt.grid(row = 1, column = 0)
    entry_username.grid(row = 1, column = 1)
    password_txt.grid(row = 2, column = 0)
    entry_password.grid(row = 2, column = 1)
    clearance_txt.grid(row = 3, column = 0)
    entry_clearance.grid(row = 3, column = 1)
    cru_button.grid(row=4, column=1)
    ext_button.grid(row=4, column=0)
    clearenceinfo_button.grid(row = 3, column = 3)


def clearance_info():
    clearance_info_window = tk.Tk()
    clearance_info_window.geometry("450x150")

    header_txt = tk.Label(
        clearance_info_window,
        text = "User Clearance info:")
    sub_header_txt = tk.Label(
        clearance_info_window,
        text = "Each user is assinged a clearence, giving them access to specific windows")

    ext_button = tk.Button(
        clearance_info_window,
        text="Close",
        command=lambda:[
            clearance_info_window.destroy()
            ],
        )
    header_txt.pack()
    sub_header_txt.pack()
    ext_button.pack()
    

#------------------------------------------------------------------------------------------------------------------

#Program start function
#------------------------------------------------------------------------------------------------------------------
def main():
    db_initialization()
    login_window_creation()
#------------------------------------------------------------------------------------------------------------------

#Running of the program
#------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
        main()
#------------------------------------------------------------------------------------------------------------------