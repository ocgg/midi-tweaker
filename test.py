
import tkinter as tk

# Création de la fenêtre principale
root = tk.Tk()

# Création de la barre de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Création de la barre "IN"
in_bar = tk.Frame(root, height=50, bg='lightblue')
in_bar.pack(fill='x')

# Création de la fenêtre principale
main_window = tk.Frame(root)
main_window.pack(fill='both', expand=True)

# Création de la barre "OUT"
out_bar = tk.Frame(root, bg='lightblue')
out_bar.pack(fill='x')

# Exemple d'ajout d'éléments à la barre "IN"
in_label = tk.Label(in_bar, text="Barre IN", bg='lightblue')
in_label.pack()

# Exemple d'ajout d'éléments à la fenêtre principale
main_label = tk.Label(main_window, text="Fenêtre principale", bg='lightgrey')
main_label.pack(fill='both', expand=True)

# Exemple d'ajout d'éléments à la barre "OUT"
out_label = tk.Label(out_bar, text="Barre OUT", bg='lightblue')
out_label.pack()

root.mainloop()
