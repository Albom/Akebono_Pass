import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import os
import datetime as dt
from processing import Parameters, Search
from database_window import DatabaseWindow


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Akebono_Pass 0.1")

        icon_image = tk.PhotoImage(
            file=os.path.join(os.path.dirname(__file__), "images/icon.png")
        )
        self.window.iconphoto(True, icon_image)

        self.window.resizable(False, False)

        label1 = tk.Label(self.window, text="L:")
        label2 = tk.Label(self.window, text="ΔL:")
        label3 = tk.Label(self.window, text="Lon:")
        label4 = tk.Label(self.window, text="ΔLon:")
        label7 = tk.Label(self.window, text="Output file:")
        label8 = tk.Label(self.window, text="Start date:")
        label9 = tk.Label(self.window, text="End date:")

        separator = ttk.Separator(self.window, orient=tk.HORIZONTAL)

        self.shell_entry = tk.Entry(self.window)
        self.shell_delta_entry = tk.Entry(self.window)
        self.longitude_entry = tk.Entry(self.window)
        self.longitude_delta_entry = tk.Entry(self.window)
        self.output_filename_entry = tk.Entry(self.window)

        ok_button = tk.Button(self.window, text="Submit", command=self.on_button_press)
        choose_output_filename_button = tk.Button(
            self.window, text="Choose", command=self.choose_output_filename_button_press
        )

        self.start_date = DateEntry(
            self.window, selectmode="day", date_pattern="yyyy-mm-dd"
        )
        self.end_date = DateEntry(
            self.window, selectmode="day", date_pattern="yyyy-mm-dd"
        )

        label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.shell_entry.grid(row=0, column=1, padx=5, pady=5)

        label2.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.shell_delta_entry.grid(row=0, column=3, padx=5, pady=5)

        label3.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.longitude_entry.grid(row=1, column=1, padx=5, pady=5)
        label4.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.longitude_delta_entry.grid(row=1, column=3, padx=5, pady=5)

        label7.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.output_filename_entry.grid(
            row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E
        )
        choose_output_filename_button.grid(row=2, column=4, padx=5, pady=10)

        label8.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.start_date.grid(row=3, column=1, padx=5, pady=5)

        label9.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.end_date.grid(row=3, column=3, padx=5, pady=5)

        separator.grid(row=4, column=0, columnspan=5, pady=10, sticky=tk.W + tk.E)

        ok_button.grid(row=5, column=3, pady=5)

    def on_button_press(self):
        try:
            start_date = dt.date.fromisoformat(self.start_date.get())
            end_date = dt.date.fromisoformat(self.end_date.get())
            shell = float(self.shell_entry.get().strip())
            shell_delta = float(self.shell_delta_entry.get().strip())
            longitude = float(self.longitude_entry.get().strip())
            longitude_delta = float(self.longitude_delta_entry.get().strip())
        except ValueError:
            return

        output_filename = self.output_filename_entry.get()

        parameters = Parameters(
            start_date=start_date,
            end_date=end_date,
            shell=shell,
            shell_delta=shell_delta,
            longitude=longitude,
            longitude_delta=longitude_delta,
            output_filename=output_filename,
        )
        search = Search(parameters)
        search.run()

    # def choose_orbit_directory_button_press(self):
    #     database_window = DatabaseWindow(self.window)
    #     database_window.run()


        # directory_path = filedialog.askdirectory()
        # self.orbit_directory_entry.delete(0, tk.END)
        # self.orbit_directory_entry.insert(0, directory_path)

    def choose_output_filename_button_press(self):

        database_window = DatabaseWindow(self.window)
        database_window.run()

        # filename = filedialog.asksaveasfilename(defaultextension=".txt")
        # self.output_filename_entry.delete(0, tk.END)
        # self.output_filename_entry.insert(0, filename)

    def run(self):
        self.window.mainloop()
