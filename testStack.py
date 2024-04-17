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


    # def peek(self):
    #     top_value = -19999
    #     if not self.is_empty():
    #         top_value = self.peek_helper(self.top)
    #     return top_value

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

    # def peek_helper(self, top):
    #     return top.get_data()
    #
    # def AnoterPeek(self, position):
    #     if not self.is_empty() and position <= len(self.stack):
    #         return self.stack[-position]  # Access element at index len(stack) - position
    #     else:
    #         return "Invalid position or stack is empty"
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# infix to postfix
def toPostfix(expression):
    result = ""

    stack = Stack(15)

    for char in expression.split(" "):
        if isOperand(char):
            result += char
        elif isOperator(char):
            while True:
                topChar = stack.topChar()

                if stack.isEmpty():
                    stack.push(char)
                    break
                else:
                    pC = getPrecedence(char)
                    pTC = getPrecedence(topChar)

                    if pC > pTC:
                        stack.push(char)
                        break
                    else:
                        result += stack.pop()

    while not stack.isEmpty():
        cpop = stack.pop()
        result += cpop

    return result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Evaluate postfix expression
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

            # ERROR HERE
            operand4 = StackFullEquation.pop()
            if StackFullEquation.peek() in "+-/*":
                index = StackFullEquation.get_index(StackFullEquation.peek())
                operand3= StackFullEquation.pop_at_index(index)
            else:
                operand3= StackFullEquation.pop()

            # here

            result = 0
            result2 = 0
            if char == '+':
                result = operand1 + operand2
                result2 = operand3 + operand4
            elif char == '-':
                result = operand1 - operand2
                result2 = operand3 - operand4
            elif char == '*':
                result = operand1 * operand2
                result2 = operand3 * operand4
            elif char == '/':
                result = operand1 / operand2
                result2 = operand3 / operand4

            stack.push(result)
            StackFullEquation.push(str(symbol))

            StackFullEquation.push(result2)

            # Comparing:  multiple choice
            choice = input("enter the symbol: ")
            #
            # answer= choice == symbol
            # print(answer)

            while queueOfOperators[0] != choice:
                score -= 10
                print("Your score decrease 10 score\nNew Score is: ", score)
                choice = input("Wrong answer. Please try again")

            if queueOfOperators[0] == choice:
                score += 10
                print("Your score is: ", score)
                queueOfOperators.pop(0)
                StackFullEquation.display()
                #print(infixExps)

    return stack.pop()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# test
infixExps = ['8 + 7 * 9 / 2']

for exp in infixExps:
    postfix = toPostfix(exp)
    print(f'Infix: {exp} -> Postfix: {postfix}')


    queueOperator = []  # Create an empty list

    for char in postfix:
        if isOperator(char):
            queueOperator.append(char)
    print(queueOperator)



    result = evaluatePostfix(infixExps,postfix, queueOperator)
    print(f'\nResult: {result}')
