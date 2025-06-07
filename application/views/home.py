from flask import Blueprint, render_template, request, jsonify
from application.forms.user_upload_form import PDFUploadForm 
from werkzeug.utils import secure_filename
from application.services.pdf_extractor import ocr_pdf_text
import os

# create home blueprint
home = Blueprint('home', __name__)


# define the home route
@home.route('/', methods=['GET'])
def home_page():
    form = PDFUploadForm()
    return render_template('home/home.html', form=form)


# define the upload pdf route
@home.route('/upload_pdf', methods=['GET', 'POST'])
def upload_pdf():
    form = PDFUploadForm()
    upload_folder = 'uploads'

    if form.validate_on_submit():
        file = form.pdf_file.data
        filename = secure_filename(file.filename)

        # validate file extension
        if not filename.lower().endswith('.pdf'):
            return jsonify({
                "success": False,
                "message": "Invalid file type. Please upload a PDF."
            }), 400

        # save the uploaded file
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # try to extract text
        try:
            extracted_text = ocr_pdf_text(filepath)
            return jsonify({
                "success": True,
                "extracted_text": extracted_text
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Failed to process PDF: {str(e)}"
            }), 500

    # handle GET or invalid submission
    if request.method == 'GET':
        return render_template('home/home.html', form=form)

    # handle form errors (e.g., no file uploaded)
    return jsonify({
        "success": False,
        "message": "Form validation failed.",
        "errors": form.errors
    }), 400

