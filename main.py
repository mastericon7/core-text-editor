import tkinter as tk
from tkinter import filedialog
import keyword
import tokenize
from io import BytesIO

def open_file(event=None):
    file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        window.title(f"Python Text Editor - {file_path}")

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get(1.0, tk.END))
        window.title(f"Python Text Editor - {file_path}")

def new_file(event=None):
    text.delete(1.0, tk.END)
    window.title("Python Text Editor")

def apply_syntax_highlighting(event=None):
    text.tag_remove("keyword", 1.0, tk.END)
    text.tag_remove("string", 1.0, tk.END)
    text.tag_remove("comment", 1.0, tk.END)
    text.tag_remove("number", 1.0, tk.END)

    code = text.get(1.0, tk.END)
    tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)

    for token in tokens:
        start_index = f"{token.start[0]}.{token.start[1]}"
        end_index = f"{token.end[0]}.{token.end[1]}"

        if token.type == tokenize.NAME and keyword.iskeyword(token.string):
            text.tag_add("keyword", start_index, end_index)
        elif token.type == tokenize.STRING:
            text.tag_add("string", start_index, end_index)
        elif token.type == tokenize.COMMENT:
            text.tag_add("comment", start_index, end_index)
        elif token.type == tokenize.NUMBER:
            text.tag_add("number", start_index, end_index)

# Create the main window
window = tk.Tk()
window.title("Python Text Editor")

# Create a text widget
text = tk.Text(window, wrap="word", font=("Courier New", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
text.pack(expand=True, fill="both", side="left")

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(window, command=text.yview)
scrollbar.pack(fill="y", side="right")
text.config(yscrollcommand=scrollbar.set)

# Set up the dark theme
window.config(bg="#1e1e1e")

# Create a menu bar
menu_bar = tk.Menu(window)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add the menu bar to the window
window.config(menu=menu_bar)

# Configure syntax highlighting
text.tag_configure("keyword", foreground="#569cd6", font=("Courier New", 12, "bold"))
text.tag_configure("string", foreground="#ce9178")
text.tag_configure("comment", foreground="#608b4e", font=("Courier New", 12, "italic"))
text.tag_configure("number", foreground="#b5cea8")

# Bind the syntax highlighting function to key events
text.bind("<KeyRelease>", apply_syntax_highlighting)

# Bind the key bindings
window.bind("<Control-n>", new_file)
window.bind("<Control-o>", open_file)
window.bind("<Control-s>", save_file)

# Run the Tkinter event loop
window.mainloop()
