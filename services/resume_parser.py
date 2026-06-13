import fitz  # PyMuPDF


def extract_resume_text(pdf_file):
    """
    Extract text from uploaded PDF resume
    """
    text = ""

    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf_document:
        text += page.get_text()

    return text