import ply.lex as lex

# Lista de Tokens
tokens = (
    # Inicio y Fin
    'T_Inicio',
    'T_Fin',
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
    'C_Mostrar',
    'C_SaltoLinea',
    'P_Leer',
    'P_Retornar',
    'P_Romper',
    # Simbolos y Signos
    'Sig_LParen',
    'Sig_RParen',
    'C_And',
    'C_Or',
    'C_coma',
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
    # Textos
    'Tex',
    # Variables y Funciones (ID)
    'ID',
)

# Expresiones regulares
# Tokens prioritarios
def t_T_Inicio(t):
  r'Inicio'
  return t

def t_T_Fin(t):
  r'Fin'
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

def t_C_Mostrar(t):
  r'Mostrar'
  return t

def t_C_SaltoLinea(t):
  r'SaltoLinea'
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

# Numeros
def t_Num(t):
  r'\d+(\.\d+)?'
  if '.' in t.value:
      t.value = float(t.value)
  else:
      t.value = int(t.value)
  return t

# Tokens con expresiones regulares más simples
t_ignore = ' \t'

# Simbolos y Signos
t_Sig_LParen = r'\('
t_Sig_RParen = r'\)'
t_C_And = r'&&'
t_C_Or = r'\|\|'
t_C_coma = r','
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

# Leer el contenido del archivo
with open('Codigo 1.txt', 'r') as file:
  data = file.read()

# Darle la entrada al lexer
lexer.input(data)

# Lista para almacenar los tokens como diccionarios
tokens_list = []

# Tokenize
while True:
  tok = lexer.token()
  if not tok:
    break  # No hay más entrada
  # Crear un diccionario para cada token
  token_info = {
    'type': tok.type,
    'value': tok.value,
    'line': tok.lineno,
    'position': tok.lexpos
  }
  tokens_list.append(token_info)

# Imprimir la lista de tokens como diccionarios
for token in tokens_list:
  print(token)
