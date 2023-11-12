'''class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        import re
        regex_patterns = {
        'INTEGER': r'\b[0-9]+\b',
        'PLUS': r'\+',
        'MINUS': r'-',
        'MULTIPLY': r'\*',
        'DIVIDE': r'/',
        'LPAREN': r'\(',
        'RPAREN': r'\)',
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
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def error(self):
        raise Exception('Invalid syntax')

    def factor(self):
        token = self.current_token

        if token['type'] == 'INTEGER':
            self.next_token()
            return int(token['value'])
        elif token['type'] == 'LPAREN':
            self.next_token()
            result = self.expr()
        if self.current_token['type'] == 'RPAREN':
            self.next_token()
            return result

    def term(self):
        result = self.factor()

        while self.current_token is not None and self.current_token['type'] in ('MULTIPLY', 'DIVIDE'):
            token = self.current_token
            self.next_token()
            if token['type'] == 'MULTIPLY':
                result *= self.factor()
            elif token['type'] == 'DIVIDE':
                result /= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token is not None and self.current_token['type'] in ('PLUS', 'MINUS'):
            token = self.current_token
            self.next_token()
            if token['type'] == 'PLUS':
                result += self.term()
            elif token['type'] == 'MINUS':
                result -= self.term()

        return result

    def parse(self):
        return self.expr()

def main():
    with open('file.cpp', 'r') as file:
        code = file.read()

    tokens = Tokenizer(code).tokenize()
    parser = Parser(tokens)
    result = parser.parse()

    print('Result:', result)

if __name__ == "__main__":
    main()

'''

import re


class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        regex_patterns = {
            'INTEGER': r'\b[0-9]+\b',
            'PLUS': r'\+',
            'MINUS': r'-',
            'MULTIPLY': r'\*',
            'DIVIDE': r'/',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
        }
        token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in regex_patterns.items()))

        for match in token_regex.finditer(self.code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            self.tokens.append({'type': token_type, 'value': token_value})

        #print(self.tokens)
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def error(self):
        raise Exception('Invalid syntax')

    def factor(self):
        token = self.current_token

        if token['type'] == 'INTEGER':
            self.next_token()
            return {'type': 'INTEGER', 'value': int(token['value'])}
        elif token['type'] == 'LPAREN':
            self.next_token()
            result = self.expr()

            if self.current_token is None or self.current_token['type'] != 'RPAREN':
                self.error()

            self.next_token()
            return result
        else:
            self.error()

    def term(self):
        result = self.factor()

        while self.current_token is not None and self.current_token['type'] in ('MULTIPLY', 'DIVIDE'):
            token = self.current_token
            self.next_token()

            if token['type'] == 'MULTIPLY':
                result = {'type': 'MULTIPLY', 'left': result, 'right': self.factor()}
            elif token['type'] == 'DIVIDE':
                result = {'type': 'DIVIDE', 'left': result, 'right': self.factor()}

        return result

    def expr(self):
        result = self.term()

        while self.current_token is not None and self.current_token['type'] in ('PLUS', 'MINUS'):
            token = self.current_token
            self.next_token()

            if token['type'] == 'PLUS':
                result = {'type': 'PLUS', 'left': result, 'right': self.term()}
            elif token['type'] == 'MINUS':
                result = {'type': 'MINUS', 'left': result, 'right': self.term()}

        return result

    def parse(self):
        return self.expr()

def main():
        with open('file.cpp', 'r') as file:
            code = file.read()

        tokens = Tokenizer(code).tokenize()
        parser = Parser(tokens)
        result = parser.parse()

        print('Result:', result)


if __name__ == "__main__":
    main()


