import tkinter as tk
from PIL import ImageTk, Image
import random

def generate_equation():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)
    equation = f"{num1} {operator} {num2}"
    print(equation)
    return equation, operator

def check_answer(user_operator, operator):
    if user_operator == operator:
        result_label.config(text="Correct!")
    else:
        result_label.config(text="Incorrect! Try again.")

def generate_new_equation():
    global equation
    equation = generate_equation()
    equation_label.config(text=equation[0])
    result_label.config(text="")

# Create the main window
window = tk.Tk()
window.title("Equation Game")

# Set the window dimensions and make it fixed
window.geometry("300x280")
window.resizable(False, False)

# Set the background image
bg_image = ImageTk.PhotoImage(Image.open("bbg.jpg"))

# Create a label widget to hold the background image
background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the score label
score_label = tk.Label(window, text="Score: "+" ", font=("Arial", 14))
score_label.pack(padx=10, pady=10, anchor=tk.NW)

# Create the equation label
equation_label = tk.Label(window, text="", font=("Helvetica", 20, "bold"))
equation_label.pack(padx=10, pady=10)

# Create the answer label
answer_label = tk.Label(window, text="What is the correct answer", font=("Arial", 14))
answer_label.pack(padx=10, pady=10)

# Create the answer image labels
images_frame = tk.Frame(window)
images_frame.pack(padx=10, pady=10, fill=tk.X)

# Load the images
image_plus = ImageTk.PhotoImage(Image.open("addition.png").resize((50, 50)))
image_minus = ImageTk.PhotoImage(Image.open("substract.png").resize((50, 50)))
image_multiply = ImageTk.PhotoImage(Image.open("multibly.png").resize((50, 50)))
image_divide = ImageTk.PhotoImage(Image.open("divid.png").resize((50, 50)))

# Show equation that detect by AI & all operator in this equation
equation, operator = generate_equation()

# Create the image labels
plus_button = tk.Button(images_frame, image=image_plus, command=lambda: check_answer("+", operator))
plus_button.pack(side=tk.LEFT, padx=5)

minus_button = tk.Button(images_frame, image=image_minus, command=lambda: check_answer("-", operator))
minus_button.pack(side=tk.LEFT, padx=5)

multiply_button = tk.Button(images_frame, image=image_multiply, command=lambda: check_answer("*", operator))
multiply_button.pack(side=tk.LEFT, padx=5)

divide_button = tk.Button(images_frame, image=image_divide, command=lambda: check_answer("/", operator))
divide_button.pack(side=tk.LEFT, padx=5)

# Create the result label
result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack(padx=10, pady=10)

# Generate the first equation
equation_label.config(text=equation)

window.mainloop()
