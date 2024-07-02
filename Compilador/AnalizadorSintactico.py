import csv
from collections import deque
import re

# ANALIZADOR SINTACTICO

# Para identificar los terminales y no terminales
def identificar_terminal_noterminal(rules):
      non_terminals = set()
      all_symbols = set()

      for rule in rules:
          lhs, rhs = re.split(r'\s*->\s*', rule.strip())
          non_terminals.add(lhs)
          all_symbols.update(rhs.split())

      return non_terminals, all_symbols - non_terminals

#Para leer la gramatica LL1
def leer_gramatica(filename):
    with open(filename, 'r') as file:
        rules = [line.strip() for line in file if line.strip()]
    return rules

# Para leer los conjuntos de primeros
def read_firsts(filename):
    firsts = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                non_terminal, elements = line.split(':')
                elements = [e.strip() for e in elements.split(',')]
                firsts[non_terminal.strip()] = set(e if e != "''" else 'ε' for e in elements if e)
    return firsts

# Para hallar los conjuntos de primeros
def hallar_primeros(rules):
 firsts = {}
 change = True

 # Inicializar FIRST para cada no terminal y terminal
 non_terminals, terminals = identificar_terminal_noterminal(rules)
 for symbol in non_terminals.union(terminals):
    firsts[symbol] = set()
    if symbol in terminals:
        firsts[symbol].add(symbol)

 while change:
    change = False
    for rule in rules:
        lhs, rhs = rule.split('->')
        lhs = lhs.strip()
        rhs = rhs.strip().split()

        original_first = firsts[lhs].copy()
        can_be_empty = True

        for symbol in rhs:
            if not can_be_empty:
                break

            firsts[lhs].update(firsts[symbol] - {EPSILON})

            if EPSILON not in firsts[symbol]:
                can_be_empty = False

        if can_be_empty:
            firsts[lhs].add(EPSILON)

        if firsts[lhs] != original_first:
            change = True

 return firsts


# Para hallar los conjuntos de siguientes
def hallar_siguientes(rules, firsts, start_symbol):
 follows = {non_terminal: set() for non_terminal in firsts}
 follows[start_symbol].add('$') 

 changed = True
 while changed:
    changed = False
    for rule in rules:
        parts = rule.split('->')
        if len(parts) < 2:
            continue
        lhs = parts[0].strip()
        rhs = parts[1].strip().split()

        trailer = set(follows[lhs])
        for i in reversed(range(len(rhs))):
            symbol = rhs[i]
            if symbol in follows:  # Solo considerar no terminales
                before_update = len(follows[symbol])
                # Añadir trailer, excluyendo explícitamente épsilon si está presente
                follows[symbol].update(trailer)
                if len(follows[symbol]) > before_update:
                    changed = True
                # Si el símbolo puede derivar en épsilon, actualizar el trailer
                if 'ε' in firsts.get(symbol, set()):
                    trailer.update(x for x in firsts[symbol] if x != 'ε')
                else:
                    trailer = set(firsts.get(symbol, set()))
            else:
                if symbol != 'ε':
                    trailer = {symbol}

# Eliminar cualquier conjunto FOLLOW vacío
 non_empty_follows = {}
 for non_terminal, follow_set in follows.items():
    if follow_set:
        non_empty_follows[non_terminal] = follow_set

 return non_empty_follows

# Para hallar la tabla de análisis sintáctico
def leer_conjuntos(filename):
 sets = {}
 with open(filename, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            non_terminal, elements = line.split(':')
            elements = elements.split(',')
            sets[non_terminal.strip()] = set(e.strip() if e.strip() != "''" else '' for e in elements if e.strip())
 return sets

def leer_gramatica_tabla(filename):
  rules = {}
  with open(filename, 'r') as file:
      current_nt = None
      for line in file:
          line = line.strip()
          if line:
              if '->' in line:
                  lhs, rhs = line.split('->')
                  lhs, rhs = lhs.strip(), rhs.strip()
                  if lhs not in rules:
                      rules[lhs] = []
                  current_nt = lhs
                  rules[lhs].append(rhs.split())
              elif current_nt:
                  rules[current_nt].append(line.split())
  return rules

def construir_tabla(rules, firsts, follows):
 terminals = set(term for terms in firsts.values() for term in terms if term != '') | {'$'}
 non_terminals = set(rules.keys())
 table = {nt: {t: [] for t in terminals} for nt in non_terminals}

 for nt, productions in rules.items():
    for production in productions:
        first = calcular_primeros(production, firsts)
        for symbol in first - {''}:
            table[nt][symbol].append(production)
        if '' in first:
            for symbol in follows[nt]:
                table[nt][symbol].append(production)

 return table

def calcular_primeros(sequence, firsts):
 result = set()
 for symbol in sequence:
    result.update(firsts.get(symbol, {symbol}))
    if '' not in firsts.get(symbol, {}):
        result.discard('')
        break
 else:
    result.add('')
 return result

def imprimir_tabla(table, filename):
  with open(filename, 'w') as file:
      for nt, row in table.items():
          file.write(f"{nt}:\n")
          for terminal, productions in row.items():
              if productions:
                  production_str = ' | '.join(' '.join(prod) for prod in productions)
                  file.write(f"  {terminal}: {production_str}\n")

# Para escribir txt con los conjuntos de primeros y siguientes
def escribir_conjuntos(sets, filename, set_type):
 with open(filename, 'w') as file:
    for symbol in sorted(sets):
        set_formatted = ', '.join(sorted(sets[symbol]))
        file.write(f"{symbol}: {set_formatted}\n")

 print(f"Los conjuntos de {set_type} han sido creado y guardado en {filename}")

EPSILON = "''"  # Asegúrate de que EPSILON coincida con cómo lo representas en las reglas
terminals = set()

# ANALISIS 

class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def cargar_tabla(archivo):
  tabla = {}
  with open(archivo, newline='') as csvfile:
      reader = csv.reader(csvfile)
      for fila in reader:
          estado = fila[0]
          transiciones = fila[1:]
          tabla[estado] = transiciones
  return tabla

def analizar_entrada_P(entrada, tabla):
  pila = ['$', 'S']  
  idx_entrada = 0
  while len(pila) > 0:
      print("Pila:", pila)
      print("Entrada:", entrada[idx_entrada:])
      print("")

      simbolo_actual = pila.pop()
      if idx_entrada < len(entrada):
          simbolo_entrada = entrada[idx_entrada]

          if simbolo_actual in tabla:
              transiciones = tabla[simbolo_actual]
              accion = transiciones[get_index(simbolo_entrada)]

              if accion != ' -':
                  if accion != 'e':
                      produccion = accion.split()
                      pila.extend(reversed(produccion))
                  else:
                      continue
              else:
                  continue
          else:
              if simbolo_actual == simbolo_entrada:
                  idx_entrada += 1
              else:
                  return False
      else:
          return False

  return idx_entrada == len(entrada) and not pila

def analizar_entrada_A(entrada, tabla):
    raiz = Nodo('S')  
    pila = [('$', None), ('S', raiz)]  # Ahora el símbolo final '$' se pone al inicio para procesarlo al final.

    idx_entrada = 0
    while len(pila) > 0:
        simbolo_actual, nodo_actual = pila.pop()

        if idx_entrada < len(entrada):
            simbolo_entrada = entrada[idx_entrada]
        else:
            break

        if simbolo_actual in tabla:
            transiciones = tabla[simbolo_actual]
            accion = transiciones[get_index(simbolo_entrada)]

            if accion != '-':
                if accion == 'e':  # Manejo de producción épsilon
                    nodo_epsilon = Nodo('e')
                    nodo_actual.agregar_hijo(nodo_epsilon)
                else:
                    produccion = accion.split()
                    nodos_nuevos = []
                    for simbolo in produccion:
                        nuevo_nodo = Nodo(simbolo)
                        nodo_actual.agregar_hijo(nuevo_nodo)
                        nodos_nuevos.append((simbolo, nuevo_nodo))
                    pila.extend(reversed(nodos_nuevos))  # Extendemos la pila con los nuevos nodos
        else:
            if simbolo_actual == simbolo_entrada:
                idx_entrada += 1
            else:
                return False, None  

    return idx_entrada == len(entrada) and not pila, raiz


def generar_dot(nodo, buffer, id=0, parent_id=None):
    if nodo is None:
        return id

    node_name = f'node{id}'

    buffer.append(f'{node_name} [label="{nodo.simbolo}"];')

    if parent_id is not None:
        buffer.append(f'{parent_id} -> {node_name};')

    child_id = id + 1
    for hijo in nodo.hijos:
        child_id = generar_dot(hijo, buffer, child_id, node_name)

    return child_id

def exportar_arbol_a_dot(raiz):
    buffer = ['digraph G {']
    generar_dot(raiz, buffer)
    buffer.append('}')
    return '\n'.join(buffer)

def get_index(simbolo):
    indice_simbolos = {
        'T_Inicio': 0,
        'T_Fin': 1,
        'T_Funcion': 2,
        'IFD': 3,
        'T_FinFuncion': 4,
        'S_lpar': 5,
        'S_rpar': 6,
        'ID': 7,
        'S_coma': 8,
        'P_Mostrar': 9,
        'Tex': 10,
        'Num': 11,
        'S_sum': 12,
        'A_int': 13,
        'A_float': 14,
        'A_string': 15,
        'A_bool': 16,
        'Bool_True': 17,
        'Bool_False': 18,
        'S_igual': 19,
        'S_res': 20,
        'S_multi': 21,
        'S_div': 22,
        'C_Si': 23,
        'C_FinSi': 24,
        'C_SiNo': 25,
        'C_Mientras': 26,
        'C_FinMientras': 27,
        'C_Para': 28,
        'C_FinPara': 29,
        'S_mayor': 30,
        'S_menor': 31,
        'S_mayorI': 32,
        'S_menorI': 33,
        'S_igualdad': 34,
        'S_desigualdad': 35,
        'S_And': 36,
        'S_Or': 37,
        'S_ascender': 38,
        'S_descender': 39,
        'P_Leer': 40,
        'P_Retornar': 41,
        'P_Romper': 42,
        '$': 43
    }
    return indice_simbolos.get(simbolo, -1)
