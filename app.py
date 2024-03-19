import rtmidi
import tkinter as tk


class TkWindow(tk.Tk): # inherits from tk.Tk
    def __init__(self, midi_ports):
        # Call parent class constructor to have its behavior & state under self
        tk.Tk.__init__(self)
        # super().__init__()
        self.midi_ports = midi_ports
        self.geometry("640x480")
        self.title("MIDI Tweaker")
        self.make_menu()
        self.make_widgets()

    def make_menu(self):
        menubar = tk.Menu(self)
    
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Reset")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.configure(menu=menubar)

    def make_widgets(self):
        # Create option menu with MIDI ports
        self.var = tk.StringVar(self)
        self.var.set('Choose a MIDI port')
        self.portsMenu = tk.OptionMenu(self, self.var, *self.midi_ports)

        self.label = tk.Label(self, text="Choose a MIDI port:")
        # self.button = tk.Button(self, text="Quitter", command=self.quit)

        # Lb1 = tk.Listbox(self)
        # Lb1.insert(1, "Python")
        # Lb1.insert(2, "Perl")
        # Lb1.insert(3, "C")
        # Lb1.insert(4, "PHP")
        # Lb1.insert(5, "JSP")
        # Lb1.insert(6, "Ruby")

        # Lb1.pack()

        self.label.pack()
        # self.button.pack()
        self.portsMenu.pack()


if __name__ == "__main__":
    midi = rtmidi.MidiIn()
    midi_ports = midi.get_ports()
    window = TkWindow(midi_ports)
    window.mainloop()