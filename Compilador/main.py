from AnalizadorLexico import analizar_entrada, lexer
from AnalizadorSintactica import (
    leer_gramatica, hallar_primeros, hallar_siguientes, leer_gramatica_tabla,
    leer_conjuntos, construir_tabla, imprimir_tabla, escribir_conjuntos, read_firsts, cargar_tabla,
    analizar_entrada_P, analizar_entrada_A, exportar_arbol_a_dot
)
from AnalizadorSemantico import leer_archivo, extraer_declaraciones_txt, escribir_resultados_txt, extraer_declaraciones_txt, escribir_declaraciones_csv, leer_tabla_simbolos, verificar_tipos, escribir_errores, procesar_archivo_entrada


# Analizador Léxico
Codigo_Base = 'Codigo 5.txt'

with open(Codigo_Base, 'r') as file:
    data = file.read()

tokens_list = analizar_entrada(data)

with open("Input.txt", "w") as f:
    for token in tokens_list:
        f.write(f"{token['type']} ")
    f.write("$\n")

with open("Detalles.txt", "w") as f:
    for token in tokens_list:
        f.write(f"Type: {token['type']}, Value: {token['value']}, Line: {token['line']}, Position: {token['position']}\n")


# Analizador Sintactico
filename = 'LL1 - oficial.txt'
rules = leer_gramatica(filename)
start_symbol = rules[0].split('->')[0].strip()

first = hallar_primeros(rules)
if '' in first:
    del first['']
escribir_conjuntos(first, 'first.txt', 'FIRST')

filename_firsts = read_firsts('first.txt')
follows = hallar_siguientes(rules, filename_firsts, start_symbol)
escribir_conjuntos(follows, 'follow.txt', 'FOLLOW')

firsts_filename = 'first.txt'
follows_filename = 'follow.txt'

rules_T = leer_gramatica_tabla(filename)
firsts_T = leer_conjuntos(firsts_filename)
follows_T = leer_conjuntos(follows_filename)

ll1_table = construir_tabla(rules_T, firsts_T, follows_T)
output_filename = 'table.txt'
imprimir_tabla(ll1_table, output_filename)
print(f"LL(1) tiene su tabla, nombrada {output_filename}")

archivo_tabla = 'LL1 - PS.csv'
tabla = cargar_tabla(archivo_tabla)

archivo_entrada = 'Input.txt'
with open(archivo_entrada, 'r') as file:
    entrada = file.read().split()

if analizar_entrada_P(entrada, tabla):
    print("La entrada es aceptada por la tabla.")
else:
    print("La entrada no es aceptada por la tabla.")

aceptado, raiz = analizar_entrada_A(entrada, tabla)
if aceptado:
    codigo_dot = exportar_arbol_a_dot(raiz)
    with open('arbol_sintactico.dot', 'w') as f:
        f.write(codigo_dot)
