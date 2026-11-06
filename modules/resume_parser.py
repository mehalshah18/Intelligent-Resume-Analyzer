
import pymupdf


def extract_text_from_pdf(pdf_file):
    """
    Extract readable text from an uploaded PDF resume.
    """

    try:
        # Handle Streamlit uploaded files
        if hasattr(pdf_file, "getvalue"):
            pdf_bytes = pdf_file.getvalue()

            if not pdf_bytes:
                raise ValueError("The uploaded PDF is empty.")

            pdf_document = pymupdf.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

        # Handle raw bytes
        elif isinstance(pdf_file, bytes):
            pdf_document = pymupdf.open(
                stream=pdf_file,
                filetype="pdf"
            )

        # Handle PDF file paths
        else:
            pdf_document = pymupdf.open(pdf_file)

        extracted_text = []

        # Extract text from every page
        for page in pdf_document:
            text = page.get_text()
            extracted_text.append(text)

        pdf_document.close()

        final_text = "\n".join(extracted_text).strip()

        if not final_text:
            raise ValueError(
                "No readable text found. "
                "The PDF may contain scanned images."
            )

        return final_text

    except Exception as e:
        raise ValueError(f"Resume extraction failed: {e}")
    
