import tkinter as tk
from tkinter import filedialog, ttk
from main import main
from main import stop_words as default_stop_words
from tktooltip import ToolTip


class ListboxEditable(tk.Frame):

    def __init__(self, root: tk.Tk, selectmode=tk.MULTIPLE, height=5, width=20, borderwidth=1, relief=tk.SOLID):
        super().__init__(root)

        self.root = root

        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.E1 = tk.Entry(self)
        self.text_color = self.E1.cget("fg")
        self.E1.config(fg='grey')
        self.E1.insert(0, "Type here...")
        self.E1.pack()

        self.list = []

        self.v = tk.StringVar(value=self.list)
        self.b1 = tk.Listbox(self, activestyle='dotbox', yscrollcommand=self.sb.set, listvariable=self.v,
                             selectmode=selectmode, height=height, width=width, borderwidth=borderwidth, relief=relief)

        self.sb.config(command=self.b1.yview)
        self.b1.pack()

        self.b1.bind('<Delete>', self.remove_item)
        self.E1.bind('<Return>', self.set_item)
        self.E1.bind('<FocusIn>', self.handle_focus_in)
        self.E1.bind('<FocusOut>', self.handle_focus_out)

    def set_entry_text(self, text):
        self.E1.delete(0, tk.END)
        self.E1.insert(0, text)
        self.root.focus()

    def set_item(self, event):
        text = self.E1.get()
        if not text:
            return
        self.E1.delete(0, tk.END)
        self.list.append(text)

        self.v.set(self.list)
        self.root.focus()

    def remove_item(self, event):
        try:
            index = self.b1.curselection()[0]
            self.list.pop(index)
            self.v.set(self.list)
            self.root.focus()
        except IndexError:
            pass

    def add_list(self, l):
        self.list.extend(l)
        self.v.set(self.list)

    def handle_focus_in(self, _):
        if self.E1.cget("fg") == self.text_color:
            return
        self.E1.delete(0, tk.END)
        self.E1.config(fg=self.text_color)

    def handle_focus_out(self, _):
        if (self.E1.get()):
            return
        self.E1.delete(0, tk.END)
        self.E1.config(fg='grey')
        self.E1.insert(0, "Type here...")


def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")], title="Select Files and Directories")
    for path in file_paths:
        file_listbox.insert(tk.END, path)


def remove_selected_files():
    selected_indices = file_listbox.curselection()
    for index in selected_indices[::-1]:
        file_listbox.delete(index)


def browse_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(tk.END, output_dir)


def anonymize_documents():
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)
    try:

        anonymization_count, files = main(file_listbox.get(0, tk.END),
                                          output_dir_entry.get(),
                                          force_anonymize_columns=force_anonymize_columns_listbox.list,
                                          force_anonymize_tokens=force_anonymize_tokens_listbox.list,
                                          stop_words=stop_words_listbox.list)
        print(anonymization_count)
        results_text.insert(tk.END, ("{} files processed".format(files)))
        results_text.insert(tk.END, "\n\n")
        results_text.insert(tk.END, "Entities removed:\n")
        for key, value in anonymization_count.items():
            results_text.insert(tk.END, ("{}: {}".format(key, value)))
            results_text.insert(tk.END, "\n")
    except Exception as e:
        results_text.insert(tk.END, f"Error: {e}")

    results_text.config(state=tk.DISABLED)


def toggle_advanced_options():
    if advanced_options_button["text"] == "Show Advanced Options":
        advanced_options_button["text"] = "Hide Advanced Options"
        advanced_options_frame.grid(row=6, columnspan=2)
        advanced_options_frame.grid(row=6, columnspan=2)

    else:
        advanced_options_button["text"] = "Show Advanced Options"
        advanced_options_frame.grid_forget()


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("Anonymizer Tool")

    # Create and configure widgets
    file_label = tk.Label(window, text="Selected Files/Directories:")
    file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    file_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, height=10, width=50, borderwidth=1, relief=tk.SOLID)
    file_listbox.grid(row=1, column=0, padx=10, pady=10)
    file_listbox.bind("<Delete>", lambda event: remove_selected_files())
    ToolTip(file_listbox, "Files and folders to be anonymized", delay=0.5)

    file_listbox_buttons_frame = tk.Frame(window)
    file_listbox_buttons_frame.grid(row=1, column=1, padx=10, pady=10)

    select_file_button = tk.Button(file_listbox_buttons_frame, text="Select File(s)/Dir(s)", command=browse_files)
    select_file_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    remove_file_button = tk.Button(file_listbox_buttons_frame, text="Remove Selected", command=remove_selected_files)
    remove_file_button.grid(row=1, column=0, padx=10, pady=10)

    output_dir_label = tk.Label(window, text="Selected Output Directory:")
    output_dir_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    output_dir_entry = tk.Entry(window, width=50, borderwidth=1, relief=tk.SOLID)
    output_dir_entry.grid(row=4, column=0, padx=10, pady=10)
    ToolTip(output_dir_entry, "The folder to save the anonymized files", delay=0.5)

    select_output_button = tk.Button(window, text="Select Output Directory", command=browse_output_dir)
    select_output_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    ToolTip(select_output_button, "The folder to save the anonymized files", delay=1)

    # Advanced Options button
    advanced_options_button = tk.Button(window, text="Show Advanced Options", command=toggle_advanced_options)
    advanced_options_button.grid(row=5, columnspan=2, pady=10)
    advanced_options_frame = tk.Frame(window)

    # Labels for advanced options
    force_anonymize_columns_label = tk.Label(advanced_options_frame, text="Force Anonymize Columns:")
    force_anonymize_tokens_label = tk.Label(advanced_options_frame, text="Force Anonymize Tokens:")
    stop_words_label = tk.Label(advanced_options_frame, text="Stop Words:")

    # Listboxes for advanced options
    force_anonymize_columns_listbox = ListboxEditable(advanced_options_frame, selectmode=tk.MULTIPLE, height=6,
                                                      width=20, borderwidth=1,
                                                      relief=tk.SOLID)
    force_anonymize_tokens_listbox = ListboxEditable(advanced_options_frame, selectmode=tk.MULTIPLE, height=6, width=20,
                                                     borderwidth=1,
                                                     relief=tk.SOLID)
    stop_words_listbox = ListboxEditable(advanced_options_frame, selectmode=tk.MULTIPLE, height=6, width=20,
                                         borderwidth=1,
                                         relief=tk.SOLID)
    force_anonymize_columns_label.grid(row=0, column=0, padx=10)
    force_anonymize_tokens_label.grid(row=0, column=1, padx=10)
    stop_words_label.grid(row=0, column=2, padx=10)
    force_anonymize_columns_listbox.grid(row=1, column=0, padx=10)
    force_anonymize_tokens_listbox.grid(row=1, column=1, padx=10)
    stop_words_listbox.grid(row=1, column=2, padx=10)

    # Set default values for advanced options
    stop_words_listbox.add_list(default_stop_words)

    # Tooltips for advanced options
    force_anonymize_columns_tooltip = ToolTip(force_anonymize_columns_listbox,
                                              "Names of the columns to be forcibly anonymized, regardless of the content type.\n\nType and hit \"enter\" to add a column name.",
                                              delay=0.3)
    force_anonymize_tokens_tooltip = ToolTip(force_anonymize_tokens_listbox,
                                             "Special tokens that should always be anonymized, e.g. person names that were not detected.\n\nType and hit \"enter\" to add a token.",
                                             delay=0.3)
    stop_words_tooltip = ToolTip(stop_words_listbox,
                                 'Special words that implicate the previous word should be anonymized, e.g. "病院" or "クリニック".\n\nType and hit \"enter\" to add a stop word.',
                                 delay=0.3)

    # Anonymize Documents button
    anonymize_button = tk.Button(window, text="Anonymize Documents", command=anonymize_documents)
    anonymize_button.grid(row=7, column=0, columnspan=2, pady=20)

    # Results text area
    results_label = tk.Label(window, text="Results:")
    results_label.grid(row=8, column=0, padx=10, sticky="w")

    results_text = tk.Text(window, height=10, width=50, state=tk.DISABLED, borderwidth=1, relief=tk.SOLID)
    results_text.grid(row=9, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    # Configure row and column weights to make the listbox and results text area expandable
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Start the main loop
    window.mainloop()
