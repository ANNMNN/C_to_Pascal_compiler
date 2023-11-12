import ply.lex as lex

tokens = (
    'INTEGER',
    'REAL',
    'CONST',
    'BOOLEAN',
    'CHAR',
    'VOID',
    'COMMENT',
    'STRING',
    'CLASSFUNCTION',
    'ARRAYINDEX',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'FOR',
    'DO',
    'COUT',
    'CIN',
    'EQUALS',
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MOD',
    'ASSIGN',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'DOUBLECOLON',
    'COLON',
    'LEFTCURLY',
    'RIGHTCURLY',
    'LEFTSQUARE',
    'RIGHTSQUARE',
    'AND',
    'OR',
    'NOT',
    'LEFTPOINTER',
    'RIGHTPOINTER'
)

# Регулярные выражения для токенов
t_INTEGER = r'integer'
t_REAL = r'real'
t_CONST = r'const'
t_BOOLEAN = r'boolean'
t_CHAR = r'char'
t_VOID = r'void'
t_COMMENT = r'\#.*'
t_STRING = r'("[a-zA-Z_][a-zA-Z0-9_]*")|(\'[a-zA-Z_][a-zA-Z0-9_]*\')'
t_CLASSFUNCTION = r'[a-zA-Z_][a-zA-Z_0-9]+[.][a-zA-Z_][a-zA-Z_0-9]+'
t_ARRAYINDEX = r'\[[a-zA-Z_][a-zA-Z0-9_]*\]'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_WHILE = r'while'
t_FOR = r'for'
t_DO = r'do'
t_COUT = r'cout'
t_CIN = r'cin'
t_EQUALS = r'=='
t_IDENTIFIER = r'[a-zA-Z_~][a-zA-Z0-9_]*'
t_NUMBER = r'[0-9]+'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MOD = r'\%'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOUBLECOLON = r'::'
t_COLON = r':'
t_LEFTCURLY = r'{'
t_RIGHTCURLY = r'}'
t_LEFTSQUARE = r'\['
t_RIGHTSQUARE = r'\]'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LEFTPOINTER = r'«'
t_RIGHTPOINTER = r'»'

# Пропуск пробелов и табуляций
t_ignore = ' \t'

# Номер строки
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Обработка ошибки
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Создание лексера
lexer = lex.lex()

def main():
    with open('file.cpp', 'r') as file:
        code = file.read()
    try:
        lexer.input(code)
        while True:
            token = lexer.token()
            if not token:
                break
            print(token)
    except ValueError as e:
        print('Error:', str(e))
        return
    print('Parsed successfully!')

main()


