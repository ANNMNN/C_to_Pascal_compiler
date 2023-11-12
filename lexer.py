class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.last_token_type = ''
        self.last_token = ''
        self.tokens = []
        self.line_number = 1

    def tokenize(self):
        import re
        regex_patterns = {
            'INTEGER': r'integer',
            'REAL': r'real',
            'CONST': r'const',
            'BOOLEAN': r'boolean',
            'CHAR': r'char',
            'VOID': r'void',
            'COMMENT': r'\#[a-zA-Z0-9_ ]*',
            'STRING': r'(\"[a-zA-Z_][a-zA-Z0-9_]*\")|(\'[a-zA-Z_][a-zA-Z0-9_]*\')',
            'CLASSFUNCTION': r'[a-zA-Z_][a-zA-Z_0-9]+[.][a-zA-Z_][a-zA-Z_0-9]+',
            'ARRAYINDEX': r'\[[a-zA-Z_][a-zA-Z0-9_]*\]',
            'IF': r'if',
            'THEN': r'then',
            'ELSE': r'else',
            'WHILE': r'while',
            'FOR': r'for',
            'DO': r'do',
            'COUT': r'cout',
            'CIN': r'cin',
            'EQUALS': r'==',
            ####
            'IDENTIFIER': r'[a-zA-Z_~][a-zA-Z0-9_]*',
            'NUMBER': r'[0-9]+',
            'PLUS': r'\+',
            'MINUS': r'\-',
            'MULTIPLY': r'\*',
            'DIVIDE': r'\/',
            'MOD': r'\%',
            'ASSIGN': r'=',
            'SEMICOLON': r';',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
            'COMMA': r',',
            'DOUBLECOLON': '::',
            'COLON': r':',
            'LEFTCURLY': r'{',
            'RIGHTCURLY': r'}',
            'LEFTSQUARE': r'\[',
            'RIGHTSQUARE': r'\]',
            'AND': r'&&',
            'OR': r'\|\|',
            'NOT': r'!',
            'LEFTPOINTER': r'«',
            'RIGHTPOINTER': r'»',
        }

        token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in regex_patterns.items()))

        KEY_WORDS = ['BOOLEAN', 'CASE', 'CHAR', 'CONST',
                     'DO', 'ELSE', 'FILE', 'FOR', 'IF',
                     'IN', 'INTEGER', 'REAL', 'CLASS', 'SET', 'THEN',
                     'TYPE', 'WHILE', 'VOID']

        for match in token_regex.finditer(self.code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type == 'IDENTIFIER':
                if self.last_token_type == 'NUMBER':
                    raise ValueError(
                        f'SyntaxError: Invalid variable name "{self.last_token + token_value}" on line {self.line_number}')
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', token_value):
                    raise ValueError(f'SyntaxError: Invalid variable name "{token_value}" on line {self.line_number}')
            elif token_type == 'NUMBER':
                try:
                    int_value = int(token_value)
                except ValueError:
                    raise ValueError(f'SyntaxError: Invalid number "{token_value}" on line {self.line_number}')
                if not -32768 <= int_value <= 32767:
                    raise ValueError(f'ValueError: Integer overflow "{token_value}" on line {self.line_number}')
            elif ((token_type == 'SEMICOLON') or (token_type == 'LEFTCURLY') or (token_type == 'RIGHTCURLY')):
                self.line_number += 1
            self.tokens.append((token_type, token_value, self.line_number))
            self.last_token_type = token_type
            self.last_token = token_value
        return self.tokens

    def get_next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        return None


def main():
    with open('file.cpp', 'r') as file:
        code = file.read()

    try:
        tokens = Tokenizer(code).tokenize()
        for token in tokens:
            print(token)
    except ValueError as e:
        print('Error:', str(e))
    return

    print('Parsed successfully!')

main()

