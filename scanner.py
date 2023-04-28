# Archivo generado automáticamente por el programa de instalación de la aplicación
import pickle
import sys

TOKENS = {0: '', 1: ' return ID ', 2: ' return PLUS ', 3: ' return TIMES ', 4: ' return LPAREN ', 5: ' return RPAREN '}

def print_tokens():
    return TOKENS

def simular_afd2(afdd, cadena):
    estado_actual = afdd.getEstadoInicial()
    cadena_aceptada = False
    estado_aceptado = []
    # print(estado_actual.id)
    cadena_leida = ''
    while len(cadena) > 0:
        for char in cadena:
            # print(char)
            estado_siguiente = estado_actual.getTransition(char)
            if estado_siguiente:
                cadena_leida += char
                estado_actual = estado_siguiente[0]
                # print(estado_actual.id)
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

def main():
    with open('afdd.pickle', 'rb') as f:
        afdd = pickle.load(f)
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as f:
                validacion = f.read()
        except:
            print('Archivo no encontrado')
            exit()
    else:
        print('Parametros incorrectos')
        exit()
    
    simular_afd2(afdd, validacion)

if __name__ == '__main__':
    main()