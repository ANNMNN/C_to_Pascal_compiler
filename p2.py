class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        import re
        regex_patterns = {
            'INTEGER': r'int',
            'PLUS': r'\+',
            'MINUS': r'-',
            'MUL': r'\*',
            'DIV': r'/',
            'LPAREN': r'\(',
            'RPAREN': r'\)',

            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'SEMICOLON': r';',
            'COUT': r'cout',
            'LEFTSHIFT': r'<<',
            'RIGHTSHIFT': r'>>',
            'STRING': r'\".*?\"',
            'NUMBER': r'[0-9]+',
            'EQUALS': r'=',
            'COMMA': r',',
            'LEFTCURLY': r'{',
            'RIGHTCURLY': r'}',
            'RETURN': r'return',
        }

        token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in regex_patterns.items()))

        for match in token_regex.finditer(self.code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            self.tokens.append({'type': token_type, 'value': token_value})

        print(self.tokens)
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = None
        if len(tokens) == 0:
            self.error()

    def function(self, function_name):
        args = []
        self.match('IDENTIFIER')
        result = None
        if self.current_token is not None:
            print('current_token:', self.current_token)
            if self.current_token['type'] == 'NUMBER':
                result = int(self.current_token['value'])
                self.match('NUMBER')
            elif self.current_token['type'] == 'LPAREN':
                result = self.expr()
                self.match('RPAREN')
            elif self.current_token['type'] == 'LEFTCURLY':
                result = self.expr()
                self.match('RIGHTCURLY')
            elif self.current_token['type'] in ('PLUS', 'MINUS', 'COMMA'):
                return result

        while self.current_token is not None and self.current_token['type'] in ('MUL', 'DIV', 'PLUS', 'MINUS'):
            token = self.current_token
            if token['type'] == 'MUL':
                self.match('MUL')
                result *= self.factor()
            elif token['type'] == 'DIV':
                self.match('DIV')
                result /= self.factor()
            elif token['type'] == 'PLUS':
                self.match('PLUS')
                result += self.term()
            elif token['type'] == 'MINUS':
                self.match('MINUS')
                result -= self.term()
            elif token['type'] == 'COMMA':
                self.match('COMMA')
                continue

        return result


    def parse(self):
        self.current_token = self.tokens[self.token_index]
        result = self.expr()
        if self.current_token is not None:
            self.error()
        return result

    def match(self, tok_type):
        if self.current_token['type'] == tok_type:
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]

    def error(self):
        return Exception('Invalid syntax')

    def expr(self):
        result = self.term()

        while self.current_token is not None and self.current_token['type'] in ('PLUS', 'MINUS'):
            token = self.current_token
            if token['type'] == 'PLUS':
                self.match('PLUS')
                result = result + self.term()
            elif token['type'] == 'MINUS':
                self.match('MINUS')
                result = result - self.term()

        return result

    def expr(self):
        result = self.term()

        while self.current_token is not None and self.current_token['type'] in ('PLUS', 'MINUS'):
            token = self.current_token
            if token['type'] == 'PLUS':
                self.match('PLUS')
                result = result + self.term()
            elif token['type'] == 'MINUS':
                self.match('MINUS')
                result = result - self.term()

        return result

    def factor(self):
        result = None
        if self.current_token is not None:
            print('current_token:', self.current_token)
            if self.current_token['type'] == 'NUMBER':
                result = int(self.current_token['value'])
                self.match('NUMBER')
            elif self.current_token['type'] == 'LPAREN':
                self.match('LPAREN')
                result = self.expr()
                self.match('RPAREN')
            elif self.current_token['type'] == 'LEFTCURLY':
                self.match('LEFTCURLY')
                result = self.expr()
                self.match('RIGHTCURLY')
            elif self.current_token['type'] == 'IDENTIFIER':
                variable_name = self.current_token['value']
                self.match('IDENTIFIER')
                if self.current_token is not None and self.current_token['type'] == 'LPAREN':
                    result = self.function(variable_name)
                else:
                    result = variable_name
            else:
                self.error()
        else:
            self.error()

        if self.current_token is not None and self.current_token['type'] not in (
                'MUL', 'DIV', 'PLUS', 'MINUS', 'COMMA'):
            return result

        while self.current_token is not None and self.current_token['type'] in ('MUL', 'DIV', 'PLUS', 'MINUS'):
            token = self.current_token
            if token['type'] == 'MUL':
                self.match('MUL')
                result *= self.factor()
            elif token['type'] == 'DIV':
                self.match('DIV')
                result /= self.factor()
            elif token['type'] == 'PLUS':
                self.match('PLUS')
                result += self.term()
            elif token['type'] == 'MINUS':
                self.match('MINUS')
                result -= self.term()
            elif token['type'] == 'COMMA':
                self.match('COMMA')
                continue

        return result

    def term(self):
        result = self.factor()

        while self.current_token is not None and self.current_token['type'] in ('MUL', 'DIV', 'PLUS', 'MINUS'):
            token = self.current_token
            if token['type'] == 'MUL':
                self.match('MUL')
                result = result * self.factor()
            elif token['type'] == 'DIV':
                self.match('DIV')
                result = result / self.factor()
            elif token['type'] == 'PLUS':
                self.match('PLUS')
                result = result + self.term()
            elif token['type'] == 'MINUS':
                self.match('MINUS')
                result = result - self.term()

        return result

def print_tree(node, level=0):
    indent = '  ' * level
    if node is None:
        return

    print(indent + node.type)
    for child in node.children:
        print_tree(child, level+1)


def main():
    with open('file.cpp', 'r') as file:
        code = file.read()

    tokens = Tokenizer(code).tokenize()
    parser = Parser(tokens)
    result = parser.parse()

    print('Result:', result)
if __name__ == "__main__":
    main()