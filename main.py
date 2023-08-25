import requests
import zipfile
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from automation_script import process_csv_to_webclient

#Github url that will send out new update to apps as new features are added also checks for updates

GITHUB_REPO ="https://api.github.com/repos/parlo12/3cx_automation/releases/latest"

def check_for_updates(current_version):
    url = f"https://api.github.com/repos/parlo12/{3cx_automation}/releases/latest"
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to fetch updates. HTTP Status Code: {response.status_code}")
        return False, current_version
    
    data = response.json()
    
    # Check if tag_name exists in the response
    if 'tag_name' not in data:
        print("The response from GitHub does not contain a 'tag_name' key.")
        return False, current_version

    latest_version = data['tag_name']
    download_url = data['html_url']  # Link to the release page

    if current_version < latest_version:
        return True, download_url
    else:
        return False, download_url


def update_aplication(download_url):
    # Download the Zip

    r = requests.get(download_url, stream=True)
    zip_path = "new_app.zip"
    with open(zip_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

        # Extract the zip to the app's directory 

        with zipfile.ZipFile(zip_path,'r') as zip_ref:
            zip_ref.extractall("path_to_app_folder")
        os.remove(zip_path)


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV to 3CX Automation")
        
        self.stop_event = None

        # File Upload
        self.label = ttk.Label(self.master, text="Upload CSV:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.filename_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.master, textvariable=self.filename_var, width=40)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = ttk.Button(self.master, text="Browse", command=self.load_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Username and Password Inputs
        self.label2 = ttk.Label(self.master, text="Username:")
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.master, textvariable=self.username_var, width=20)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.label3 = ttk.Label(self.master, text="Password:")
        self.label3.grid(row=2, column=0, padx=10, pady=10)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.master, textvariable=self.password_var, width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Phone Column Name
        self.label4 = ttk.Label(self.master, text="Phone Column Name:")
        self.label4.grid(row=3, column=0, padx=10, pady=10)

        self.column_name_var = tk.StringVar()
        self.column_name_entry = ttk.Entry(self.master, textvariable=self.column_name_var, width=20)
        self.column_name_entry.grid(row=3, column=1, padx=10, pady=10)

        # Web Client URL
        self.label5 = ttk.Label(self.master, text="URL:")
        self.label5.grid(row=4, column=0, padx=10, pady=10)

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.master, textvariable=self.url_var, width=40)
        self.url_entry.grid(row=4, column=1, padx=10, pady=10)

        # Start and Stop buttons
        self.start_button = ttk.Button(self.master, text="Start", command=self.start_script)
        self.start_button.grid(row=5, column=1, pady=20)

        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=2, pady=20)

        self.update_button = ttk.Button(self.master, text="Check for Updates", command=self.on_check_updates)
        self.update_button.grid(row=6, column=1, pady=20)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        self.filename_var.set(filepath)

    def start_script(self):
        self.script_thread = threading.Thread(target=self.run_script)
        self.script_thread.start()
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL

    def stop_script(self):
        if self.stop_event:
            self.stop_event.set()
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED

    #checking for updates available for the app

    def on_check_updates(self):
        with open("version.txt", "r") as file:
            current_version =file.readline().strip()

        lastest_version, download_url = check_for_updates(current_version)
        if download_url:
            response = messagebox.askyesno("Update Available", f"Version{lastest_version} is available. DO you want to update?")
            if response:
                update_aplication(download_url)
                messagebox.showinfo("Update completed", "Please restart the application.")
        else:
            messagebox.showinfo("No Updates", "You are using the latest version.")
        
    def run_script(self):
        self.stop_event = threading.Event()
        csv_path = self.filename_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        column_name = self.column_name_var.get()
        url = self.url_var.get()
        
        process_csv_to_webclient(csv_path, username, password, column_name, url, self.stop_event)

if __name__ == "__main__":
    root = tk.Tk()
app = Application(root)
root.mainloop()

