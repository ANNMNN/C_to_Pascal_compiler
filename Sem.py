import ply.lex as lex
import ply.yacc as yacc
from collections import OrderedDict

class Symbol:
    name: str

class SymTable:
    data: OrderedDict[str, Symbol] # важен порядок символов в таблице

    def __init__(self):
        self.data = OrderedDict()

    def Add(self, name: str):
        pass

    def Get(self, name: str) -> Symbol:
        pass

class SymTableStack:
    tables: list[SymTable]

    def __init__(self):
        self.tables = []

    def Add(self, name: str, value: Symbol):
        pass        

    def Get(self, name: str) -> Symbol:
        pass

    def push(self, table: SymTable):
        self.tables.append(table)

    def pop(self):
        self.tables.pop()

class SymType(Symbol):
    pass

class SymInteger(SymType):
    pass

class SymDouble(SymType):
    pass

class SymString(SymType):
    pass

class SymBool(SymType):
    pass

class SymArray(SymType):
    elem_type: SymType
    low: int
    hi: int
    bounds: Tuple[low, hi]  # границы

class SymRecord(SymType):
    fields: SymTable

class SymVar(Symbol):
    type_: SymType
    # value...

class SymConst(SymVar):
    pass

class SymParamVar(SymVar):
    pass

class SymProc(Symbol):
    params: SymTable
    locals: SymTable
    body: NodeBody

class SymFunc(SymProc):
    ret: SymType

class SymTypeAlias(SymType):
    original: SymType;

# Правила для лексера
tokens = (
    'IDENTIFIER',
    'INTEGER',
    'DOUBLE',
    'STRING',
    'BOOL',
    'ASSIGN',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE'
)

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'IDENTIFIER'
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'INTEGER'
    return t

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    t.type = 'DOUBLE'
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]  # убрать кавычки
    t.type = 'STRING'
    return t

def t_COMMA(t):
    r','
    t.type = 'COMMA'
    return t

def t_SEMICOLON(t):
    r';'
    t.type = 'SEMICOLON'
    return t

def t_COLON(t):
    r':'
    t.type = 'COLON'
    return t

def t_ASSIGN(t):
    r'='
    t.type = 'ASSIGN'
    return t

def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'
    return t

def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'
    return t

def t_LBRACKET(t):
    r'\['
    t.type = 'LBRACKET'
    return t

def t_RBRACKET(t):
    r'\]'
    t.type = 'RBRACKET'
    return t

def t_LBRACE(t):
    r'{'
    t.type = 'LBRACE'
    return t

def t_RBRACE(t):
    r'}'
    t.type = 'RBRACE'
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    t.type = 'BOOL'
    return t

# Обработка ошибок
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Правила для парсера
def p_statement_vardef(p):
    '''
    statement : IDENTIFIER COLON type SEMICOLON
    '''
    name = p[1]
    type_ = p[3]
    symStack[-1].Add(name, SymVar(name, type_))

def p_type(p):
    '''
    type : INTEGER
         | DOUBLE
         | STRING
         | BOOL
         | array_type
         | record_type
    '''
    pass

def p_array_type(p):
    '''
    array_type : ARRAY LBRACKET INTEGER CARDINAL RBRACKET OF type
    '''
    pass

def p_record_type(p):
    '''
    record_type : RECORD LBRACE field_list RBRACE
    '''
    pass

def p_field_list(p):
    '''
    field_list : field_declaration SEMICOLON field_list
               | field_declaration SEMICOLON
    '''
    pass

def p_field_declaration(p):
    '''
    field_declaration : IDENTIFIER COLON type
    '''
    pass

# Создание лексера и парсера
lexer = lex.lex()
parser = yacc.yacc()

# Пример использования
symStack = SymTableStack()
symStack.push(SymTable())  # builtins
symStack.push(SymTable())  # globals
symStack.push(SymTable())  # locals
code = 'x: integer;'
parser.parse(code)

class SymTable:
    data: OrderedDict[str, Symbol] # важен порядок символов в таблице

    def __init__(self):
        self.data = OrderedDict()

    def Add(self, name: str, symbol: Symbol):
        if name in self.data:
            raise ValueError(f'Symbol with name "{name}" already exists')
        self.data[name] = symbol

    def Get(self, name: str) -> Symbol:
        for table in reversed(symStack.tables):
            if name in table.data:
                return table.data[name]
        raise ValueError(f'Symbol with name "{name}" was not found')

    def p_statement_vardef(p):
        '''
        statement : IDENTIFIER COLON type SEMICOLON
        '''
        name = p[1]
        type_ = p[3]
        symStack.tables[-1].Add(name, SymVar(name, type_))

    def p_expression_identifier(p):
        '''
        expression : IDENTIFIER
        '''
        name = p[1]
        symbol = symStack.tables[0].Get(name)
        # дальнейшая обработка символа

class SymTableStack:
    tables: list[SymTable]

    def __init__(self):
        self.tables = []

    def Add(self, name: str, symbol: Symbol):
        self.tables[-1].Add(name, symbol)

    def Get(self, name: str) -> Symbol:
        for table in reversed(self.tables):
            if name in table.data:
                return table.data[name]
        raise ValueError(f'Symbol with name "{name}" was not found')

    def push(self, table: SymTable):
        self.tables.append(table)

    def pop(self):
        if len(self.tables) <= 1:
            raise ValueError('Cannot pop the last table')
        return self.tables.pop()

    def top(self) -> SymTable:
        return self.tables[-1]

    def p_statement_funcdef(p):
        '''
        statement : FUNCTION IDENTIFIER LPAREN param_list RPAREN COLON type block
        '''
        name = p[2]
        params = p[4]
        ret_type = p[6]
        code = p[7]

        symStack.push(SymTable())  # локальная таблица символов
        for param in params:
            symStack.Add(param.name, param)
        # и т.д.

        symStack.pop()
        symStack.top().Add(name, SymFunc(name, params, ret_type, code))

    def p_param_list(p):
        '''
        param_list : param_decl COMMA param_list
                   | param_decl
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[3].insert(0, p[1])
            p[0] = p[3]

    def p_param_decl(p):
        '''
        param_decl : IDENTIFIER COLON type
        '''
        p[0] = SymParamVar(p[1], p[3])

    def p_param_ident(p):
        '''
        param_ident : IDENTIFIER
        '''
        p[0] = symStack.top().Get(p[1])

    def p_expression_call(p):
        '''
        expression : IDENTIFIER LPAREN arg_list RPAREN
        '''
        name = p[1]
        args = p[3]

        func_sym = symStack.Get(name)
        if not isinstance(func_sym, SymFunc):
            raise ValueError(f'Symbol "{name}" is not a function')
        if len(args) != len(func_sym.params):
            raise ValueError(f'Incorrect number of arguments for function "{name}"')

    # В данном месте мы знаем, что функция существует и число аргументов верное
    # Можно создать новую таблицу символов для локальных переменных
    symStack.push(SymTable())
    for param_sym, arg_node in zip(func_sym.params, args):
        symStack.Add(param_sym.name, SymVar(param_sym.name, param_sym.type_, arg_node))

    # Обрабатываем код функции
    result = func_sym.body.eval()

    # Возвращаемся к предыдущей таблице символов
    symStack.pop()

    p[0] = result

    def p_arg_list(p):
        '''
        arg_list : expression COMMA arg_list
                 | expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[3].insert(0, p[1])
            p[0] = p[3]

    x = 5
    y = 3

    def inc(n: integer) -> integer:
        return n + 1

    z = inc(x)
    print(z)