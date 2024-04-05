
import cv2
import pytesseract
import numpy as np
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Afnan\Desktop\Student Life\KAU\3th\semester2\Multimedia CPIT380\project\app\tesseract.exe"

# Open the image file
image_path = r"C:\Users\Afnan\PycharmProjects\cpit380\newfont.png"
img = cv2.imread(image_path)

# Convert the image to a NumPy array and change color space
img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Save the image using OpenCV
cv2.imwrite("removed_noise.jpg", img_array)

# Convert the image to text using PyTesseract
text = pytesseract.image_to_string(img_array)


def fix_equation(equation):
    # Use regular expression to find patterns like 'number('
    pattern = re.compile(r'(\d+)\(')
    fixed_equation = re.sub(pattern, r'\1*(', equation)
    return fixed_equation

# Example usage
fixed_equation = fix_equation(text)

# Print the extracted text
print("Equation is : ", fixed_equation)

# Handel with Exception or Display the output
try:
    result = eval(fixed_equation)
    print("Result:", result)
except Exception as e:
    print("Error:", e, "\nPlease try again")
