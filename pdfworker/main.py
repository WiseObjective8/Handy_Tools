import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QWidget,
    QMessageBox,
    QLineEdit,
)
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import os


class PDFToolApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Tool")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Choose a PDF file to start", self)
        layout.addWidget(self.label)

        self.choose_pdf_btn = QPushButton("Select PDF", self)
        self.choose_pdf_btn.clicked.connect(self.open_pdf)
        layout.addWidget(self.choose_pdf_btn)

        self.extract_pages_btn = QPushButton("Extract Pages", self)
        self.extract_pages_btn.clicked.connect(self.extract_pages)
        layout.addWidget(self.extract_pages_btn)

        self.extract_range_btn = QPushButton("Extract Specified Pages", self)
        self.extract_range_btn.clicked.connect(self.extract_range)
        layout.addWidget(self.extract_range_btn)

        self.insert_pages_btn = QPushButton("Insert External Pages", self)
        self.insert_pages_btn.clicked.connect(self.insert_pages)
        layout.addWidget(self.insert_pages_btn)

        self.merge_pdfs_btn = QPushButton("Merge PDFs", self)
        self.merge_pdfs_btn.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.merge_pdfs_btn)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.pdf_file_path = ""

    def open_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        if file_path:
            self.pdf_file_path = file_path
            self.label.setText(f"Selected PDF: {os.path.basename(file_path)}")

    def extract_pages(self):
        if not self.pdf_file_path:
            self.show_error("No PDF selected.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not output_dir:
            return

        reader = PdfReader(self.pdf_file_path)
        for page_num in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            output_pdf = os.path.join(output_dir, f"page_{page_num+1}.pdf")
            with open(output_pdf, "wb") as out_file:
                writer.write(out_file)

            images = convert_from_path(
                self.pdf_file_path, first_page=page_num + 1, last_page=page_num + 1
            )
            for img in images:
                img.save(os.path.join(output_dir, f"page_{page_num+1}.jpg"), "JPEG")

        self.show_message("Pages extracted successfully.")

    def extract_range(self):
        if not self.pdf_file_path:
            self.show_error("No PDF selected.")
            return

        start, ok_start = self.get_page_input("Enter start page:")
        end, ok_end = self.get_page_input("Enter end page:")

        if not (ok_start and ok_end and start <= end):
            self.show_error("Invalid page range.")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Extracted Pages As", "", "PDF Files (*.pdf)"
        )
        if not output_file:
            return

        reader = PdfReader(self.pdf_file_path)
        writer = PdfWriter()

        for page_num in range(start - 1, end):
            writer.add_page(reader.pages[page_num])

        with open(output_file, "wb") as out_file:
            writer.write(out_file)

        self.show_message(f"Pages {start} to {end} extracted successfully.")

    def insert_pages(self):
        if not self.pdf_file_path:
            self.show_error("No PDF selected.")
            return

        external_pdf_path, _ = QFileDialog.getOpenFileName(
            self, "Select External PDF to Insert", "", "PDF Files (*.pdf)"
        )
        if not external_pdf_path:
            return

        reader = PdfReader(self.pdf_file_path)
        external_reader = PdfReader(external_pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        for ext_page in external_reader.pages:
            writer.add_page(ext_page)

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "", "PDF Files (*.pdf)"
        )
        if not output_file:
            return

        with open(output_file, "wb") as out_file:
            writer.write(out_file)

        self.show_message("External pages inserted successfully.")

    def merge_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDFs to Merge", "", "PDF Files (*.pdf)"
        )
        if not files or len(files) < 2:
            self.show_error("Select at least two PDF files.")
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )
        if not output_file:
            return

        writer = PdfWriter()
        for pdf in files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_file, "wb") as out_file:
            writer.write(out_file)

        self.show_message("PDFs merged successfully.")

    def show_message(self, message):
        QMessageBox.information(self, "Success", message)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def get_page_input(self, message):
        num, ok = QLineEdit.getInt(self, "Page Input", message)
        return num, ok


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFToolApp()
    window.show()
    sys.exit(app.exec_())
