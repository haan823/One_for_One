def convert_date_PytoJs(str):
    str.replace('-', '/')
    for i in range(len(str)):
        if str[i] == '.':
            return str[0:10] + '/' + str[11:i]
    return None

# '2020-02-18 07:45:03.654487'
