import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import schedule
import time

class BackupApp:
    def __init__(self, master):
        self.master = master
        master.title("Mozamen")

        self.source_label = tk.Label(master, text="Select Source Directory:")
        self.source_label.pack()

        self.source_entry = tk.Entry(master, width=50)
        self.source_entry.pack()

        self.source_button = tk.Button(master, text="Browse", command=self.browse_source)
        self.source_button.pack()

        self.destination_label = tk.Label(master, text="Select Destination Directory:")
        self.destination_label.pack()

        self.destination_entry = tk.Entry(master, width=50)
        self.destination_entry.pack()

        self.destination_button = tk.Button(master, text="Browse", command=self.browse_destination)
        self.destination_button.pack()

        self.backup_button = tk.Button(master, text="Backup Now", command=self.backup_files)
        self.backup_button.pack()

        self.schedule_label = tk.Label(master, text="Set Backup Schedule (HH:MM):")
        self.schedule_label.pack()

        self.schedule_entry = tk.Entry(master, width=20)
        self.schedule_entry.pack()

        self.schedule_button = tk.Button(master, text="Set Schedule", command=self.set_schedule)
        self.schedule_button.pack()

        self.stop_schedule_button = tk.Button(master, text="Stop Schedule", command=self.stop_schedule)
        self.stop_schedule_button.pack()

    def browse_source(self):
        source_directory = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, source_directory)

    def browse_destination(self):
        destination_directory = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, destination_directory)

    def backup_files(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()

        if not os.path.exists(source):
            messagebox.showerror("Error", "Source directory does not exist.")
            return
        if not os.path.exists(destination):
            os.makedirs(destination)

        try:
            shutil.copytree(source, os.path.join(destination, os.path.basename(source)))
            messagebox.showinfo("Success", "Backup completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def set_schedule(self):
        schedule_time = self.schedule_entry.get()
        try:
            schedule.clear()
            schedule.every().day.at(schedule_time).do(self.backup_files)
            messagebox.showinfo("Schedule Set", f"Backup scheduled daily at {schedule_time}.")
            self.schedule_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid schedule format: {str(e)}")

    def stop_schedule(self):
        schedule.clear()
        messagebox.showinfo("Schedule Stopped", "Backup schedule stopped successfully.")

def main():
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
