pdf_path = r'msft_ars.pdf'
from time import time
from pdfminer.high_level import extract_text

start = time()
text = extract_text(pdf_path)
print(f"Time taken to extract text: {time() - start:.2f} seconds")