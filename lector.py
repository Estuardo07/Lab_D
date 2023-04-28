from mylib import *
import graphviz

EPSILON = 'ε'
CONCAT = "."
UNION = "|"
KLEENE = "*"
QUESTION = "?"
PLUS = "+"
LEFT_PARENTHESIS = "("
RIGHT_PARENTHESIS = ")"

OPS = [EPSILON, CONCAT, UNION, KLEENE, QUESTION,
              PLUS, LEFT_PARENTHESIS, RIGHT_PARENTHESIS]

OPS_2 = [EPSILON, CONCAT, UNION, KLEENE, QUESTION,
               PLUS, RIGHT_PARENTHESIS]

def check_concat(value):
    array = []
    for char in value:
        array.append(char)

    res = ""
    while array:
        char = array.pop(0)
        if char == ')':
            if array:
                if array[0] not in OPS_2:
                    res += char + CONCAT
                elif array[0] == '#':
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        elif char == "'":
            if array:
                if len(array) >= 3:
                    if array[1] == "'":
                        if array[2] not in OPS_2:
                            res += char + array.pop(0) + array.pop(0) + CONCAT
                        else:
                            res += char + array.pop(0) + array.pop(0)
                elif len(array) == 2:
                    if array[1] == "'":
                        res += char + array.pop(0) + array.pop(0)
        elif char == '"':
            if array:
                items = []
                items.append(char)
                for i in range(len(array)):
                    if array[i] == '"':
                        items.append(array[i])
                        break
                    else:
                        items.append(array[i])
                for i in range(len(items)-1):
                    array.pop(0)
                while items:
                    item = items.pop(0)
                    if item == '"':
                        res += item
                    elif item != '"' and items[0] != '"':
                        res += item + CONCAT
                    else:
                        res += item

        elif char == '*' or char == '?' or char == '+':
            if array:
                if array[0] not in OPS_2:
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        else:
            res += char
    return res

class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.val = simbolo
        self.id = ord(simbolo)
        self.is_operator = is_operator

def str_to_symbol(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char in OPS:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res

# funcion para convertir la cadena a un arreglo de simbolos tomando en cuenta los simbolos de dos caracteres


def str_to_two_symbols(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char == '"':
            items = []
            for i in range(len(array)):
                if array[i] == '"':
                    items.append(array[i])
                    break
                else:
                    items.append(array[i])
            for i in range(len(items)):
                array.pop(0)
            while items:
                item = items.pop(0)
                if item == '.':
                    res.append(Simbolo(item, True))
                elif item != '"':
                    res.append(Simbolo(item))

        elif char in OPS:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res

def shunting_yard(infix):
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3}
    stack = []
    postfix = []
    for c in infix:
        # Si se encuentra un '(' se agrega a la pila
        if c.val == '(' and c.is_operator == True:
            stack.append(c)
        # Si se encuentra un ')' se sacan los operadores de la pila hasta encontrar un '('
        elif c.val == ')' and c.is_operator == True:
            while stack[-1].val != '(' and stack[-1].is_operator == True:
                postfix.append(stack.pop())
            stack.pop()
        # Si se encuentra un operador se sacan los operadores de la pila hasta encontrar un operador de menor precedencia
        elif c.val in precedence and c.is_operator == True:
            while stack and stack[-1].val != '(' and stack[-1].is_operator == True and precedence[c.val] <= precedence[stack[-1].val]:
                postfix.append(stack.pop())
            stack.append(c)
        # Si se encuentra un simbolo se agrega a la cola
        else:
            postfix.append(c)
    # Se sacan los operadores restantes de la pila y se agregan a la cola
    while stack:
        postfix.append(stack.pop())

    return postfix

class Node:
    def __init__(self, data):
        self.id = id(self)
        self.data = data
        self.left = None
        self.right = None

def armarArbol(postfix):
    stack = []
    for c in postfix:
        if not c.is_operator:
            stack.append(Node(c))
        elif c.val == '*' or c.val == '?' or c.val == '+':
            node = Node(c)
            node.left = stack.pop()
            stack.append(node)
        else:
            node = Node(c)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack.pop()

def printArbol(root):
    dot = graphviz.Digraph()

    def traverse(node):
        if node:
            dot.node(str(id(node)), node.data.val)
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return dot

def mostrarArbol(postfix, nombre):
    tree = armarArbol(postfix)
    dot = printArbol(tree)
    dot.format = 'png'
    dot.render('arboles/' + nombre, view=False)

TOKENS = {}

def readYal(archivo):
    with open(archivo, "r") as file:
        content = file.read()

    while '(*' in content:
        content = content[:find_string(content, '(*')] + \
            content[find_string(content, "*)") + 2:]

    while '\n' in content:
        content = content[:find_char(content, '\n')] + \
            " " + content[find_char(content, '\n') + 1:]

    abcd = 'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z'
    ABCD = 'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z'
    digits = '0|1|2|3|4|5|6|7|8|9'

    variables = {}

    # Guardar cada expresion regular dentro de la seccion de definicion regular
    while 'let' in content:
        index = find_string(content, 'let ')
        content = content[index + 3:]
        name = content[:find_char(content, '=')]
        name = quitar_espacios(name)
        if find_string(content, 'let ') == -1:
            value = content[find_string(content, '=') +
                            1: find_string(content, 'rule tokens')]
            value = leer_entre_comillas(value)
            variables[name] = value
            content = content[find_string(content, 'rule tokens'):]
        else:
            value = content[find_string(content, '=') + 1:find_string(content, 'let ')]
            value = leer_entre_comillas(value)
            variables[name] = value
            content = content[find_string(content, 'let '):]

    # Guardar cada token dentro de la seccion de rule tokens
    rule_tokens = []
    while content != '':
        if check_string(content, 'rule tokens'):
            index = find_string(content, 'rule tokens')
            content = content[index + 11:]
            rule = content[find_char(content, '=') + 1:find_char(content, '|')]
            rule_tokens.append(rule)
            content = content[find_char(content, '|') + 1:]
        elif check_string(content, '|'):
            rule = content[:find_char(content, '|')]
            rule_tokens.append(rule)
            content = content[find_char(content, '|') + 1:]
        else:
            rule = content
            rule_tokens.append(rule)
            content = ''

    tuples = []
    for rule in rule_tokens:
        if '{' in rule:
            tuples.append(
                (rule[:find_char(rule, '{')], rule[find_char(rule, '{') + 1:find_char(rule, '}')]))
        else:
            tuples.append((rule, ''))

    rule_tokens = []
    for rule in tuples:
        rule_tokens.append(quitar_espacios(rule[0]))

    i = 0
    for rule in tuples:
        TOKENS[i] = rule[1]
        i += 1

    newVariables = {}
    keys_array = list(variables.keys())

    for key, value in variables.items():
        if check_range(value):
            value = expand_range(value)
            variables[key] = value

    for key, value in variables.items():
        for key2 in keys_array:
            value = find_replace(value, key2, variables[key2])
        variables[key] = value
        newVariables[key] = value

    for key, value in newVariables.items():
        if check_string(value, "'A'-'Z''a'-'z'"):
            value = reemplazar(value, "'A'-'Z''a'-'z'",
                               ABCD + '|' + abcd)
        if check_string(value, "'A'-'Z'"):
            value = value.replace("'A'-'Z'", ABCD)
        if check_string(value, "'a'-'z'"):
            value = value.replace("'a'-'z'", abcd)
        if check_string(value, "'0'-'9'"):
            value = value.replace("'0'-'9'", digits)
        if check_string(value, "' ''\\t''\\n'"):
            value = value.replace("' ''\\t''\\n'", ' ' +
                                  '|' + '\t' + '|' + '\n')
        if check_string(value, '"\\s\\t\\n"'):
            value = value.replace('"\\s\\t\\n"', ' ' + '|' + '\t' + '|' + '\n')
        if check_string(value, "'+''-'"):
            value = value.replace("'+''-'", "'+'" + '|' + "'-'")
        if check_string(value, '"0123456789"'):
            value = value.replace('"0123456789"', digits)
        newVariables[key] = value

    for key, value in newVariables.items():
        if check_string(value, '['):
            value = reemplazar(value, '[', '(')
        if check_string(value, ']'):
            value = reemplazar(value, ']', ')')
        newVariables[key] = value

    for key, value in newVariables.items():
        newVariables[key] = check_concat(value)

    new_rule_tokens = []
    for rule in rule_tokens:
        for key, value in newVariables.items():
            if rule == key:
                rule = value
        new_rule_tokens.append(rule)

    for rule in new_rule_tokens:
        if rule[0] != "'" and rule[0] != '(' and rule[0] != '"':
            print(key, 'Error: ' + rule +
                  'Token no valido\n')
            exit()

    rule_token_regex = ""
    for rule in new_rule_tokens:
        if rule == new_rule_tokens[-1]:
            rule_token_regex += '(' + '(' + rule + ')' + '#' + ')'
        else:
            rule_token_regex += '(' + '(' + rule + ')' + '#' + ')' + '|'

    rule_token_regex = check_concat(rule_token_regex)

    definicion_regular = {}

    # Convertir la cadena a un arreglo de simbolos
    rule_token_regex = str_to_two_symbols(rule_token_regex)

    # Convertir cada variable a un arreglo de simbolos
    for key, value in newVariables.items():
        definicion_regular[key] = str_to_symbol(value)

    # Aplicar shunting_yard a cada variable
    definicion_regular_postfix = {}
    for key, value in definicion_regular.items():
        definicion_regular_postfix[key] = shunting_yard(value)

    # Aplicar shunting_yard a los tokens
    rule_token_regex_postfix = shunting_yard(rule_token_regex)

    return rule_token_regex_postfix, TOKENS
