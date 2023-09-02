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
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Determine the output folder (Documents or Desktop)
    # Change to "~/Desktop" for Desktop
    output_folder = os.path.expanduser("~/Documents")

    # Save the combined PDF to a new file
    output_pdf = os.path.join(output_folder, 'combined.pdf')
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    result_label.config(text="PDFs combined successfully!")


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


def clear_list():
    pdf_list.delete(0, tk.END)
    pdf_paths.clear()


def show_about():
    about_text = "PDF Compiler\nVersion 1.1\nReleased on September 2, 2023\n\nCopyright © 2023 Morales Research Inc and Erick Suarez"
    messagebox.showinfo("About", about_text)


# Create the main window
root = tk.Tk()
root.title("PDF Compiler")

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

combine_button = tk.Button(root, text="Combine PDFs", command=combine_pdfs)
remove_button = tk.Button(
    root, text="Remove Selected", command=remove_selected)
clear_button = tk.Button(root, text="Clear List", command=clear_list)
result_label = tk.Label(root, text="")

combine_button.pack(side=tk.LEFT, padx=5, pady=5)
remove_button.pack(side=tk.LEFT, padx=5, pady=5)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

about_button = tk.Button(root, text="About", command=show_about)
about_button.pack(side=tk.RIGHT, padx=5, pady=5)

result_label.pack(padx=10, pady=5, fill=tk.X)

# Dictionary to store file paths with displayed file names
pdf_paths = {}

# Start the GUI event loop
root.mainloop()
