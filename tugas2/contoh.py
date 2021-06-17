#import tkinter as tk
from tkinter import Tk, Frame

window = Tk()
window.geometry("800+600+500+500")

frame01 = Frame(window, background="pink", width=10, height=100)
frame01.grid(row=0, column=0, sticky="nsew")

frame02 = Frame(window, background="bisque", width=10, height=100)
frame02.grid(row=0, column=1, sticky="nsew")

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)



window.mainloop()