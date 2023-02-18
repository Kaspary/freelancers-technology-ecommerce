
def str_as_float(value):
    if not value:
        return value
    
    return float(str(value).replace('.', '').replace(',', '.'))

