import tkinter as tk
import random


def generate_equation():
    operands = [str(random.randint(1, 10)) for _ in range(3)]
    operators = ['*', '/', '+', '-']
    equation = ' '.join([random.choice(operands) + random.choice(operators) for _ in range(2)]) + random.choice(
        operands)
    return equation


def evaluate():
    equation = equation_label.cget("text")
    operators = ['*', '/', '+', '-']

    # Check if the equation contains higher priority operators
    higher_priority = False
    for operator in operators[:2]:
        if operator in equation:
            higher_priority = True
            break

    # If higher priority operators are found, display message
    if higher_priority:
        result_label.config(text="Equation is valid.")
    else:
        result_label.config(text="Error: No higher priority operators found. Try again.")
        return

    try:
        result = eval(equation)
        result_label.config(text="Result: " + str(result))
    except:
        result_label.config(text="Error: Invalid equation.")


# Create main window
root = tk.Tk()
root.title("Fixed Equation Calculator")

# Generate a fixed equation
equation = generate_equation()

# Create label for displaying equation
equation_label = tk.Label(root, text=equation)
equation_label.grid(row=0, column=0, columnspan=4)

# Create label for displaying result or error message
result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=4)

# Create button to evaluate equation
evaluate_button = tk.Button(root, text="Evaluate", command=evaluate)
evaluate_button.grid(row=2, column=0, columnspan=4)

# Run the main event loop
root.mainloop()
