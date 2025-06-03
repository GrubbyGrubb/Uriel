import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import os

class UrielGUI:
    def __init__(self, master, scraper_names, on_start):
        self.master = master
        self.master.title("Uriel V6 – Scraper Control Center")
        self.master.geometry("850x650")
        self.on_start = on_start

        # Input File
        self.input_label = ttk.Label(master, text="Select Input File:")
        self.input_label.pack(pady=(10, 0))
        self.input_entry = ttk.Entry(master, width=90)
        self.input_entry.pack()
        self.input_button = ttk.Button(master, text="Browse", command=self.browse_input)
        self.input_button.pack(pady=(0, 10))

        # Output File
        self.output_label = ttk.Label(master, text="Select Output File:")
        self.output_label.pack()
        self.output_entry = ttk.Entry(master, width=90)
        self.output_entry.pack()
        self.output_button = ttk.Button(master, text="Browse", command=self.browse_output)
        self.output_button.pack(pady=(0, 10))

        # Shotgun Mode
        self.shotgun_var = tk.BooleanVar()
        self.shotgun_checkbox = ttk.Checkbutton(master, text="💥 Shotgun Mode (Run all scrapers)", variable=self.shotgun_var, command=self.toggle_shotgun_mode)
        self.shotgun_checkbox.pack(pady=(10, 5))

        # Scraper Checkboxes
        self.scraper_vars = {}
        self.scraper_frame = ttk.LabelFrame(master, text="Select Active Scrapers")
        self.scraper_frame.pack(fill="x", padx=10, pady=5)

        for name in scraper_names:
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(self.scraper_frame, text=name.capitalize(), variable=var)
            chk.pack(side="left", padx=5, pady=5)
            self.scraper_vars[name] = var

        # Start Button
        self.start_button = ttk.Button(master, text="Start Scraping", command=self.start_scraping)
        self.start_button.pack(pady=(10, 5))

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)

        # Log Terminal
        self.log_output = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=18)
        self.log_output.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_shotgun_mode(self):
        state = "disabled" if self.shotgun_var.get() else "normal"
        for chk in self.scraper_frame.winfo_children():
            chk.configure(state=state)

    def browse_input(self):
        filetypes = [("Excel files", "*.xlsx *.csv")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def start_scraping(self):
        if self.shotgun_var.get():
            selected_scrapers = list(self.scraper_vars.keys())
        else:
            selected_scrapers = [name for name, var in self.scraper_vars.items() if var.get()]

        input_path = self.input_entry.get()
        output_path = self.output_entry.get()

        if not selected_scrapers:
            self.log("⚠️ No scrapers selected. Enable Shotgun Mode or select at least one.")
            return

        self.on_start(input_path, output_path, selected_scrapers)

    def log(self, message):
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)

    def update_progress(self, percent):
        self.progress["value"] = percent
        self.master.update_idletasks()
