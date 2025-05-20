import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from ctypes import c_ushort, c_ulong, POINTER, c_float, c_void_p, c_size_t, c_uint8, c_int
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
    # Get required buffer size for font data
    data_size = c_size_t(0)
    success = pdfium_c.FPDFFont_GetFontData(
        font,                 # FPDF_FONT
        None,                 # buffer (NULL to get size)
        0,                    # buffer size
        pdfium_c.byref(data_size)  # pointer to receive required size
    )

    
    # Allocate buffer for font data
    #buffer = pdfium_c.create_string_buffer(data_size.value)

    
    # Get font name
    name_len = pdfium_c.FPDFFont_GetBaseFontName(font, None, 0)
    name_buffer = pdfium_c.create_string_buffer(name_len)
    pdfium_c.FPDFFont_GetBaseFontName(font, name_buffer, name_len)
    font_name = name_buffer.value.decode('utf-8', errors='replace')
    
    # # Get font family
    # family_len = pdfium_c.FPDFFont_GetFamilyName(font, None, 0)
    # family_buffer = pdfium_c.create_string_buffer(family_len)
    # pdfium_c.FPDFFont_GetFamilyName(font, family_buffer, family_len)
    # font_family = family_buffer.value.decode('utf-8', errors='replace')
    
    # # Get other font properties
    # is_embedded = pdfium_c.FPDFFont_GetIsEmbedded(font)
    # font_flags = pdfium_c.FPDFFont_GetFlags(font)
    # font_weight = pdfium_c.FPDFFont_GetWeight(font)
    
    # # Get italic angle
    # italic_angle = c_int(0)
    # has_italic = pdfium_c.FPDFFont_GetItalicAngle(font, pdfium_c.byref(italic_angle))
    
    return {
        'font_name': font_name,
        # 'family': font_family,
        # 'is_embedded': bool(is_embedded),
        # 'flags': font_flags,
        # 'weight': font_weight,
        # 'italic_angle': italic_angle.value if has_italic else None,
        # 'data_size': data_size.value
    }

def get_font_size(obj):
    font_size = c_float(0.0)
    success = pdfium_c.FPDFTextObj_GetFontSize(
        obj.raw,                     # FPDF_PAGEOBJECT
        pdfium_c.byref(font_size)    # POINTER(c_float)
    )
    
    return {'font_size': font_size.value} if success else {}