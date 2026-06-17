import fitz  # PyMuPDF


def extract_resume_text(pdf_file):
    """
    Extract text from an uploaded PDF resume.

    Handles:
    - Corrupt or unreadable PDFs (raises ValueError with user-friendly message)
    - Scanned/image-based PDFs that produce empty text (raises ValueError)
    - Any unexpected fitz errors (re-raised as ValueError)

    The caller (app.py) is responsible for catching ValueError and
    showing the user-friendly error message.
    """

    try:
        # Read the uploaded file bytes
        file_bytes = pdf_file.read()

        if not file_bytes:
            raise ValueError(
                "The uploaded file is empty. Please try another file."
            )

        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

        text = ""
        for page in pdf_document:
            page_text = page.get_text()
            if page_text:
                text += page_text

        pdf_document.close()

        return text

    except fitz.FileDataError as e:
        raise ValueError(
            f"Could not read this PDF. The file may be corrupt. ({e})"
        )

    except Exception as e:
        # Re-raise as ValueError so app.py can catch it uniformly
        raise ValueError(
            f"PDF extraction failed: {e}"
        )