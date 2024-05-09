class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size

    def push(self, item):
        if len(self.stack) < self.size:
            self.stack.append(item)

    def pop(self):
        result = -1

        if self.stack != []:
            result = self.stack.pop()

        return result

    def displayReversed(self):
        if self.stack == []:
            print("Stack is empty!")
        else:
            print("Stack data:")
            for item in reversed(self.stack):
                print(item)

    def display(self):
        if self.stack == []:
            print("Stack is empty!")
        else:
            # Print items in the same line
            print("new equation", end=" ")
            for item in self.stack:
                print(item, end=" ")

    def isEmpty(self):
        return self.stack == []

    def topChar(self):
        result = -1

        if self.stack != []:
            result = self.stack[len(self.stack) - 1]

        return result

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "Stack is empty"

    def get_index(self, item):
        if item in self.stack:
            return len(self.stack) - self.stack[::-1].index(item) - 1
        else:
            return f"{item} is not in the stack"

    def pop_at_index(self, index):
        if 0 <= index < len(self.stack):
            return self.stack.pop(index)
        else:
            return f"Invalid index or stack is empty"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Aux operations
def isOperand(c):
    return c not in operators


operators = "+-*/"


def isOperator(c):
    return c in operators


def getPrecedence(c):
    result = 0

    for char in operators:
        result += 1

        if char == c:
            if c in '-/':
                result -= 1
            break

    return result



def evaluatePostfix(infixExps, expression, queueOfOperators):
    stack = Stack(15)
    StackFullEquation = Stack(30)
    score = 0

    for char in expression:
        if isOperand(char):
            stack.push(int(char))
            StackFullEquation.push(int(char))
        elif isOperator(char):
            symbol = char
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = calculateResult(operand1, operand2, symbol)
            stack.push(result)
            StackFullEquation.push(str(symbol))

            handleUserInput(queueOfOperators, score)

            # Display the part of the equation based on the selected first operator
            part_of_equation = f"{operand1} {symbol} {operand2}"
            try:
                infixExps = list(map(lambda x: x.replace(part_of_equation, str(result)), infixExps))
                print(str(infixExps))
            except ValueError:
                print(f"{part_of_equation} not found in infixExps")

    return stack.pop()

def calculateResult(operand1, operand2, operator):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2

def handleUserInput(queueOfOperators, score):
    choice = input("enter the symbol: ")

    while queueOfOperators[0] != choice:
        score -= 10
        print("Your score decreased by 10 points.\nNew Score is: ", score)
        choice = input("Wrong answer. Please try again")

    if queueOfOperators[0] == choice:
        score += 10
        print("Correct!.\nNew Score is: ", score)
        queueOfOperators.pop(0)

# Assuming isOperand and isOperator functions are defined elsewhere

# Sample input data

infixExps = ['8 + 7 * 9 / 2 '] # List of infix expressions
expression = ['8','7','9','*','2','/','+']  # Postfix expression
queueOfOperators = ['*', '/', '+']  # Queue of expected operators

result = evaluatePostfix(infixExps, expression, queueOfOperators)
print("Final result:", result)