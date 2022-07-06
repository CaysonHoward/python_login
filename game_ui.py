import tkinter as tk


window = tk.Tk()
window.geometry("200x200")

def print_usernames(name_var, passw_var):
    name=name_var.get()
    password=passw_var.get()

    print('hello')
    print(f"lol{name}{password}")
    window.destroy()

def window2():
    #This is an important
    name_var=tk.StringVar()
    passw_var=tk.StringVar()

    greetingl1 = tk.Label(
        window,
        text="Welcome to CH Solutions login")
    greetingl2 = tk.Label(
        window,
        text="Please login below:")
    entry_username = tk.Entry(window,textvariable=name_var)
    entry_password = tk.Entry(window,textvariable=passw_var)
    button = tk.Button(
        window,
        text="Click me!",
        command=lambda:[print_usernames(name_var, passw_var)],
        )
        
    greetingl1.grid(row = 0, column= 0)
    greetingl2.grid(row = 1, column= 0)
    entry_username.grid(row = 2, column= 0)
    entry_password.grid(row = 3, column= 0)
    button.grid(row = 4, column= 0)
    window.mainloop()

window2()
