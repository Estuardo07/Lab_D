import graphviz

OPS = ['|', '.', '*', '+', '?', '(', ')']
PARENTHESIS = ['(', ')']
TOKEN = {0: 'Return Number'}

class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.val = simbolo
        self.id = ord(simbolo)
        self.is_operator = is_operator

class Transition:
    def __init__(self, simbolo, estado):
        self.simbolo = simbolo
        self.estado = estado

class Estado:
    def __init__(self, id, es_final=False, token=None):
        self.id = id
        self.es_final = es_final
        self.token = token
        self.trancisiones = {}

    def addTransition(self, simbolo, estado):
        if simbolo in self.trancisiones:
            self.trancisiones[simbolo].append(estado)
        # Si el simbolo no existe en las trancisiones se crea una nueva trancision
        else:
            self.trancisiones[simbolo] = [estado]
    
    # Se obtienen las trancisiones de un estado
    def getTransition(self, simbolo):
        if simbolo in self.trancisiones:
            return self.trancisiones[simbolo]
        else:
            return []

    def delTransition(self, simbolo):
        if simbolo in self.trancisiones:
            del self.trancisiones[simbolo]

class AFD:

    def __init__(self):
        self.estados = set()
        self.estados_iniciales = set()
        self.estados_finales = set()

    def getEstados(self):
        return self.estados

    def getEstadosFinales(self):
        return self.estados_finales

    def armarAFD(self):
        dot = graphviz.Digraph(comment='AFD')
        for estado in self.estados:
            if estado.es_final:
                dot.node(str(estado.id), str(estado.id), shape="doublecircle")
            else:
                dot.node(str(estado.id), str(estado.id))
        for estado in self.estados:
            for simbolo in estado.trancisiones:
                for estado_siguiente in estado.getTransition(simbolo):
                    dot.edge(str(estado.id), str(
                        estado_siguiente.id), label=simbolo)
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('AFD2', view=True)

    def getEstado(self, id):
        for estado in self.estados:
            if estado.id == id:
                return estado

    def getEstadoInicial(self):
        for estado in self.estados:
            if estado.id == 0:
                return estado

class Node:
    def __init__(self, valor, id):
        self.valor = valor
        self.id = id
        self.izquierda = None
        self.derecha = None
        self.nulabilidad = None
        self.primera_posicion = set()
        self.ultima_posicion = set()
        self.siguiente_posicion = set()
        self.siguientes_posiciones = []

def crearArbol(postfix):
    stack = []
    id = 0
    for c in postfix:
        if not c.is_operator:
            if c.val == 'ε':
                stack.append(Node(c, None))
            else:
                stack.append(Node(c, id))
                id += 1
        elif c.val == '*' or c.val == '+' or c.val == '?':
            node = Node(c, None)
            node.izquierda = stack.pop()
            stack.append(node)
        elif c.val == "|" or c.val == ".":
            node = Node(c, None)
            node.derecha = stack.pop()
            node.izquierda = stack.pop()
            node.valor = c
            stack.append(node)
    return stack.pop()

def armarArbol(root):
    dot = graphviz.Digraph()

    def traverse(node):
        if node:
            pp = [str(x) for x in node.primera_posicion]
            up = [str(x) for x in node.ultima_posicion]
            r = node.valor + " " + str(pp) + " " + \
                str(up) + " " + str(node.nulabilidad)
            s = [str(x) for x in node.siguiente_posicion]
            dot.node(str(id(node)), str(r))
            if node.izquierda:
                dot.edge(str(id(node)), str(id(node.izquierda)))
            if node.derecha:
                dot.edge(str(id(node)), str(id(node.derecha)))
            traverse(node.izquierda)
            traverse(node.derecha)

    traverse(root)
    return dot

def calcNullable(root):
    if root is None:
        return False
    if not root.valor.is_operator:
        if root.valor.val == 'ε':
            root.nulabilidad = True
        else:
            root.nulabilidad = False
        return False
    if root.valor.val == '|':
        nullable = root.izquierda.nulabilidad or root.derecha.nulabilidad
    elif root.valor.val == '.':
        nullable = root.izquierda.nulabilidad and root.derecha.nulabilidad
    elif root.valor.val == '*':
        nullable = True
    elif root.valor.val == '+':
        nullable = root.izquierda.nulabilidad
    elif root.valor.val == '?':
        nullable = True
    else:
        nullable = False
    root.nulabilidad = nullable
    return nullable or False

def posorden(node, func):
    if node is not None:
        posorden(node.izquierda, func)
        posorden(node.derecha, func)
        func(node)

def firstpos(node):
    if node:
        # Si el nodo es una hoja, su primera posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.primera_posicion.add(node.id)
        # Si el nodo es un operador '.' su primera posición es la primera posición de su hijo izquierdo
        elif node.valor.val == '.' and node.valor.is_operator:
            firstpos(node.izquierda)
            firstpos(node.derecha)
            if node.izquierda.nulabilidad:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
            else:
                node.primera_posicion = node.izquierda.primera_posicion
        # Si el nodo es un operador '|' su primera posición es la unión de las primeras posiciones de sus dos hijos
        elif node.valor.val == '|' and node.valor.is_operator:
            firstpos(node.izquierda)
            firstpos(node.derecha)
            if list(node.izquierda.primera_posicion)[0] == None:
                node.primera_posicion = node.derecha.primera_posicion
            elif list(node.derecha.primera_posicion)[0] == None:
                node.primera_posicion = node.izquierda.primera_posicion
            else:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
        # Si el nodo es un operador '*' su primera posición es la primera posición de su hijo
        elif node.valor.val == '*' and node.valor.is_operator:
            firstpos(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion
        elif node.valor.val == '+' and node.valor.is_operator:
            firstpos(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion
        elif node.valor.val == '?' and node.valor.is_operator:
            firstpos(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion

    # Calcular la primera posición del nodo raíz
    if node and node.valor.val is not None and node.primera_posicion is None:
        node.primera_posicion = node.izquierda.primera_posicion

def lastpos(node):
    if node:
        # Si el nodo es una hoja, su última posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.ultima_posicion.add(node.id)
        # Si el nodo es un operador '.' su última posición es la última posición de su hijo derecho
        elif node.valor.val == '.' and node.valor.is_operator:
            lastpos(node.izquierda)
            lastpos(node.derecha)
            if node.derecha.nulabilidad:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
            else:
                node.ultima_posicion = node.derecha.ultima_posicion
        # Si el nodo es un operador '|' su última posición es la unión de las últimas posiciones de sus dos hijos
        elif node.valor.val == '|' and node.valor.is_operator:
            lastpos(node.izquierda)
            lastpos(node.derecha)
            if list(node.izquierda.ultima_posicion)[0] == None:
                node.ultima_posicion = node.derecha.ultima_posicion
            elif list(node.derecha.ultima_posicion)[0] == None:
                node.ultima_posicion = node.izquierda.ultima_posicion
            else:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
        # Si el nodo es un operador '*' su última posición es la última posición de su hijo
        elif node.valor.val == '*' and node.valor.is_operator:
            lastpos(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion
        elif node.valor.val == '+' and node.valor.is_operator:
            lastpos(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion
        elif node.valor.val == '?' and node.valor.is_operator:
            lastpos(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion

    # Calcular la última posición del nodo raíz
    if node and node.valor.val is not None and node.ultima_posicion is None:
        node.ultima_posicion = node.derecha.ultima_posicion

def printArbol(arbol):
    if arbol:
        print(arbol.valor.val, arbol.nulabilidad)
        printArbol(arbol.izquierda)
        printArbol(arbol.derecha)

table = []

def followpos(arbol):
    val = True
    if arbol:

        if arbol.valor.val == '.' and arbol.valor.is_operator:
            for i in arbol.izquierda.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.derecha.primera_posicion))
                        val = False
                if val:
                    simbol = getValue(arbol, i)
                    table.append(
                        [i, simbol, list(arbol.derecha.primera_posicion)])
        elif arbol.valor.val == '*' and arbol.valor.is_operator:
            for i in arbol.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.primera_posicion))
                        val = False
                if val:
                    simbol = getValue(arbol, i)
                    table.append([i, simbol, list(arbol.primera_posicion)])
        elif arbol.valor.val == '+' and arbol.valor.is_operator:
            for i in arbol.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.primera_posicion))
                        val = False
                if val:
                    simbol = getValue(arbol, i)
                    table.append([i, simbol, list(arbol.primera_posicion)])
        val = False
        for k in table:
            if k[0] == arbol.id:
                val = True
        if not val:
            simbol = getValue(arbol, arbol.id)
            table.append([arbol.id, simbol, []])
        for i in table:
            if i[0] is None:
                table.remove(i)

        followpos(arbol.izquierda)
        followpos(arbol.derecha)

def getValue(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.valor.val
        else:
            return getValue(arbol.izquierda, id) or getValue(arbol.derecha, id)

def getFirstpos(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.primera_posicion
        else:
            return getFirstpos(arbol.izquierda, id) or getFirstpos(arbol.derecha, id)

def getNextpos(tab, id):
    for i in tab:
        if i[0] == id:
            return i[2]

def Trans(state, simbol, tab):
    conj = []
    for i in state:
        for j in tab:
            if j[0] == i and j[1] == simbol:
                for k in j[2]:
                    if k not in conj:
                        conj.append(k)
    return conj

def getSymbols(tab):
    simbols = []
    for i in tab:
        if i[1] not in simbols:
            simbols.append(i[1])
    return simbols

def getEstadoFinal(tab):
    final_state = []
    for i in tab:
        if i[1] == '#':
            final_state.append(i[0])
    return final_state

def regex_to_afd(regex, token_dic):
    TOKEN = token_dic
    arbol = crearArbol(regex)
    calcNullable(arbol)
    posorden(arbol, calcNullable)
    firstpos(arbol)
    lastpos(arbol)
    followpos(arbol)
    tab = sorted(table, key=lambda x: x[0])
    root = arbol.primera_posicion
    alfabeto = getSymbols(tab)
    alfabeto.remove('#')
    afdd = AFD()
    conjunto_estados = {}
    transiciones = []
    id = 0
    x = []
    for y in root:
        x.append(y)
    conjunto_estados[id] = x
    id += 1
    estados_visitados = []
    estados_por_visitar = []
    estados_por_visitar.append(conjunto_estados[0])
    final = getEstadoFinal(tab)
    while len(estados_por_visitar) > 0:
        estado_actual = estados_por_visitar.pop()
        estados_visitados.append(estado_actual)
        for simbolo in alfabeto:
            transicion = Trans(estado_actual, simbolo, tab)
            transicion = sorted(transicion)

            if transicion != [] and not None:
                transiciones.append([estado_actual, simbolo, transicion])
                if transicion not in estados_visitados and transicion not in estados_por_visitar:
                    conjunto_estados[id] = transicion
                    estados_por_visitar.append(transicion)
                    estados_por_visitar = sorted(
                        estados_por_visitar, reverse=True)
                    id += 1

    for key, value in conjunto_estados.items():
        if value == []:
            del conjunto_estados[key]
            break

    newTransitions = []
    for key, value in conjunto_estados.items():
        for i in transiciones:
            if i[0] == value:
                newTransitions.append([key, i[1], i[2]])
    for key, value in conjunto_estados.items():
        for i in newTransitions:
            if i[2] == value:
                i[2] = key

    numEstados = []
    for key, value in conjunto_estados.items():
        numEstados.append(key)
    numEstados = set(numEstados)
    for e in numEstados:
        es = Estado(e)
        for key, value in conjunto_estados.items():
            if key == e:
                for val in value:
                    if val in final:
                        es.es_final = True
                        k = final.index(val)
                        es.token = TOKEN[k]
        afdd.estados.add(es)

    for estado in afdd.estados:
        for k in newTransitions:
            if k[0] == estado.id:
                estado.addTransition(k[1], afdd.getEstado(k[2]))

    return afdd

def simularAFD(afdd, cadena):
    estado_actual = afdd.getEstadoInicial()
    cadena_aceptada = False
    estado_aceptado = []
    cadena_leida = ''
    while len(cadena) > 0:
        for char in cadena:
            estado_siguiente = estado_actual.getTransition(char)
            if estado_siguiente:
                cadena_leida += char
                estado_actual = estado_siguiente[0]
                if estado_actual.es_final:
                    estado_aceptado.append([estado_actual, cadena_leida])
            else:
                if estado_aceptado != []:
                    token_encontrado = estado_aceptado.pop()
                    print(token_encontrado[1], token_encontrado[0].token)

                    cadena = cadena[len(token_encontrado[1]):]
                    estado_actual = afdd.getEstadoInicial()
                    cadena_leida = ''
                    estado_aceptado = []
                    break
                else:
                    cadena_leida += char
                    print(cadena_leida, 'Lexical error')
                    cadena = cadena[len(cadena_leida):]
                    estado_actual = afdd.getEstadoInicial()
                    cadena_leida = ''
                    break
        if estado_aceptado != []:
            token_encontrado = estado_aceptado.pop()
            print(token_encontrado[1], token_encontrado[0].token)
            break
