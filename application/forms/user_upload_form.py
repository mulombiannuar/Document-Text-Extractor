from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class PDFUploadForm(FlaskForm):
    pdf_file = FileField('Upload PDF', validators=[
        FileRequired(message="Please upload a PDF file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed.")
    ])