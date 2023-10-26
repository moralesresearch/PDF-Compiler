import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def combine_pdfs():
    pdf_files = pdf_list.get(0, tk.END)
    if not pdf_files:
        result_label.config(text="No PDF files to combine.")
        return

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Loop through each PDF file and add its pages to the writer
    for pdf_name in pdf_files:
        pdf_path = pdf_paths[pdf_name]
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_path)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
        except Exception as e:
            result_label.config(text=f"Error reading {pdf_name}. {str(e)}")
            return

    # Determine the output folder (Desktop)
    output_folder = os.path.expanduser("~/Desktop")

    # Use the specified output filename or default to 'combined.pdf'
    output_filename = output_filename_entry.get() or 'combined.pdf'
    output_pdf = os.path.join(output_folder, output_filename)
    
    # PDF Compression
    if compress_pdf_var.get():
        for page_num in range(len(pdf_writer.pages)):
            page = pdf_writer.pages[page_num]
            page.compressContentStreams()

    # Save the combined PDF
    try:
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)
        result_label.config(text="PDFs combined successfully!")
    except Exception as e:
        result_label.config(text=f"Error saving PDF. {str(e)}")

def add_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_name = os.path.basename(file_path)
        pdf_list.insert(tk.END, file_name)
        pdf_paths[file_name] = file_path

def remove_selected():
    selected_indices = pdf_list.curselection()
    for index in selected_indices[::-1]:
        pdf_name = pdf_list.get(index)
        del pdf_paths[pdf_name]
        pdf_list.delete(index)

def move_up():
    selected_indices = pdf_list.curselection()
    if not selected_indices:
        return
    for index in selected_indices:
        if index > 0:
            pdf_name = pdf_list.get(index)
            pdf_list.delete(index)
            pdf_list.insert(index - 1, pdf_name)
            pdf_list.select_set(index - 1)

def move_down():
    selected_indices = pdf_list.curselection()
    if not selected_indices:
        return
    for index in reversed(selected_indices):
        if index < pdf_list.size() - 1:
            pdf_name = pdf_list.get(index)
            pdf_list.delete(index)
            pdf_list.insert(index + 1, pdf_name)
            pdf_list.select_set(index + 1)

def clear_list():
    pdf_list.delete(0, tk.END)
    pdf_paths.clear()

def show_about():
    about_text = "PDF Compiler\nVersion 1.1.2\nReleased on October 26, 2023\n\nCopyright © 2023 Morales Research Inc and Erick Suarez"
    messagebox.showinfo("About", about_text)

# Create the main window
root = tk.Tk()
root.title("PDF Compiler 1.1.2")

# Create the menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create the File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add PDF File", command=add_pdf)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create the Help menu
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Create GUI elements
pdf_list = tk.Listbox(root, selectmode=tk.MULTIPLE)
pdf_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

output_filename_label = tk.Label(root, text="Output File Name:")
output_filename_entry = tk.Entry(root)
output_filename_label.pack(padx=10, pady=5, anchor=tk.W)
output_filename_entry.pack(padx=10, pady=5, fill=tk.X)

compress_pdf_var = tk.IntVar()
compress_pdf_checkbox = tk.Checkbutton(root, text="Compress PDF", variable=compress_pdf_var)
compress_pdf_checkbox.pack(padx=10, pady=5)

combine_button = tk.Button(root, text="Combine PDFs", command=combine_pdfs)
remove_button = tk.Button(
    root, text="Remove Selected", command=remove_selected)
clear_button = tk.Button(root, text="Clear List", command=clear_list)
result_label = tk.Label(root, text="")

combine_button.pack(side=tk.LEFT, padx=5, pady=5)
remove_button.pack(side=tk.LEFT, padx=5, pady=5)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

move_up_button = tk.Button(root, text="Move Up", command=move_up)
move_down_button = tk.Button(root, text="Move Down", command=move_down)
move_up_button.pack(side=tk.LEFT, padx=5, pady=5)
move_down_button.pack(side=tk.LEFT, padx=5, pady=5)

# About button
about_button = tk.Button(root, text="About", command=show_about)
about_button.pack(side=tk.RIGHT, padx=5, pady=5)

result_label.pack(padx=10, pady=5, fill=tk.X)

# Dictionary to store file paths with displayed file names
pdf_paths = {}

# Start the GUI event loop
root.mainloop()
