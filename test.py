import tkinter as tk
from tkinter import ttk
root = tk.Tk()
ttk.Style().theme_use('alt')  # Setting a theme for TTK widgets
btn_standard = tk.Button(root, text='Standard Button')
btn_standard.pack()
btn_ttk = ttk.Button(root, text='TTK Button')
btn_ttk.pack()
root.mainloop()
