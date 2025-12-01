

if __name__ == "__main__":
    pass # Ваш код здес
"""3 лаба. Рекусрсивное вычисление выражения."""

class ExpressionCalculator:
    def __init__(self):
        self.journal = []
        self.pos = 0

    def calculate(self, expression):
        self.journal = []
        self.pos = 0
        expression = expression.replace(" ", "")
        result = self.parse_expression(expression)
        return result, self.journal

    def log_action(self, action, result):
        self.journal.append(f"{action} = {result}")

    def parse_expression(self, expr):
        result = self.parse_term(expr)
        while self.pos < len(expr) and expr[self.pos] in ['+', '-']:
            op = expr[self.pos]
            self.pos += 1
            left_result = result
            right = self.parse_term(expr)
            if op == '+':
                result = left_result + right
            else:
                result = left_result - right
            self.log_action(f"{left_result} {op} {right}", result)
        return result

    def parse_term(self, expr):
        result = self.parse_factor(expr)
        while self.pos < len(expr) and expr[self.pos] in ['*', '/']:
            op = expr[self.pos]
            self.pos += 1
            left_result = result
            right = self.parse_factor(expr)
            if op == '*':
                result = left_result * right
                self.log_action(f"{left_result} * {right}", result)
            else:
                result = left_result / right
                self.log_action(f"{left_result} / {right}", result)
        return result

    def parse_factor(self, expr):
        if self.pos < len(expr) and expr[self.pos] == '(':
            self.pos += 1
            result = self.parse_expression(expr)
            if self.pos >= len(expr) or expr[self.pos] != ')':
                raise ValueError("Незакрытая скобка")
            self.pos += 1  
        else:
            start_pos = self.pos
            while self.pos < len(expr) and (expr[self.pos].isdigit() or expr[self.pos] == '.'):
                self.pos += 1
            if start_pos == self.pos:
                raise ValueError("Ожидалось число или выражение в скобках")
            number_str = expr[start_pos:self.pos]
            result = float(number_str) if '.' in number_str else int(number_str)
        return result


calculator = ExpressionCalculator()
task = input('Введите математическое выражение: ')
result, journal = calculator.calculate(task)
print("Журнал действий:")
for i, action in enumerate(journal, 1):
    print(f"{i}. {action}")
print(f"Финальный результат: {result}")
