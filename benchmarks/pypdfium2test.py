import pypdfium2 as pdfium
from time import time

pdf_path = r'msft_ars.pdf'

start = time()

# Open the PDF
pdf = pdfium.PdfDocument(pdf_path)

# Extract text from each page
for page_index in range(len(pdf)):
    page = pdf[page_index]
    text_page = page.get_textpage()
    text = text_page.get_text_range()


print(f"Time taken to extract text: {time() - start:.2f} seconds")

# Clean up resources
pdf.close()