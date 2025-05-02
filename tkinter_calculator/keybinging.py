from tkinter_calculator.general_operations import on_button_click, all_clear


def on_keypress(event, window):
    key = event.char

    if key.isdigit() or key in [".", "+", "-", "*", "/", "=", "%"]:
        on_button_click("X" if key == "*" else key, window)
    elif event.keysym == "Return":
        on_button_click("=", window)
    elif event.keysym == "BackSpace":
        window.set(window.get()[:-1])
    elif event.keysym == "Escape":
        all_clear()

def bind_keys(root, window):
    root.bind("<Key>", lambda event: on_keypress(event, window))
