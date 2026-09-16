import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file provided as bytes.
    Raises ValueError if no text could be extracted or if the PDF is invalid.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Invalid or corrupted PDF file: {e}")

    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text() + "\n"
        
    doc.close()
    
    clean_text = extracted_text.strip()
    if not clean_text:
        raise ValueError("Could not extract any text from the PDF. It might be a scanned image.")
        
    return clean_text
