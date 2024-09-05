import fitz

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_document = fitz.open(pdf_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            print(f"Page {page_num + 1}: {page_text[:500]}")  # Print a snippet of text from each page
            text += page_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text
