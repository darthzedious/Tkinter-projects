from tkinter import *
from tkinter import ttk

def create_root():
    root = Tk()
    root.title("BMI Calculator")
    root.geometry("350x200")
    root.resizable(False, False)
    return root

def create_frame(root):
    frame = ttk.Frame(root, padding="10")
    frame.grid(column=0, row=0, sticky="nsew")
    return frame

root = create_root()
frame = create_frame(root)


label_height = ttk.Label(frame, text="Enter your height (m):")
label_height.grid(column=0, row=0, sticky="w", padx=5, pady=5)

label_weight = ttk.Label(frame, text="Enter your weight (kg):")
label_weight.grid(column=0, row=1, sticky="w", padx=5, pady=5)


enter_height = ttk.Entry(frame, width=10)
enter_height.grid(column=1, row=0, sticky="w", padx=5, pady=5)

enter_weight = ttk.Entry(frame, width=10)
enter_weight.grid(column=1, row=1, sticky="w", padx=5, pady=5)


bmi_label = ttk.Label(frame, text="BMI: ")
bmi_label.grid(column=1, row=3, sticky="w", padx=5, pady=5)


description = StringVar()
label_description = ttk.Label(frame, textvariable=description)
label_description.grid(column=1, row=4, sticky="w", columnspan=2)

def calculate_bmi(event=None):
    try:
        height = float(enter_height.get())
        weight = float(enter_weight.get())

        if height <= 0 or weight <= 0:
            bmi_label.config(text="Invalid input!", foreground="red")
            description.set(f"Height and weight\nmust be positive.")

            return

        bmi = weight / (height ** 2)
        bmi_label.config(text=f"BMI: {bmi:.2f}",)
        set_bmi_description(description, bmi)
    except ValueError:
        bmi_label.config(text="Enter valid numbers!", foreground="red")
        description.set("Please enter numeric values.")

def set_bmi_description(desc, value):
    if value < 18.5:
        desc.set("You are underweight!")
    elif 18.5 <= value < 25:
        desc.set("Healthy weight!")
    elif 25 <= value < 30:
        desc.set("Overweight!")
    elif 30 <= value < 35:
        desc.set("Class 1 Obesity!")
    elif 35 <= value < 40:
        desc.set("Class 2 Obesity!")
    else:
        desc.set(f"Class 3 Obesity!\n(Severe Obesity)")

def change_calculate_button_status(event=None):
    """Both fields must be filled , else button can't be clicked."""
    if enter_height.get().strip() and enter_weight.get().strip():
        calculate_button["state"] = "normal"
        root.bind("<Return>", calculate_bmi)
    else:
        calculate_button["state"] = "disabled"
        root.unbind("<Return>")


calculate_button = ttk.Button(frame, text="Calculate", command=calculate_bmi, state="disabled")
calculate_button.grid(column=1, row=2, sticky="w", padx=5, pady=5)

enter_height.bind("<KeyRelease>", change_calculate_button_status)
enter_weight.bind("<KeyRelease>", change_calculate_button_status)
root.unbind("<Return>")

root.mainloop()
