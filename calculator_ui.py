import tkinter as tk
import warnings
import re
from math import *
from playsound import playsound
from tkinter import ttk
from keypad import Keypad
from calculator_controller import Calculator


class CalculatorUI(tk.Tk):
    """Class for creating a calculator GUI."""

    def __init__(self) -> None:
        """Initialize the CalculatorUI."""
        super().__init__()
        self.calculator = Calculator()
        self.title("Calculator")
        self.rowconfigure(tuple(range(2)), weight=1)
        self.columnconfigure(tuple(range(3)), weight=1)
        self.equation = tk.StringVar()
        self.equation.set('')
        self.last_equations = []
        self.init_components()

    def init_components(self) -> None:
        """Initialize the components of the calculator."""
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.expression_field = tk.Entry(entry_frame, state="disabled", textvariable=self.equation, justify="right", font=("Arial", 20), disabledbackground="black", disabledforeground="yellow")
        self.expression_field.pack(fill=tk.BOTH, expand=True)

        self.history = ttk.Combobox(self, state="readonly")
        self.history.set("history")
        self.history.bind("<<ComboboxSelected>>", lambda _: self.history_select_handler(self.history.get()))
        self.history.grid(row=0, column=3, sticky="nsew")

        math_func = 'CLR,2 DEL,1 (,1 ),1 mod,1 exp,1 ln,1 sqrt,1 log10,1 log2,1 x!,1'.split()
        math_func = [key.split(",") for key in math_func]
        math_func_keypad = Keypad(self, keynames=math_func, columns=3)
        math_func_keypad.bind('<Button>', lambda event: self.press(event.widget["text"]))
        math_func_keypad.configure(foreground='#FFFFFF', background="#48494B")
        math_func_keypad.frame.configure(background='#FEECEC')
        math_func_keypad.grid(row=1, column=0, sticky="nsew")

        keys = '7,1 8,1 9,1 4,1 5,1 6,1 1,1 2,1 3,1 0,2 .,1 '.split()
        keys = [key.split(",") for key in keys]
        keypad = Keypad(self, keynames=keys, columns=3)
        keypad.bind('<Button>', lambda event: self.press(event.widget["text"]))
        keypad.configure(foreground='#000000', background="#BEBEBE")
        keypad.frame.configure(background='#FEECEC')
        keypad.grid(row=1, column=1, sticky="nsew")

        operators = '*,1 /,1 +,1 -,1 ^,1 =,1'.split()
        operators = [key.split(",") for key in operators]
        operators_keypad = Keypad(self, keynames=operators, columns=1)
        operators_keypad.bind('<Button>', lambda event: self.press(event.widget["text"]))
        operators_keypad.configure(foreground='#104A8E', background="#F4BC1C")
        operators_keypad.frame.configure(background='#FEECEC')
        operators_keypad.grid(row=1, column=2, sticky="nsew")

    def press(self, key: str) -> None:
        """Update the equation when a button is pressed.

        :param key: The key pressed.
        """
        if self.equation.get() == "Error":
            self.clear_equation()
        if key == "CLR":
            self.clear_equation()
        elif key == "=":
            self.calculate_result()
        elif key == "DEL":
            self.delete_last_entry()
        elif key == "mod":
            self.handle_modulus_key()
        elif key.isnumeric():
            self.handle_numeric_key(key)
        else:
            self.handle_operator_key(key)
        self.update_field_color()

    def clear_equation(self) -> None:
        """Clear the equation."""
        self.equation.set('')
        self.last_equations = ["", ]

    def calculate_result(self) -> None:
        """Calculate the result of the equation."""
        result = self.calculator.calculate(self.equation.get(), self.last_equations.copy())
        if result == "Error":
            playsound("warning_sound.mp3")
        self.equation.set(result)
        self.last_equations.clear()
        for index in range(len(str(result))):
            self.last_equations.append(str(result)[:index])
        self.history["values"] = [snapshot[0] for snapshot in self.calculator.load_snapshot()]

    def delete_last_entry(self) -> None:
        """Delete the last entry from the equation."""
        if self.equation.get() and self.last_equations:
            self.equation.set(self.last_equations[-1])
            self.last_equations.pop()

    def handle_modulus_key(self) -> None:
        """Handle key press for modulus operation."""
        self.last_equations.append(self.equation.get())
        self.equation.set(self.equation.get() + "%")

    def handle_numeric_key(self, key: str) -> None:
        """Handle key press for numeric entry."""
        self.last_equations.append(self.equation.get())
        self.equation.set(self.equation.get() + key)

    def handle_operator_key(self, key: str) -> None:
        """Handle key press for operator entry."""
        self.last_equations.append(self.equation.get())
        last_char = self.equation.get()[-1] if self.equation.get() else ''
        if key in "()" or ((last_char.isnumeric() or not self.equation.get()) and key in "+-*/^."):
            self.equation.set(self.equation.get() + key)
        elif key == "x!" and self.equation.get() and last_char not in "+-*/^()":
            self.equation.set("(" + self.equation.get() + ")!")
        elif key == "x!":
            self.equation.set(self.equation.get() + "!")
        elif last_char in "+-*/^()!%":
            if key in "+-*/^.":
                self.equation.set(self.equation.get() + key)
            else:
                self.equation.set(self.equation.get() + key.replace("ln", "log") + "(")
        else:
            self.equation.set(key.replace("ln", "log") + "(" + self.equation.get() + ")")

    def update_field_color(self) -> None:
        """Update the color of the expression field based on the equation validity."""
        try:
            if self.equation.get():
                pattern = r"\(([^)]+)\)!"
                equation = re.sub(pattern, lambda match: f"factorial({match.group(1)})", self.equation.get())
                eval(equation.replace("^", "**"))
                self.expression_field.config(disabledforeground="yellow")
        except Exception:
            self.expression_field.config(disabledforeground="red")

    def history_select_handler(self, history: str) -> None:
        """Handle the selection of a history item.

        :param history: The selected history item.
        """
        histories = self.calculator.load_snapshot()
        histories_values = [value[0] for value in histories]
        self.last_equations = histories[histories_values.index(history)][1].copy()
        history = history.replace("=", "").strip()
        self.equation.set(history)
        self.history.set("history")
        self.expression_field.config(disabledforeground="yellow")

    def run(self) -> None:
        """Run the calculator application."""
        self.mainloop()


warnings.simplefilter("ignore", SyntaxWarning)
