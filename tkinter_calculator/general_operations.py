from tkinter_calculator.formulas import calculate_factorial, calculate_root

reset_display = False
first_num = None
operation = None

def clear_entry(window):
    window.set("")

def all_clear():
    global first_num, operation
    clear_entry(window)
    first_num = None
    operation = None

# def display_error_message(window):
#     window.set("Error")

def on_button_click(value: str, window):
    global first_num, operation, reset_display
    current_text = window.get()

    if value == "-" and (not current_text or current_text == "0.0" or current_text == "0"):
        window.set("-")
        return

    if reset_display or current_text in ["0.0", "0"]:
        window.set("")
        reset_display = False

    if value.isdigit() or value == ".":
        window.set(window.get() + value)
        return

    if value == "!":
        calculate_factorial(window, current_text)

    if value == "√":
        calculate_root(window, current_text)

    elif value in ["+", "-", "X", "/", "%"]:
        if first_num is None:
            try:
                first_num = float(current_text)
            except ValueError:
                window.set("Error")
        else:
            if operation is not None:
                second_num = float(current_text) if current_text else 0.0
                result = calculate(first_num, second_num, operation)
                window.set(str(result))
                first_num = result
        operation = value
        reset_display = True

    elif value == "=":
        if first_num is not None and operation:
            try:
                second_num = float(current_text) if current_text else 0.0
                result = calculate(first_num, second_num, operation)
                window.set(str(result))
                first_num = result
                operation = None
            except ZeroDivisionError:
                window.set("Error")

    elif value == "+/-":
        try:
            num = float(current_text) if current_text else 0.0
            new_value = -num
            window.set(str(new_value))
            if first_num is not None and operation is None:
                first_num = new_value
        except ValueError:
            window.set("Error")

def calculate(first_number: float, second_number: float, operator: str):
    if operator == "+":
        return first_number + second_number
    elif operator == "-":
        return first_number - second_number
    elif operator == "X":
        return first_number * second_number
    elif operator == "/":
        if second_number == 0:
            global window
            window.set("Error")
        return first_number / second_number
    elif operator == "%":
        return (first_number * second_number) / 100
