import cv2
import pytesseract
import numpy as np
import re

# Define the CharStack class for handling symbols
class CharStackNode:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

class IntStackNode:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node


class IntStack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def peek(self):
        top_value = -19999
        if not self.is_empty():
            top_value = self.peek_helper(self.top)
        return top_value

    def peek_helper(self, top):
        return top.get_data()

class CharStack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = CharStackNode(data, self.top)
        self.top = new_node

    def print_stack(self):
        self._print_stack(self.top)

    def _print_stack(self, top):
        help_ptr = top
        while help_ptr is not None:
            print(f"{help_ptr.get_data()}, ", end="")
            help_ptr = help_ptr.get_next()
        print()

    def _stack(self):
        self._print_stack(self.top)

    def _print_stack(self, top):
        help_ptr = top
        while help_ptr is not None:
            print(f"{help_ptr.get_data()}, ", end="")
            help_ptr = help_ptr.get_next()
        print()
# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia CPIT380\project\app\tesseract.exe"

# Open the image file
image_path = r"C:\Users\Afnan\PycharmProjects\cpit380\images\EQUATION2.png"
img = cv2.imread(image_path)

# Convert the image to a NumPy array and change color space
img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Save the image using OpenCV
cv2.imwrite("images/removed_noise.jpg", img_array)

# Convert the image to text using PyTesseract
text = pytesseract.image_to_string(img_array)

def fix_equation(equation):
    # Use regular expression to find patterns like 'number('
    pattern = re.compile(r'(\d+)\(')
    fixed_equation = re.sub(pattern, r'\1*(', equation)
    return fixed_equation

# Example usage
fixed_equation = fix_equation(text)

print("Equation is : ", fixed_equation)

# Create an instance of CharStack
stack = CharStack()

# Push symbols onto the stack
for char in fixed_equation:
    if char in ['+', '-', '*', '/', '(', ')']:
        stack.push(char)

# Read the symbols

# Print the symbols
print("Symbols in the equation:")
stack.print_stack()
