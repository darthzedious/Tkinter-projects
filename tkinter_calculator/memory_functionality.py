memory_value = 0.0


def memory_clear():
    global memory_value
    memory_value = 0.0

def memory_plus(window):
    try:
        num = float(window.get())
        global memory_value
        memory_value += num
        # window.set(str(memory_value))
    except ValueError:
        window.set("Error")


def memory_minus(window):
    global memory_value
    try:
        num = float(window.get())
        memory_value -= num
        # window.set(str(memory_value))
    except ValueError:
        window.set("Error")


def memory_recall(window):
    global memory_value
    window.set(str(memory_value))

# memory_plus = memory_plus(window, memory_value, display_error_message())
# memory_minus = memory_minus(window, memory_value, display_error_message())
# memory_recall = memory_recall(window, memory_value)
