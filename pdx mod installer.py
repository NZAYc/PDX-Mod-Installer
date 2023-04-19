import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from zipfile import ZipFile


class ModInstaller(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Paradox Game Mod Installer")
        self.directory = os.environ["USERPROFILE"] + \
            "\\Documents\\Paradox Interactive\\"    # Doesn't work, too bad!
        self.master.geometry("770x500")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Creating mod directory browse button
        self.mod_dir_button = ttk.Button(
            self, text="Select Mod Installation Directory", command=self.browse_directory)
        self.mod_dir_button.pack(side="top", padx=10, pady=10)

        # Creating selected archive label
        self.selected_directory = ttk.Label(self, text="")
        self.selected_directory.pack(side="top", padx=5, pady=5)

        # Creating zip archive browse button
        self.zip_file_button = ttk.Button(
            self, text="Select Mod Archives", command=self.browse_zip_archive)
        self.zip_file_button.pack(side="top", padx=10, pady=10)

        # Creating selected archive label
        self.selected_archive_label = ttk.Label(self, text="")
        self.selected_archive_label.pack(side="top")

        # Creating clear button
        self.clear_button = ttk.Button(
            self, text="Clear List", command=self.clear_files)
        self.clear_button.pack(side="bottom", padx=10, pady=10)

        # Creating extract button
        self.extract_button = ttk.Button(
            self, text="Extract and Install", command=self.extract_files)
        self.extract_button.pack(side="top", padx=10, pady=10)

        # Creating progress bar
        self.status_label = ttk.Label(self, text="Waiting for user input...")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=10)

        # Initializing drop box frame
        self.drop_box_frame = ttk.Frame(self)
        self.drop_box_frame.pack(side="top", fill="both",
                                 expand=True, padx=10, pady=10)

        # Initializing drop box
        self.drop_box = ttk.Treeview(
            self.drop_box_frame, height=5)
        self.drop_box.pack(side="left", fill="both", expand=True)

        # Add scrollbar to drop box frame
        self.drop_box_scrollbar = ttk.Scrollbar(
            self.drop_box_frame, orient="vertical", command=self.drop_box.yview)
        self.drop_box_scrollbar.pack(side="right", fill="y")
        self.drop_box.configure(yscrollcommand=self.drop_box_scrollbar.set)

    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        self.selected_directory.config(text=self.directory)
        # reset status label to default
        self.status_label.config(text="Waiting for user input...")

    def browse_zip_archive(self):
        zip_file_path = filedialog.askopenfilename(
            filetypes=[("Zip Archive", "*.zip")])
        if zip_file_path:
            self.selected_archive_label.config(text="")
            self.drop_box.insert("", "end", text=os.path.basename(
                zip_file_path), values=(zip_file_path,))
            # reset status label to default
            self.status_label.config(text="Waiting for user input...")

    def clear_files(self):
        self.drop_box.delete(*self.drop_box.get_children())
        self.selected_archive_label.config(text="")
        # reset status label to default
        self.status_label.config(text="Waiting for user input...")

    def extract_files(self):
        self.status_label.config(text="Installing...")
        directory = self.directory
        if not directory:
            tk.messagebox.showerror("Error", "Please select a mod directory!")
            return

        if not self.drop_box.get_children():
            tk.messagebox.showerror(
                "Error", "Please select one or more zip archives!")
            return

        # Disabling extract button to prevent multiple extractions
        self.extract_button.config(state="disabled")

        # Iterating over files in drop box
        for item in self.drop_box.get_children():
            file_path = self.drop_box.item(item, "values")[0]
            try:
                print(f"Extracting {file_path}...")
                # Opening zip file
                with ZipFile(file_path, "r") as zip_file:
                    # Extracting contents to directory
                    zip_folder = zip_file.namelist()[0]
                    extract_dir = directory
                    zip_file.extractall(extract_dir)

                    # Modifying mod file path
                    mod_files = [f for f in os.listdir(
                        extract_dir) if f.endswith('.mod')]
                    for mod_file in mod_files:
                        mod_file_path = os.path.join(extract_dir, mod_file)
                        with open(mod_file_path, "r") as mod_file:
                            mod_file_contents = mod_file.read()
                        if "path=" not in mod_file_contents:
                            # If path line is missing, add a new one with appropriate path
                            mod_file_contents += f"\npath=\"{extract_dir}/{zip_folder}\""
                            with open(mod_file_path, "w") as mod_file:
                                mod_file.write(mod_file_contents)

                print(f"{file_path} extracted successfully!")
                self.status_label.config(text="Installation complete!")
            except Exception as e:
                print(f"Failed to extract {file_path}.")
                # setting the status label to installation failed
                self.status_label.config(
                    text="Installation failed, error has occured!")
                break

        # Re-enable extract button
        self.extract_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModInstaller(master=root)
    app.mainloop()
