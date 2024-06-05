import tkinter as tk
from PIL import ImageTk, Image
import cv2
import pytesseract
import numpy as np

class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size
        self.queueOperator = []  # Public variable with underscore prefix
        self.infixExps = []  # Public list for infix expressions

    def push(self, item):
        if len(self.stack) < self.size:
            self.stack.append(item)

    def pop(self):
        result = -1
        if self.stack != []:
            result = self.stack.pop()
        return result

    def peek(self):
        if not self.isEmpty():
            return self.stack[-1]
        else:
            return None

    def isEmpty(self):
        return self.stack == []

    def topChar(self):
        result = -1
        if self.stack != []:
            result = self.stack[len(self.stack) - 1]
        return result


class EquationGame:
    def __init__(self, window):
        self.window = window
        self.score = 0
        self.wrong_answers = 0

        self.bg_image = ImageTk.PhotoImage(Image.open("bbg.jpg"))
        self.background_label = tk.Label(window, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.score_label = tk.Label(window, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(padx=10, pady=10, anchor=tk.NW)

        self.equation_label = tk.Label(window, text="", font=("Helvetica", 20, "bold"))
        self.equation_label.pack(padx=10, pady=10)

        self.answer_label = tk.Label(window, text="What is the correct answer?", font=("Arial", 14))
        self.answer_label.pack(padx=10, pady=10)

        # frame
        self.images_frame = tk.Frame(window)
        self.images_frame.pack(padx=10, pady=10, fill=tk.X)

        self.image_plus = ImageTk.PhotoImage(Image.open("addition.png").resize((50, 50)))
        self.image_minus = ImageTk.PhotoImage(Image.open("substract.png").resize((50, 50)))
        self.image_multiply = ImageTk.PhotoImage(Image.open("multibly.png").resize((50, 50)))
        self.image_divide = ImageTk.PhotoImage(Image.open("divid.png").resize((50, 50)))

        self.result_label = tk.Label(window, text="", font=("Arial", 14))
        self.result_label.pack(padx=10, pady=10)

        self.infixExp = self.generateEquation()
        self.equation = self.infixExp
        self.equation_label.config(text=self.infixExp) #
        self.postfixExp = self.toPostfix(self.infixExp)  # 879*2/+
        self.queueOperator = [char for char in self.postfixExp if self.isOperator(char)]  # [*,/,+]

        self.buttons = self.createButtons()

    def generateEquation(self):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia_CPIT380\project\app\tesseract.exe"
        image_path = r"C:\Users\Afnan\PycharmProjects\CPIT380project_final\Equation\EQ33.jpg"
        img = cv2.imread(image_path)
        img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        text = pytesseract.image_to_string(img_array)
        # print(text)
        spaced_text = []

        for char in text:
            if char.isdigit() or char in "+-*/":
                spaced_text.append(char)
                spaced_text.append(" ")
            else:
                spaced_text.append(char)

        # print(spaced_text)

        spaced_text_str = "".join(spaced_text)
        text_without_final_space = spaced_text_str[:-1]
        return text_without_final_space

    def toPostfix(self, expression):  # 8 + 7 * 9 / 2
        result = ""
        stack = Stack(15)

        for char in expression.split(" "):
            if self.isOperand(char):
                result += char
            elif self.isOperator(char):
                while (not stack.isEmpty()) and (
                        self.getPrecedence(stack.topChar()) >= self.getPrecedence(char)):
                    result += stack.pop()
                stack.push(char)

        while not stack.isEmpty():
            result += stack.pop()

        return result

    def update_equation_label(self, new_equation, current_operator):
        # Split the new equation into a list of tokens
        equation_tokens = new_equation.split()

        # Find the index of the current operator
        operator_index = equation_tokens.index(current_operator)

        # Extract the operands around the operator
        operand1 = equation_tokens[operator_index - 1]
        operand2 = equation_tokens[operator_index + 1]

        # Perform the calculation
        if '.' in operand1 or '.' in operand2:
            # At least one operand is a floating-point number
            operand1 = float(operand1)
            operand2 = float(operand2)

            if current_operator == '*':
                result = str(operand1 * operand2)
            elif current_operator == '/':
                result = str(operand1 / operand2)
            elif current_operator == '+':
                result = str(operand1 + operand2)
            elif current_operator == '-':
                result = str(operand1 - operand2)
            else:
                result = ''
        else:
            # Both operands are integers
            operand1 = float(operand1)
            operand2 = float(operand2)

            if current_operator == '*':
                result = str(operand1 * operand2)
            elif current_operator == '/':
                result = str(operand1 // operand2)
            elif current_operator == '+':
                result = str(operand1 + operand2)
            elif current_operator == '-':
                result = str(operand1 - operand2)
            else:
                result = ''

        # Update the equation label with the calculated result
        equation_tokens[operator_index - 1] = result
        equation_tokens[operator_index] = ''
        equation_tokens[operator_index + 1] = ''

        # Remove empty elements from the equation tokens
        equation_tokens = list(filter(None, equation_tokens))

        # Construct the updated equation label
        updated_equation = ' '.join(equation_tokens)
        self.equation = updated_equation
        self.equation_label.config(text=updated_equation)


    def createButtons(self):
        plus_button = tk.Button(self.images_frame, image=self.image_plus,
                                command=lambda: self.check_answer("+"))
        plus_button.pack(side=tk.LEFT, padx=5)

        minus_button = tk.Button(self.images_frame, image=self.image_minus,
                                 command=lambda: self.check_answer("-"))
        minus_button.pack(side=tk.LEFT, padx=5)

        multiply_button = tk.Button(self.images_frame, image=self.image_multiply,
                                    command=lambda: self.check_answer("*"))
        multiply_button.pack(side=tk.LEFT, padx=5)

        divide_button = tk.Button(self.images_frame, image=self.image_divide,
                                  command=lambda: self.check_answer("/"))
        divide_button.pack(side=tk.LEFT, padx=5)

        return plus_button, minus_button, multiply_button, divide_button

    def isOperand(self, c):
        return c not in "+-*/"

    def isOperator(self, c):
        return c in "+-*/"

    def getPrecedence(self, c):
        result = 0

        if c == '+':
            return 1
        elif c == '-':
            return 1
        elif c == '*':
            return 2
        elif c == '/':
            return 2
        else:
            return -1

    def check_answer(self, answer):
        if len(self.queueOperator) == 0:
            self.equation_label.config(text="Congratulations", fg="blue")

            self.answer_label.config(text="your result is: " + str(self.equation), fg="black")



            for button in self.buttons:
                button.destroy()
            self.result_label.destroy()

            self.images_frame.destroy()
            return

        current_operator = self.queueOperator[0]

        if answer == current_operator:
            self.update_score(10)
            self.result_label.config(text="Your score is: " + str(self.score), fg="green")

            # Update equation label
            self.update_equation_label(self.equation, current_operator)


            # Remove current operator from the queue
            self.queueOperator.pop(0)

        else:
            self.update_score(-10)
            self.result_label.config(text="Your score decrease 10 score\nNew Score is: " + str(self.score),
                                     fg="red")

        if len(self.queueOperator) == 0:
            self.check_answer("")

        return

    def update_score(self, value):
        self.score += value
        self.score_label.config(text="Score: " + str(self.score))

    def evaluatePostfix(self, infixExps, expression):  # 879*2/+
        stack = Stack(15)
        StackFullEquation = Stack(30)
        infixExps_string = ""

        for char in expression:  # 879*2/+
            if self.isOperand(char):
                stack.push(int(char))
                StackFullEquation.push(int(char))
            elif self.isOperator(char):
                symbol = char
                operand2 = stack.pop()
                operand1 = stack.pop()
                del self.queueOperator[0]
                result = self.calculateResult(operand1, operand2, symbol)
                stack.push(result)

                StackFullEquation.push(str(symbol))

                part_of_equation = f"{operand1} {symbol} {operand2}"

                stack_items = stack.stack
                stack_string = ' '.join(map(str, stack_items))
                infixExps_string = ""
                try:
                    infixExps = list(map(lambda x: x.replace(part_of_equation, str(result)), infixExps))
                    infixExps_string = ''.join(infixExps)
                    # self.update_equation_label(infixExps_string)
                    return infixExps_string

                except ValueError:
                    return str(stack_string)

        self.update_equation_label(infixExps_string)
        return infixExps_string, self.queueOperator

    def calculateResult(self, operand1, operand2, operator):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 / operand2


if __name__ == "__main__":
    window = tk.Tk()

    window.title("Equation Game")
    window.geometry("300x280")
    window.resizable(False, False)
    game = EquationGame(window)
    window.mainloop()
