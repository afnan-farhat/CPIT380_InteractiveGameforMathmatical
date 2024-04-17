import tkinter as tk
def calculate():
    global equation
    try:
        result = eval(equation)  # Evaluate the equation
        result_label.config(text="Result: " + str(result))  # Display the result
    except Exception as e:
        result_label.config(text="Error: Invalid equation")  # Handle invalid equations or errors

def modify_equation(operator):
    global equation
    equation_parts = equation.split(operator)  # Split the equation based on the operator
    if len(equation_parts) > 1:
        if operator == '+':
            new_part = str(eval(equation_parts[0]) + eval(equation_parts[1]))
        elif operator == '-':
            new_part = str(eval(equation_parts[0]) - eval(equation_parts[1]))
        elif operator == '*':
            new_part = str(eval(equation_parts[0]) * eval(equation_parts[1]))
        elif operator == '/':
            new_part = str(eval(equation_parts[0]) / eval(equation_parts[1]))

        equation = new_part
        entry.delete(0, tk.END)  # Clear the current equation in the entry widget
        entry.insert(tk.END, equation)  # Insert the modified equation in the entry widget

root = tk.Tk()
root.title("Calculator")

equation = ""  # Initialize the equation variable

# Create an entry to display the equation
entry = tk.Entry(root, font=("Arial", 14), width=20)
entry.pack(pady=10)

# Operation Buttons
addition_btn = tk.Button(root, text="+", command=lambda: modify_equation('+'))
addition_btn.pack(side=tk.LEFT, padx=5)

subtraction_btn = tk.Button(root, text="-", command=lambda: modify_equation('-'))
subtraction_btn.pack(side=tk.LEFT, padx=5)

multiplication_btn = tk.Button(root, text="*", command=lambda: modify_equation('*'))
multiplication_btn.pack(side=tk.LEFT, padx=5)

division_btn = tk.Button(root, text="/", command=lambda: modify_equation('/'))
division_btn.pack(side=tk.LEFT, padx=5)

# Create a button to calculate the result
calculate_btn = tk.Button(root, text="Calculate", command=calculate)
calculate_btn.pack(pady=10)

# Create an element to display the result
result_label = tk.Label(root, text="Result: ")
result_label.pack()

root.mainloop()