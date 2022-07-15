import tkinter as tk

test_window = tk.Tk()
info = ["name", "phone Number", "hello"]

for item in info:
    greetingl1 = tk.Label(
        test_window,
        text=f"{item}")

    greetingl1.pack()


test_window.mainloop()