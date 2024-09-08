#%%
import tkinter as tk
from tkinter import messagebox

# Initialize the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("400x400")

# Display entry for showing input and output
display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="solid")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Function to handle button clicks
def button_click(value):
    current_text = display.get()
    display.delete(0, tk.END)
    display.insert(0, current_text + value)

# Buttons for the calculator
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '+'
]

# Position buttons in a grid
row_val = 1
col_val = 0
for button in buttons:
    action = lambda x=button: button_click(x)
    tk.Button(root, text=button, width=10, height=3, command=action).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val == 4:
        col_val = 0
        row_val += 1

# Function to clear the display
def clear_display():
    display.delete(0, tk.END)

def evaluate_expression():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")
        clear_display()

# Add clear and equal buttons
tk.Button(root, text='C', width=10, height=3, command=clear_display).grid(row=row_val, column=0)
tk.Button(root, text='=', width=10, height=3, command=evaluate_expression).grid(row=row_val, column=1, columnspan=3)

# Start the main loop
root.mainloop()

# %%