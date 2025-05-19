pdf_path = r'msft_ars.pdf'
from time import time
import pdfplumber

start = time()
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()

print(f"Time taken to extract text: {time() - start:.2f} seconds")