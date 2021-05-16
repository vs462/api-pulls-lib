

def col_input_check(cols):
    if type(cols) is list:
        return cols
    elif type(cols) is str:
        return [cols]
    else:
        raise Exception("Pass in either a string or a list!")
        
def col_input_check2(cols):
    cols = [cols] * (type(cols) is str) 
    return cols   


test = col_input_check2('poo')