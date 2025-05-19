import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from ctypes import c_ushort, c_ulong, POINTER, c_float, c_void_p, c_size_t, c_uint8
from time import time
from pdf_utils import get_text, get_font_data, get_font
from utils import get_font_attributes
pdf_path = r'msft_ars.pdf'

start = time()

# Open the PDF
pdf = pdfium.PdfDocument(pdf_path)

# Extract text and font info from each page
for page_index in range(len(pdf)):
    page = pdf[page_index]
    text_page = page.get_textpage()
    
    # Get page objects
    for obj in page.get_objects():

        text = get_text(text_page, obj)
        font = get_font(obj)
        font_raw_data = get_font_data(font)
        font_attributes = get_font_attributes(font_raw_data)



                                

        output_dct = {'text': text} | font_attributes
        #print(f"Text content: {output_dct}")
                
print(f"\nTime taken: {time() - start:.2f} seconds")
# Clean up resources
pdf.close()