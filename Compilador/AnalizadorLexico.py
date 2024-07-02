import ply.lex as lex

# ANALIZADOR LEXICO
# Lista de Tokens
tokens = (
    # Inicio y Fin
    'T_Inicio',
    'T_Fin',
    'T_Funcion',
    'T_FinFuncion',
    # Atributos
    'A_int',
    'A_float',
    'A_bool',
    'A_string',
    # Numeros
    'Num',
    # Valores de Bool
    'Bool_True',
    'Bool_False',
    # Controladores / Palabras Clave
    'C_Si',
    'C_SiNo',
    'C_FinSi',
    'C_Para',
    'C_FinPara',
    'C_Mientras',
    'C_FinMientras',
    'P_Mostrar',
    'C_SaltoLinea',
    'P_Leer',
    'P_Retornar',
    'P_Romper',
    # Simbolos y Signos
    'S_lpar',
    'S_rpar',
    'S_And',
    'S_Or',
    'S_coma',
    'S_sum',
    'S_res',
    'S_multi',
    'S_div',
    'S_igual',
    'S_mayor',
    'S_menor',
    'S_mayorI',
    'S_menorI',
    'S_igualdad',
    'S_desigualdad',
    'S_ascender',
    'S_descender',
    # Textos
    'Tex',
    # Variables y Funciones (ID)
    'ID',
    'IFD',
)

# Expresiones regulares
# Tokens prioritarios
def t_T_Inicio(t):
  r'Inicio'
  return t

def t_T_Fin(t):
  r'Fin'
  return t

def t_T_Funcion(t):
  r'Funcion'
  return t

def t_T_FinFuncion(t):
  r'FFuncion'
  return t

def t_A_int(t):
  r'int'
  return t

def t_A_float(t):
  r'float'
  return t

def t_A_bool(t):
  r'bool'
  return t

def t_Bool_True(t):
  r'True'
  return t

def t_Bool_False(t):
  r'False'
  return t

def t_A_string(t):
  r'string'
  return t

def t_C_Si(t):
  r'Si'
  return t

def t_C_SiNo(t):
  r'SN'
  return t

def t_C_FinSi(t):
  r'FSi'
  return t

def t_C_Para(t):
  r'Para'
  return t

def t_C_FinPara(t):
  r'FPara'
  return t

def t_C_Mientras(t):
  r'Mientras'
  return t

def t_C_FinMientras(t):
  r'FMientras'
  return t

def t_P_Mostrar(t):
  r'Mostrar'
  return t

def t_C_SaltoLinea(t):
  r'S'
  return t

def t_P_Leer(t):
  r'Leer'
  return t

def t_P_Retornar(t):
  r'Retornar'
  return t

def t_P_Romper(t):
  r'Romper'
  return t

# Textos
def t_Tex(t):
    r'("[a-zA-Z0-9 ]*")'
    return t

# Variables y Funciones
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t
def t_IFD(t):
    r'_[a-zA-Z][a-zA-Z0-9]*_'
    return t

# Numeros
def t_Num(t):
  r'(-)?\d+(\.\d+)?'
  if '.' in t.value:
      t.value = float(t.value)
  else:
      t.value = int(t.value)
  return t

def t_S_ascender(t):
  r'::'
  return t

def t_S_descender(t):
  r':'
  return t

# Tokens con expresiones regulares más simples
t_ignore = ' \t'

# Simbolos y Signos
t_S_lpar = r'\('
t_S_rpar = r'\)'
t_S_And = r'&&'
t_S_Or = r'\|\|'
t_S_coma = r','
t_S_sum = r'\+'
t_S_res = r'-'
t_S_multi = r'\*'
t_S_div = r'/'
t_S_igual = r'='
t_S_mayor = r'<'
t_S_menor = r'>'
t_S_mayorI = r'<='
t_S_menorI = r'>='
t_S_igualdad = r'=='
t_S_desigualdad = r'<>'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def analizar_entrada(data):
  lexer.input(data)
  tokens_list = []
  while True:
      tok = lexer.token()
      if not tok:
          break
      token_info = {
          'type': tok.type,
          'value': tok.value,
          'line': tok.lineno,
          'position': tok.lexpos
      }
      tokens_list.append(token_info)
  return tokens_list
