def is_letter(char):
    ascii_val = ord(char)
    return (ascii_val >= 65 and ascii_val <= 90) or (ascii_val >= 97 and ascii_val <= 122)

def is_digit(char):
    ascii_val = ord(char)
    return ascii_val >= 48 and ascii_val <= 57

def quitar_espacios(string):
    result = ""
    for char in string:
        if char != " ":
            result += char
    return result

def leer_entre_comillas(string):
    result = ""
    for index, char in enumerate(string):
        if char == " ":
            if index == 0 or index == len(string) - 1:
                continue
            elif string[index - 1] != "'" and string[index + 1] != "'" and string[index - 1] != '"' and string[index + 1] != '"':
                continue
        result += char
    return result

def find_char(string, char):
    for index, char_ in enumerate(string):
        if char_ == char:
            return index
    return -1

def find_string(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return index
    return -1

def check_string(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return True
    return False

def find_var(string, index, string_to_find):
    for i in range(index, len(string)):
        if string[i:i + len(string_to_find)] == string_to_find:
            return i
    return -1

def reemplazar(original_str, old_substring, new_substring):
    result_str = ""
    sub_len = len(old_substring)
    i = 0

    while i < len(original_str):
        # Buscar la siguiente ocurrencia de la subcadena a reemplazar
        j = find_var(original_str, i, old_substring)

        # Si no, agregar el resto del string original al resultado
        if j == -1:
            result_str += original_str[i:]
            break

        # Agregar el segmento del string original que está antes de la ocurrencia de la subcadena a reemplazar
        result_str += original_str[i:j]

        # Agregar la subcadena de reemplazo al resultado
        result_str += new_substring

        # Actualizar el índice para continuar la búsqueda después de la ocurrencia actual de la subcadena a reemplazar
        i = j + sub_len

    return result_str

def find_replace(string, string_to_replace, string_to_replace_with):
    words = []
    word = ""
    for char in string:
        if is_letter(char) or is_digit(char):
            word += char
        else:
            if word != "":
                words.append(word)
                word = ""
            words.append(char)
    if word != "":
        words.append(word)

    resultado = ""
    for word in words:
        if word == string_to_replace:
            resultado += string_to_replace_with
        else:
            resultado += word
    return resultado

def expand_range(range_str):
    expanded_str = ""
    while find_char(range_str, "-") != -1:
        index = find_char(range_str, "-")
        for j in range(ord(range_str[index-2]), ord(range_str[index+2])+1):
            if j == ord(range_str[index+2]):
                expanded_str += chr(j)
            else:
                expanded_str += chr(j) + "|"
        if range_str[index+4] == "]":
            range_str = range_str[:index-3] + \
                expanded_str + range_str[index+4:]
        else:
            range_str = range_str[:index-3] + \
                expanded_str + '|' + range_str[index+4:]
        expanded_str = ""
    return range_str

def check_range(range_str):
    for i in range(len(range_str)):
        if range_str[i] == "-":
            if is_letter(range_str[i-2]) and is_letter(range_str[i+2]):
                continue
            elif is_digit(range_str[i-2]) and is_digit(range_str[i+2]):
                continue
            else:
                return False
    return True
