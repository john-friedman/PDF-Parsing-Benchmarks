import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from ctypes import c_ushort, c_ulong, POINTER
from time import time

pdf_path = r'msft_ars.pdf'

start = time()

# Open the PDF
pdf = pdfium.PdfDocument(pdf_path)
text_list = []

# Extract text and font info from each page
for page_index in range(5,6):#len(pdf)):
    page = pdf[page_index]
    text_page = page.get_textpage()
    
    # Get page objects
    for obj in page.get_objects():

        # First call to get the length - pass NULL for the buffer and the maximum length
        # According to the signature: (FPDF_PAGEOBJECT, FPDF_TEXTPAGE, POINTER(FPDF_WCHAR), c_ulong)
        text_len = pdfium_c.FPDFTextObj_GetText(
            obj.raw,               # FPDF_PAGEOBJECT
            text_page.raw,                  # FPDF_TEXTPAGE (NULL in this case)
            None,                  # POINTER(FPDF_WCHAR) - NULL to get the length
            c_ulong(0)             # c_ulong - specify 0 to get the required buffer size
        )
        
        # Create buffer for the text
        buffer = pdfium_c.create_string_buffer(text_len * 2)  # UTF-16LE encoding
        text_ptr = pdfium_c.cast(buffer, pdfium_c.POINTER(pdfium_c.c_ushort))
        
        # Second call to actually get the text
        chars_copied = pdfium_c.FPDFTextObj_GetText(
            obj.raw,               # FPDF_PAGEOBJECT
            text_page.raw,                  # FPDF_TEXTPAGE (NULL in this case)
            text_ptr,              # POINTER(FPDF_WCHAR) - pointer to our buffer
            c_ulong(text_len)      # c_ulong - the buffer size
        )
        
        # Convert UTF-16LE to string
        # Only convert the number of characters actually copied
        text = buffer.raw[:chars_copied*2].decode('utf-16le', errors='ignore')
        text_list.append(text)
        print(f"Text content: {text}")
                
print(f"\nTime taken: {time() - start:.2f} seconds")
# Clean up resources
pdf.close()