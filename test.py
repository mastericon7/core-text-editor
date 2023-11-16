import tkinter as tk
from tkinter import filedialog
import keyword

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        window.title(f"Python Text Editor - {file_path}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get(1.0, tk.END))
        window.title(f"Python Text Editor - {file_path}")

def apply_syntax_highlighting(event=None):
    text.tag_remove("keyword", 1.0, tk.END)

    for word in keyword.kwlist:
        start_index = 1.0
        while True:
            start_index = text.search(word, start_index, tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(word)}c"
            text.tag_add("keyword", start_index, end_index)
            start_index = end_index

# Create the main window
window = tk.Tk()
window.title("Python Text Editor")

# Create a text widget
text = tk.Text(window, wrap="word", font=("Courier New", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
text.pack(expand=True, fill="both")

# Set up the dark theme
window.config(bg="#1e1e1e")

# Create a menu bar
menu_bar = tk.Menu(window)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add the menu bar to the window
window.config(menu=menu_bar)

# Configure syntax highlighting
text.tag_configure("keyword", foreground="#569cd6", font=("Courier New", 12, "bold"))

# Bind the syntax highlighting function to key events
text.bind("<KeyRelease>", apply_syntax_highlighting)

# Run the Tkinter event loop
window.mainloop()

