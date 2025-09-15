import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class DatabaseWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Akebono_Pass 0.1")

        self.window.resizable(False, False)

        label5 = tk.Label(self.window, text="Directory with orbit files:")
        label6 = tk.Label(self.window, text="Directory with data files:")

        separator = ttk.Separator(self.window, orient=tk.HORIZONTAL)

        self.orbit_directory_entry = tk.Entry(self.window)
        self.datafile_directory_entry = tk.Entry(self.window)

        ok_button = tk.Button(self.window, text="Create database", command=self.on_button_press)
        choose_orbit_directory_button = tk.Button(
            self.window, text="Choose", command=self.choose_orbit_directory_button_press
        )
        choose_datafile_directory_button = tk.Button(
            self.window,
            text="Choose",
            command=self.choose_datafile_directory_button_press,
        )

        label5.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.orbit_directory_entry.grid(
            row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E
        )
        choose_orbit_directory_button.grid(row=0, column=4, padx=5, pady=10)

        label6.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.datafile_directory_entry.grid(
            row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E
        )
        choose_datafile_directory_button.grid(row=1, column=4, padx=5, pady=10)

        separator.grid(row=2, column=0, columnspan=5, pady=10, sticky=tk.W + tk.E)

        ok_button.grid(row=3, column=3, pady=5)

    def on_button_press(self):
        pass

    def choose_orbit_directory_button_press(self):
        directory_path = filedialog.askdirectory()
        self.orbit_directory_entry.delete(0, tk.END)
        self.orbit_directory_entry.insert(0, directory_path)

    def choose_datafile_directory_button_press(self):
        directory_path = filedialog.askdirectory()
        self.datafile_directory_entry.delete(0, tk.END)
        self.datafile_directory_entry.insert(0, directory_path)

    def run(self):
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)
