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

            result = 0
            if char == '+':
                result = operand1 + operand2
            elif char == '-':
                result = operand1 - operand2
            elif char == '*':
                result = operand1 * operand2
            elif char == '/':
                result = operand1 / operand2

            stack.push(result)
            StackFullEquation.push(str(symbol))


            # Comparing:  multiple choice
            choice = input("enter the symbol: ")


            while queueOfOperators[0] != choice:
                score -= 10
                print("Your score decrease 10 score\nNew Score is: ", score)
                choice = input("Wrong answer. Please try again")

            if queueOfOperators[0] == choice:
                score += 10
                print("Your score is: ", score)
                queueOfOperators.pop(0)


                # Display the part of the equation based on the selected first operator
                part_of_equation = f"{operand1} {symbol} {operand2}"

                # Replace all occurrences of 'a' with 'e' in the string
                # Find the index of part_of_equation in infixExps
                try:
                    infixExps = list(map(lambda x: x.replace(part_of_equation, str(result)), infixExps))

                    print(str(infixExps))

                except ValueError:
                    # Handle the case where part_of_equation is not found in infixExps
                    print(f"{part_of_equation} not found in infixExps")

    return stack.pop()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Detect equation from image by AI
import cv2
import pytesseract
import numpy as np
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia CPIT380\project\app\tesseract.exe"

# Open the image file
image_path = r"C:\Users\Afnan\PycharmProjects\cpit380\EQUATION2.png"
img = cv2.imread(image_path)

# Convert the image to a NumPy array and change color space
img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Save the image using OpenCV
cv2.imwrite("images/removed_noise.jpg", img_array)

# Convert the image to text using PyTesseract
text = pytesseract.image_to_string(img_array)


# def fix_equation(equation):
#     # Use regular expression to find patterns like 'number('
#     pattern = re.compile(r'(\d+)\(')
#     fixed_equation = re.sub(pattern, r'\1*(', equation)
#     return fixed_equation
#
# # Example usage
# fixed_equation = fix_equation(text)

# Print the extracted text
print("Equation is : ", text)

# # Handel with Exception or Display the output
# try:
#     result = eval(text)
#     print("Result:", result)
# except Exception as e:
#     print("Error:", e, "\nPlease try again")

# Initialize an empty list to store the spaced-out text
spaced_text = []

# Iterate through the characters of the text
for char in text:
    # Check if the character is a digit or an operator
    if char.isdigit() or char in "+-*/":
        # Add the character and a space to the spaced_text list
        spaced_text.append(char)
        spaced_text.append(" ")
    else:
        # Add the character as is to the spaced_text list
        spaced_text.append(char)

# Convert the list to a string
spaced_text_str = "".join(spaced_text)

text_without_final_space = spaced_text_str[:-1]
print(text_without_final_space)  # Output: "2 * 3 + 5 - 2 * 10 / 4 "

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# test
infixExps = [text_without_final_space]

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
    exit()
