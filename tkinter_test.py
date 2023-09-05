import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Import ttk for themed widgets
from new_main import main

def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")], title="Select Files and Directories")
    for path in file_paths:
        file_listbox.insert(tk.END, path)

def browse_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(tk.END, output_dir)

def anonymize_documents():
    # Add your anonymization logic here
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)

    anonymization_count, files = main(file_listbox.get(0, tk.END), output_dir_entry.get())
    print(anonymization_count)
    results_text.insert(tk.END, ("{} files processed".format(files)))
    results_text.insert(tk.END, "\n\n")
    results_text.insert(tk.END, "Entities removed:\n")
    for key, value in anonymization_count.items():
        results_text.insert(tk.END, ("{}: {}".format(key, value)))
        results_text.insert(tk.END, "\n")
    results_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("Anonymizer Tool")

    # Create and configure widgets
    file_label = tk.Label(window, text="Selected Files/Directories:")
    file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    file_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, height=10, width=50, borderwidth=1, relief=tk.SOLID)
    file_listbox.grid(row=1, column=0, padx=10, pady=10)

    select_file_button = tk.Button(window, text="Select File(s)/Dir(s)", command=browse_files)
    select_file_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    output_dir_label = tk.Label(window, text="Selected Output Directory:")
    output_dir_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    output_dir_entry = tk.Entry(window, width=50, borderwidth=1, relief=tk.SOLID)
    output_dir_entry.grid(row=3, column=0, padx=10, pady=10)

    select_output_button = tk.Button(window, text="Select Output Directory", command=browse_output_dir)
    select_output_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Anonymize Documents button
    anonymize_button = tk.Button(window, text="Anonymize Documents", command=anonymize_documents)
    anonymize_button.grid(row=4, column=0, columnspan=3, pady=20)

    # Progress bar
    # progress_var = tk.IntVar()
    # progress_bar = ttk.Progressbar(window, mode='determinate', variable=progress_var)
    # progress_bar.grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

    # Results text area
    results_label = tk.Label(window, text="Results:")
    results_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    results_text = tk.Text(window, height=10, width=50, state=tk.DISABLED, borderwidth=1, relief=tk.SOLID)
    results_text.grid(row=7, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    # Configure row and column weights to make the listbox and results text area expandable
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Start the main loop
    window.mainloop()
