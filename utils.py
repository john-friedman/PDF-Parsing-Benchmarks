import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from ctypes import c_ushort, c_ulong, POINTER, c_float, c_void_p, c_size_t, c_uint8
from time import time

def get_text(text_page,obj):
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
    # remove buffer
    text = text.strip('\x00')
    return text

def get_font(obj):
    font = pdfium_c.FPDFTextObj_GetFont(obj.raw)
    return font

def get_font_data(font):
    font_data_len = pdfium_c.FPDFFont_GetFontData(
        font,                  # FPDF_FONT
        None,                 # POINTER(uint8_t) - NULL to get the length
        c_size_t(0),         # c_size_t - specify 0 to get the required buffer size
        None                  # POINTER(c_size_t) - NULL to get the length
    )
    print(f"Font data length: {font_data_len}")

    # FPDFFont_GetFontData.argtypes = [FPDF_FONT, POINTER(uint8_t), c_size_t, POINTER(c_size_t)]
            # font = pdfium_c.FPDFTextObj_GetFont(obj.raw)
        # #[FPDF_FONT, POINTER(uint8_t), c_size_t, POINTER(c_size_t)]
        # font_len = pdfium_c.FPDFFont_GetFontData(
        #     font,
        #     c_uint8(0), 
        #     c_size_t(0),
        #     c_size_t(0)
        # )
        # print(f"Font length: {font_len}")