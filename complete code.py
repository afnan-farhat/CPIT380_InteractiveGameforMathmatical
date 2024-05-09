# ------------------------------------------------------------
# STEP 3: CREATE CLASS (STACK) AND ALL OPERATION OF STACK

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

            result = calculateResult(operand1, operand2, symbol)
            stack.push(result)
            StackFullEquation.push(str(symbol))

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
    check_answer(choice, queueOfOperators)
    while queueOfOperators[0] != choice:
        score -= 10
        print("Your score decreased by 10 points.\nNew Score is: ", score)
        choice = input("Wrong answer. Please try again")

    if queueOfOperators[0] == choice:
        score += 10
        print("Correct!.\nNew Score is: ", score)
        queueOfOperators.pop(0)

# ------------------------------------------------------------------------------
# STEP 1: DETECT EQUATION FROM IMAGE BY AI
import cv2
import pytesseract
import numpy as np
import re
def generateEquation():
    # Path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia_CPIT380\project\app\tesseract.exe"

    # Open the image file
    image_path = r"C:\Users\Afnan\PycharmProjects\CPIT380project\images\EQUATION2.png"
    img = cv2.imread(image_path)

    # Convert the image to a NumPy array and change color space
    img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Save the image using OpenCV
    cv2.imwrite("images/removed_noise.jpg", img_array)

    # Convert the image to text using PyTesseract
    text = pytesseract.image_to_string(img_array)

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
    return text_without_final_space




# ------------------------------------------------------------------------------
# STEP 2: SEND EQUATION IN GUI

import tkinter as tk
from PIL import ImageTk, Image
import random

# Function to check if the selected answer is correct

# Function to generate a new equation and update the interface

def check_answer( answer, operator):
    if answer == operator:
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Wrong answer! Try again.", fg="red")

def checkSelectedAnswer(images_frame, image_plus, image_minus, image_multiply, image_divide):
    # Create the image labels
    plus_label = tk.Label(images_frame, image=image_plus)
    plus_label.pack(side=tk.LEFT, padx=5)

    minus_label = tk.Label(images_frame, image=image_minus)
    minus_label.pack(side=tk.LEFT, padx=5)

    multiply_label = tk.Label(images_frame, image=image_multiply)
    multiply_label.pack(side=tk.LEFT, padx=5)

    divide_label = tk.Label(images_frame, image=image_divide)
    divide_label.pack(side=tk.LEFT, padx=5)

    # ------------------------------------------------------------------------------------
    # STEP (): EQUATION

    infixExps = [generateEquation()]

    for exp in infixExps:
        postfix = toPostfix(exp)
        print(f'Infix: {exp} -> Postfix: {postfix}')

        queueOperator = []  # Create an empty list


        for char in postfix:
            if isOperator(char):
                queueOperator.append(char)

        for operator in queueOperator:
            # Check on input of uer if it equals the correct operator
            plus_label.bind("<Button-1>", lambda event: check_answer("+", operator))
            minus_label.bind("<Button-1>", lambda event: check_answer("-", operator))
            multiply_label.bind("<Button-1>", lambda event: check_answer("*", operator))
            divide_label.bind("<Button-1>", lambda event: check_answer("/", operator))

        result = evaluatePostfix(infixExps, postfix, queueOperator)
        print(f'\nResult: {result}')
        exit()



# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# STEP 4: GUI

# Create the main window
window = tk.Tk()
window.title("Equation Game")

# Set the window dimensions and make it fixed
window.geometry("300x280")
window.resizable(False, False)

# Set the background image
bg_image = ImageTk.PhotoImage(Image.open("Operation_images/bbg.jpg"))

# Create a label widget to hold the background image
background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the score label
score_label = tk.Label(window, text="Score: " + " ", font=("Arial", 14))
score_label.pack(padx=10, pady=10, anchor=tk.NW)

# Create the equation label
equation_label = tk.Label(window, text="", font=("Helvetica", 20, "bold"))
equation_label.pack(padx=10, pady=10)

# Create the answer label
answer_label = tk.Label(window, text="what is the correct answer", font=("Arial", 14))
answer_label.pack(padx=10, pady=10)

# Create the answer image labels
images_frame = tk.Frame(window)
images_frame.pack(padx=10, pady=10, fill=tk.X)

# Load the images
image_plus = ImageTk.PhotoImage(Image.open("Operation_images/addition.png").resize((50, 50)))
image_minus = ImageTk.PhotoImage(Image.open("Operation_images/substract.png").resize((50, 50)))
image_multiply = ImageTk.PhotoImage(Image.open("Operation_images/multibly.png").resize((50, 50)))
image_divide = ImageTk.PhotoImage(Image.open("Operation_images/divid.png").resize((50, 50)))

# Create the result label
result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack(padx=10, pady=10)

checkSelectedAnswer( images_frame, image_plus, image_minus, image_multiply, image_divide)

# Generate the first equation
equation_label.config(text=generateEquation())

# Start the main loop
window.mainloop()


#



