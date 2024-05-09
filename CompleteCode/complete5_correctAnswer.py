import tkinter as tk
from PIL import ImageTk, Image
import cv2
import pytesseract
import numpy as np

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

    def isEmpty(self):
        return self.stack == []

    def topChar(self):
        result = -1

        if self.stack != []:
            result = self.stack[len(self.stack) - 1]

        return result

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

def toPostfix(expression):
    result = ""
    stack = Stack(15)

    for char in expression.split(" "):
        if isOperand(char):
            result += char
        elif isOperator(char):
            while (not stack.isEmpty()) and (getPrecedence(stack.topChar()) >= getPrecedence(char)):
                result += stack.pop()
            stack.push(char)

    while not stack.isEmpty():
        result += stack.pop()

    return result

def generateEquation():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia_CPIT380\project\app\tesseract.exe"

    # Open the image file
    image_path = r"C:\Users\Afnan\PycharmProjects\CPIT380project\images\EQUATION2.png"
    img = cv2.imread(image_path)
    img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    cv2.imwrite("images/removed_noise.jpg", img_array)
    text = pytesseract.image_to_string(img_array)
    spaced_text = []

    for char in text:
        if char.isdigit() or char in "+-*/":
            spaced_text.append(char)
            spaced_text.append(" ")
        else:
            spaced_text.append(char)

    spaced_text_str = "".join(spaced_text)
    text_without_final_space = spaced_text_str[:-1]
    return text_without_final_space

def check_answer(answer, queueOperator, score_value, wrong_answers):
    precedence_order = {'+': 1, '-': 1, '*': 2, '/': 2}
    max_precedence = max(queueOperator, key=lambda x: (precedence_order[x], -queueOperator.index(x)))
    if answer == max_precedence:
        update_score(score_value + 10)
        return "Correct!"
    else:
        wrong_answers += 1
        update_score(score_value - (10 * wrong_answers))
        return "Wrong answer! Try again."

def evaluatePostfix(expression, queueOfOperators):
    stack = Stack(15)
    result = 0

    for char in expression:
        if isOperand(char):
            stack.push(int(char))
        elif isOperator(char):
            operand2 = stack.pop()
            operand1 = stack.pop()

            if char == '+':
                result = operand1 + operand2
            elif char == '-':
                result = operand1 - operand2
            elif char == '*':
                result = operand1 * operand2
            elif char == '/':
                result = operand1 / operand2

            stack.push(result)

    return stack.pop()

def update_result_label(result, expression, wrong_answers):
    if result == "Correct!":
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

                part_of_equation = f"{operand1} {symbol} {operand2}"

                equation_label.config(text=part_of_equation)

                infixExp = part_of_equation

                postfixExp = toPostfix(infixExp)
                queueOperator = [char for char in postfixExp if isOperator(char)]
                clear_result_label()
            else:
                result_label.config(text=result, fg="red")

def update_score(new_score):
    global score_value
    score_value = new_score
    score_label.config(text=f"Score: {score_value}")

def calculateResult(operand1, operand2, operator):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2

def clear_result_label():
    result_label.config(text="")

def checkSelectedAnswer(images_frame, image_plus, image_minus, image_multiply, image_divide, queueOperator, expression, score_value, wrong_answers):
    plus_button = tk.Button(images_frame, image=image_plus, command=lambda: update_result_label(check_answer("+", queueOperator, score_value, wrong_answers), expression, wrong_answers))
    plus_button.pack(side=tk.LEFT, padx=5)

    minus_button = tk.Button(images_frame, image=image_minus, command=lambda: update_result_label(check_answer("-", queueOperator, score_value, wrong_answers), expression, wrong_answers))
    minus_button.pack(side=tk.LEFT, padx=5)

    multiply_button = tk.Button(images_frame, image=image_multiply, command=lambda: update_result_label(check_answer("*", queueOperator, score_value, wrong_answers), expression, wrong_answers))
    multiply_button.pack(side=tk.LEFT, padx=5)

    divide_button = tk.Button(images_frame, image=image_divide, command=lambda: update_result_label(check_answer("/", queueOperator, score_value, wrong_answers), expression, wrong_answers))
    divide_button.pack(side=tk.LEFT, padx=5)



window = tk.Tk()
window.title("Equation Game")
window.geometry("300x280")
window.resizable(False, False)

bg_image = ImageTk.PhotoImage(Image.open("bbg.jpg"))
background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

score_value = 0
wrong_answers = 0

score_label = tk.Label(window, text=f"Score: {score_value}", font=("Arial", 14))
score_label.pack(padx=10, pady=10, anchor=tk.NW)

equation_label = tk.Label(window, text="", font=("Helvetica", 20, "bold"))
equation_label.pack(padx=10, pady=10)

answer_label = tk.Label(window, text="What is the correct answer?", font=("Arial", 14))
answer_label.pack(padx=10, pady=10)

images_frame = tk.Frame(window)
images_frame.pack(padx=10, pady=10, fill=tk.X)

image_plus = ImageTk.PhotoImage(Image.open("addition.png").resize((50, 50)))
image_minus = ImageTk.PhotoImage(Image.open("substract.png").resize((50, 50)))
image_multiply = ImageTk.PhotoImage(Image.open("multibly.png").resize((50, 50)))
image_divide = ImageTk.PhotoImage(Image.open("divid.png").resize((50, 50)))

result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack(padx=10, pady=10)

equation_label.config(text=generateEquation())

infixExp = generateEquation()
postfixExp = toPostfix(infixExp)

queueOperator = [char for char in postfixExp if isOperator(char)]

checkSelectedAnswer(images_frame, image_plus, image_minus, image_multiply, image_divide, queueOperator, postfixExp, score_value, wrong_answers)

window.mainloop()
