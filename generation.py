class CppToPascalConverter:
    def __init__(self, cpp_code):
        self.cpp_code = cpp_code
        self.pascal_code = ""
        self.current_state = "start"

    def convert(self):
        for char in self.cpp_code:
            self.process_char(char)

        return self.pascal_code

    def process_char(self, char):
        if self.current_state == "start":
            if char.isalpha():  # Начало идентификатора
                self.current_state = "identifier"
                self.pascal_code += char

        elif self.current_state == "identifier":
            if char == "<":
                self.current_state = "less_than"
                self.pascal_code += "array of"
            elif char.isalpha() or char.isdigit() or char == "_":
                self.pascal_code += char
            elif char == ":":  # Достигнут оператор присваивания
                self.current_state = "assignment"
                self.pascal_code += ":="
            elif char == ")":  # Закрывающая скобка
                self.current_state = "start"
                self.pascal_code += ";"
            else:
                self.current_state = "start"
                self.pascal_code += char

        elif self.current_state == "less_than":
            if char == "<":
                self.current_state = "start"
                self.pascal_code += char
            else:
                self.current_state = "start"
                self.pascal_code += char

        elif self.current_state == "assignment":
            if char == "=":
                self.current_state = "start"
                self.pascal_code += char
            else:
                self.current_state = "start"
                self.pascal_code += char


# Пример использования CppToPascalConverter

cpp_code = """

int main() {
    int x = 10;
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
"""

converter = CppToPascalConverter(cpp_code)
pascal_code = converter.convert()
print(pascal_code)