import tkinter as tk
from PIL import ImageTk, Image
import pytesseract
import cv2
import numpy as np

def generate_equation():
    # Path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia_CPIT380\project\app\tesseract.exe"

    # Open the image file
    image_path = r"C:\Users\Afnan\PycharmProjects\CPIT380project\images\EQUATION2.png"
    img = cv2.imread(image_path)

    # Convert the image to a NumPy array and change color space
    img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Convert the image to text using PyTesseract
    equation = pytesseract.image_to_string(img_array)

    # Extract the operator from the equation
    operator = ''
    for char in equation:
        if char in '+-*/':
            operator = char
            break

    spaced_text = []

    # Iterate through the characters of the text
    for char in equation:
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

    return text_without_final_space, operator

def check_answer(selected_op, correct_op):
    if selected_op == correct_op:
        result_label.config(text="Correct!")
    else:
        result_label.config(text="Incorrect. Try again.")

# Create main window
window = tk.Tk()
window.title("Equation Game")

# Set the window dimensions and make it fixed
window.geometry("300x400")
window.resizable(False, False)

# Create the score label
score_label = tk.Label(window, text="Score: " + " ", font=("Arial", 14))
score_label.pack(padx=10, pady=10, anchor=tk.NW)

# Create the equation label
equation_label = tk.Label(window, text="", font=("Helvetica", 20, "bold"))
equation_label.pack(padx=10, pady=10)

# Create the answer label
answer_label = tk.Label(window, text="Select the correct operator:", font=("Arial", 14))
answer_label.pack(padx=10, pady=10)

# Create the answer image labels
images_frame = tk.Frame(window)
images_frame.pack(padx=10, pady=10, fill=tk.X)

# Load the images
image_plus = ImageTk.PhotoImage(Image.open("addition.png").resize((50, 50)))
image_minus = ImageTk.PhotoImage(Image.open("substract.png").resize((50, 50)))
image_multiply = ImageTk.PhotoImage(Image.open("multibly.png").resize((50, 50)))
image_divide = ImageTk.PhotoImage(Image.open("divid.png").resize((50, 50)))

# Show equation detected by OCR & all operators in this equation
equation, correct_operator = generate_equation()
equation_label.config(text=equation)

# Create the image labels
plus_button = tk.Button(images_frame, image=image_plus, command=lambda op="+": check_answer(op, correct_operator))
plus_button.pack(side=tk.LEFT, padx=5)

minus_button = tk.Button(images_frame, image=image_minus, command=lambda op="-": check_answer(op, correct_operator))
minus_button.pack(side=tk.LEFT, padx=5)

multiply_button = tk.Button(images_frame, image=image_multiply, command=lambda op="*": check_answer(op, correct_operator))
multiply_button.pack(side=tk.LEFT, padx=5)

divide_button = tk.Button(images_frame, image=image_divide, command=lambda op="/": check_answer(op, correct_operator))
divide_button.pack(side=tk.LEFT, padx=5)

# Create the result label
result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack(padx=10, pady=10)

# Run the main event loop
window.mainloop()
