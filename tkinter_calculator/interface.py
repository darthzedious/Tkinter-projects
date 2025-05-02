from tkinter import ttk, StringVar
from memory_functionality import memory_recall, memory_plus, memory_minus, memory_clear
from tkinter_calculator.general_operations import all_clear, clear_entry, on_button_click


def create_interface(root):
    frame = ttk.Frame(root, padding="5", height=500, width=500)
    frame.grid(column=0, row=0, sticky="nsew")

    window = StringVar()
    # window.set("0")
    window_entry = ttk.Entry(frame, textvariable=window, font=("Arial", 20), justify="center")
    window_entry.grid(row=0, column=1, columnspan=3, ipadx=10, ipady=10, padx=5, pady=5, sticky="nsew")

    memo_plus = memory_plus(window)
    memo_minus = memory_minus(window)
    memo_recall = memory_recall(window)

    def clear_entry(window):
        window.set("")

    def all_clear():
        global first_num, operation
        clear_entry(window)
        first_num = None
        operation = None

    buttons_coordinates = [
        ("MC", 1, 0), ("7", 1, 1), ("8", 1, 2), ("9", 1, 3), ("-", 1, 4),
        ("M+", 2, 0), ("4", 2, 1), ("5", 2, 2), ("6", 2, 3), ("X", 2, 4),
        ("M-", 3, 0), ("1", 3, 1), ("2", 3, 2), ("3", 3, 3), ("+", 3, 4),
        ("MR", 4, 0), (".", 4, 1), ("0", 4, 2), ("√", 4, 3), ("/", 4, 4),
        ("!", 5, 0), ("=", 5, 2, 2), ("%", 5, 4), ("+/-", 5, 1),
    ]

    for btn in buttons_coordinates:
        char, row, col = btn[0], btn[1], btn[2]
        col_span = btn[3] if len(btn) > 3 else 1

        if char == "MC":
            action = memory_clear
        elif char == "M+":
            action = memo_plus
        elif char == "M-":
            action = memo_minus
        elif char == "MR":
            action = memo_recall
        else:
            action = lambda x=char: on_button_click(x, window)

        button = ttk.Button(frame, text=char, command=action)
        button.grid(row=row, column=col, columnspan=col_span, sticky="nsew", pady=5, padx=2)

        ttk.Button(frame, text="C", command=clear_entry, width=5).grid(column=4, row=0, sticky="nsew")
        ttk.Button(frame, text="AC", command=all_clear, width=5).grid(column=0, row=0, sticky="nsew")

    return window, frame
