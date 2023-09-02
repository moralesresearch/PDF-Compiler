import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

# Initialize the tkinter app
app = tk.Tk()
app.title("PDF Compiler")

# Set the window dimensions
app.geometry("300x300")  # Width x Height

# Define global list to store selected PDF files
pdf_files = []

# Define PDF Merging Functionality
def merge_pdfs(files):
    merged_pdf = "combined.pdf"
    
    pdf_writer = PyPDF2.PdfWriter()
    for file in files:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    
    with open(merged_pdf, "wb") as output_file:
        pdf_writer.write(output_file)
    
    return merged_pdf

# Define PDF Compression Functionality
def compress_pdf(pdf_file):
    compressed_file = pdf_file.replace('.pdf', '_compressed.pdf')

    with open(pdf_file, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page in pdf.pages:
            writer.add_page(page)

        with open(compressed_file, 'wb') as output_file:
            writer.write(output_file)

    return compressed_file

# Define a function to generate a new unique filename
def generate_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}({counter}){ext}"
        counter += 1
    return filename

# Define an About window
def show_about():
    about_window = tk.Toplevel(app)
    about_window.title("About PDF Compiler")
    about_text = """
    PDF Compiler
    Version: 2.0
    Copyright © 2023 Morales Research Inc and Erick Suarez

    Released: August 30, 2023
    """
    about_label = tk.Label(about_window, text=about_text)
    about_label.pack()

# Define GUI Callbacks
def add_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_files.append(file_path)
        file_listbox.insert(tk.END, os.path.basename(file_path))

def compress_and_merge_pdfs():
    if pdf_files:
        merged_file = merge_pdfs(pdf_files)

        if compress_var.get():
            compressed_file = compress_pdf(merged_file)
            compressed_file = generate_unique_filename(compressed_file)
            status_label.config(text=f"PDFs merged and compressed: {compressed_file}")
        else:
            status_label.config(text=f"PDFs merged: {merged_file}")
    else:
        status_label.config(text="No PDFs selected.")

# Create GUI elements
file_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE)
add_button = tk.Button(app, text="Add PDF File", command=add_pdf_file)
compress_var = tk.BooleanVar()
compress_checkbox = tk.Checkbutton(app, text="Compress Merged PDF", variable=compress_var)
merge_button = tk.Button(app, text="Merge PDFs", command=compress_and_merge_pdfs)
status_label = tk.Label(app, text="Status: ")

# Create a Menu bar
menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add PDF File", command=add_pdf_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Place GUI elements
file_listbox.pack()
add_button.pack()
compress_checkbox.pack()
merge_button.pack()
status_label.pack()

# Start the GUI event loop
app.mainloop()