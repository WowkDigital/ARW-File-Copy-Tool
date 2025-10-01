import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
import re

# Set application appearance
ctk.set_appearance_mode("System")  # Light/dark mode based on Windows settings
ctk.set_default_color_theme("blue")

def parse_list_and_copy_files(source_dir, list_content, destination_dir):
    """
    Parses the list content, identifies matching ARW files, and copies them to the destination folder.
    """
    if not source_dir or not list_content.strip():
        messagebox.showerror("Validation Error", "Select the source folder and paste the file list.")
        return

    try:
        # Create the destination folder 'selected' (or other, if the path was changed)
        os.makedirs(destination_dir, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Folder Creation Error", f"Failed to create the destination folder: {e}")
        return
    
    patterns_to_find = set()
    copied_count = 0

    # Process the pasted content
    for line in list_content.splitlines():
        line = line.strip()
        if not line:
            continue
            
        # Look for the pattern 'n_X.enc'
        match = re.search(r'n_(\d+)\.enc', line)
        if match:
            number = match.group(1)
            patterns_to_find.add(f'n_{number}.ARW')

    if not patterns_to_find:
        messagebox.showwarning("List Error", "No valid patterns (e.g., n_X.enc) found in the pasted list.")
        return

    # List of ARW files in the source folder
    source_files = {f for f in os.listdir(source_dir) if f.lower().endswith('.arw')}

    # Set of files to be copied
    files_to_copy = patterns_to_find.intersection(source_files)
    
    if not files_to_copy:
        messagebox.showwarning("No Matching Files", "None of the files from the list were found in the source folder.")
        return

    # Copying files
    for arw_filename in files_to_copy:
        source_path = os.path.join(source_dir, arw_filename)
        destination_path = os.path.join(destination_dir, arw_filename)
        
        try:
            shutil.copy2(source_path, destination_path)
            copied_count += 1
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy file {arw_filename}: {e}")
            return

    # Check which files were on the list but not found
    missing_files_final = patterns_to_find.difference(files_to_copy)

    # Feedback message
    result_message = f"Successfully finished! Copied {copied_count} files to folder:\n{destination_dir}"
    if missing_files_final:
        result_message += f"\n\nNot found in the source folder (missing): \n{', '.join(missing_files_final)}"
        messagebox.showwarning("Finished with Warning ⚠️", result_message)
    else:
        messagebox.showinfo("Copying Complete ✅", result_message)


# ----------------------------------------------------------------------------------------------------------------------

class ModernFileCopyApp(ctk.CTk):
    """Main application class with a modern GUI."""
    def __init__(self):
        super().__init__()

        self.title("ARW File Copy — Default Folder 'selected'")
        self.geometry("700x520")
        self.resizable(False, False)

        # Path variables
        self.source_dir = ctk.StringVar()
        self.destination_dir = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        
        # --- 1. Source Folder Frame ---
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(self.source_frame, text="1. Source Folder (ARW files):", font=ctk.CTkFont(size=13, weight="bold")).pack(padx=10, pady=(10, 5), anchor="w")
        
        self.source_entry = ctk.CTkEntry(self.source_frame, textvariable=self.source_dir, width=450, placeholder_text="Path to the folder with n_X.ARW files", state='readonly')
        self.source_entry.pack(side="left", padx=(10, 5), pady=10, fill="x", expand=True)
        
        ctk.CTkButton(self.source_frame, text="Select Folder...", command=self.select_source_dir).pack(side="right", padx=(5, 10), pady=10)


        # --- 2. Paste List Frame ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.list_frame, text="2. Paste File List (.enc):", font=ctk.CTkFont(size=13, weight="bold")).pack(padx=10, pady=(10, 5), anchor="w")
        
        self.list_text = ctk.CTkTextbox(self.list_frame, height=150, activate_scrollbars=True, wrap="word")
        self.list_text.pack(padx=10, pady=(0, 10), fill="x", expand=True)
        self.list_text.insert("0.0", "Paste the list here, e.g.:\n0004_n_3.enc\n0009_n_8.enc\n...")
        self.list_text.bind("<FocusIn>", self.clear_placeholder)
        self.list_text.bind("<FocusOut>", self.set_placeholder)


        # --- 3. Destination Folder (Automatic) Frame ---
        self.dest_frame = ctk.CTkFrame(self)
        self.dest_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.dest_frame, text="3. Destination Folder (Automatic):", font=ctk.CTkFont(size=13, weight="bold")).pack(padx=10, pady=(10, 5), anchor="w")
        
        self.dest_entry = ctk.CTkEntry(self.dest_frame, textvariable=self.destination_dir, width=450, 
                                        placeholder_text="Will be: [Source Folder]/selected", 
                                        state='readonly', 
                                        text_color="#10803c", 
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.dest_entry.pack(side="left", padx=(10, 5), pady=10, fill="x", expand=True)
        
        # Start button
        self.start_button = ctk.CTkButton(self, text="▶ START COPYING", command=self.start_copying, 
                                          fg_color="#10803c", hover_color="#0e6b33", 
                                          font=ctk.CTkFont(size=16, weight="bold"), height=50)
        self.start_button.pack(fill="x", padx=20, pady=(15, 20))


    # --- Placeholder handler methods ---
    def clear_placeholder(self, event):
        if self.list_text.get("1.0", "end-1c").startswith("Paste the list here, e.g.:"):
            self.list_text.delete("1.0", "end")

    def set_placeholder(self, event):
        if not self.list_text.get("1.0", "end-1c").strip():
             self.list_text.insert("0.0", "Paste the list here, e.g.:\n0004_n_3.enc\n0009_n_8.enc\n...")

    # --- Dialog handler methods ---

    def select_source_dir(self):
        directory = filedialog.askdirectory(title="Select folder with ARW files")
        if directory:
            self.source_dir.set(directory)
            # Automatically set the destination folder to [source_dir]/selected
            self.destination_dir.set(os.path.join(directory, "selected"))

    # --- Operation startup method ---

    def start_copying(self):
        source = self.source_dir.get()
        destination = self.destination_dir.get()
        list_content = self.list_text.get("1.0", "end-1c")
        
        # Remove placeholder if it is pasted
        if list_content.startswith("Paste the list here, e.g.:"):
             list_content = ""

        parse_list_and_copy_files(source, list_content, destination)

# --- Application launch ---
if __name__ == "__main__":
    app = ModernFileCopyApp()
    app.mainloop()
