def get_font_attributes(dct):
    if 'font_name' in dct:
        attribute = dct['font_name'].split('-')
        if len(attribute) > 1:
            key = attribute[-1].lower()
            dct[key] = True
    return dct