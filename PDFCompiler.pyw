import PyPDF3
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QMessageBox

class PDFCompiler(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_paths = {}
        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout(self)
        self.setWindowTitle("PDF Compiler 2.0")

        # Create and add widgets to the layout
        self.pdf_list = QListWidget(self)
        add_button = QPushButton('Add PDFs', self)
        combine_button = QPushButton('Combine PDFs', self)
        self.result_label = QLabel('', self)

        # Add widgets to the layout
        layout.addWidget(self.pdf_list)
        layout.addWidget(add_button)
        layout.addWidget(combine_button)
        layout.addWidget(self.result_label)

        # Connect the button click events
        add_button.clicked.connect(self.add_pdfs)
        combine_button.clicked.connect(self.combine_pdfs)

    def add_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        for file in files:
            if file.endswith('.pdf'):
                self.pdf_list.addItem(os.path.basename(file))
                self.pdf_paths[os.path.basename(file)] = file

    def combine_pdfs(self):
        pdf_files = [self.pdf_paths[self.pdf_list.item(i).text()] for i in range(self.pdf_list.count())]
        if not pdf_files:
            self.result_label.setText("No PDF files to combine.")
            return

        # Create a PDF writer object
        pdf_writer = PyPDF3.PdfFileWriter()

        # Loop through each PDF file and add its pages to the writer
        for pdf_path in pdf_files:
            pdf_reader = PyPDF3.PdfFileReader(pdf_path)
            for page in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page))

        # Save the combined PDF
        output_filename, _ = QFileDialog.getSaveFileName(self, "Save Combined PDF", "", "PDF Files (*.pdf)")
        if output_filename:
            with open(output_filename, 'wb') as out_pdf:
                pdf_writer.write(out_pdf)
            self.result_label.setText(f"Combined PDF saved as {os.path.basename(output_filename)}")
        else:
            self.result_label.setText("PDF combining cancelled.")

if __name__ == '__main__':
    app = QApplication([])
    ex = PDFCompiler()
    ex.resize(400, 300)
    ex.show()
    app.exec()