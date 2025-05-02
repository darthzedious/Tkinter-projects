import random
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def create_root():
    root = Tk()
    root.title("Hangman")
    root.geometry("700x300")
    root.resizable(False, False)
    return root


root = create_root()

frame = ttk.Frame(root, padding="5 5 5 5", width=800, height=400)
frame.grid(column=0, row=0, sticky="nsew")

word_frame = ttk.Frame(frame)
word_frame.grid(row=2, column=0, columnspan=10)

words = ["word", "frog", "column", "python", "elephant"]
word = StringVar()

entries = []
letters = []
max_wrong_answers = 7
letters_attempt = []
wrong_guesses = 0
image_label = None
game_over = False

victory_image = PhotoImage(file='images/victory.png')


def show_losing_image():
    """
    The function removes the already displayed image if not None.
    Finds the path for the current image depending on the turns(or 'lives') the user has left.
    Assigns the properly loaded and resized image to the variable image_label to be shown when the function is called.
    If wrong path exception case.
    """
    global image_label, losing_image

    if image_label:
        image_label.destroy()
        image_label = None

    img_path = f"images/hangman{wrong_guesses}.png"

    try:
        image = Image.open(img_path)
        image = image.resize((150, 150), Image.LANCZOS)
        losing_image = ImageTk.PhotoImage(image)

        image_label = Label(frame, image=losing_image)
        image_label.image = losing_image
        image_label.grid(row=2, column=10, columnspan=3, rowspan=5, pady=10, padx=10)
    except FileNotFoundError:
        print(f"Image not found: {img_path}")


def show_victory_image():
    """
    The function removes the already displayed image if not None.
    Assigns the properly loaded and resized image to the variable image_label to be shown when the function is called.
    """
    global image_label

    if image_label:
        image_label.destroy()
        image_label = None

    resized_victory = victory_image.subsample(3, 3)  # Resize image to 1/3 of its size
    image_label = Label(frame, image=resized_victory)
    image_label.image = resized_victory
    image_label.grid(row=2, column=10, columnspan=3,rowspan=5, pady=10, padx=10)


def on_button_click(value: str):
    """
    The function accepts the value parameter which is the letter reffering to the button pressed.
    If game_over=True or button already checked does nothing.
    Makes the button appear as pressed, checks if the value char is in the chosen word and sets it if found.
    If all letters are found calls the show_victory_image() to display the victory image,
    game_over=True, disables buttons.
    :param value: string
    """
    global letters_attempt, wrong_guesses, game_over

    if game_over or value in letters_attempt:
        return

    letters_attempt.append(value)
    buttons[value].state(["pressed"])

    if value in word.get():
        for index, char in enumerate(word.get()):
            if value == char:
                letters[index].set(char)


        if all(l.get() != "_" for l in letters):
            show_victory_image()
            game_over = True
            for button in buttons.values():
                button.state(["disabled"])

    else:
        wrong_guesses += 1
        show_losing_image()

        if wrong_guesses >= max_wrong_answers:
            game_over = True
            messagebox.showerror("Game Over", "Game Over! You lost!")
            for char, button in buttons.items():
                button.configure(state="disabled")


def display_covered_words():
    """
    Resets and initializes the game for a new round.
    - Selects a random word from the word list and sets it as the current word.
    - Clears previous game state:
      - Resets the list of attempted letters.
      - Resets the wrong guesses counter.
      - Removes any displayed hangman or victory image.
      - Destroys old entry fields used for word display.
    - Re-enables the alphabet buttons for new guesses.
    - Creates new entry fields displaying underscores for the letters of the chosen word.
    - Ensures a centered display for words of varying lengths.
    - Sets `game_over` to False, allowing the user to play a new round.

    This function is triggered when the "Play" button is pressed.
    """
    global entries, letters, wrong_guesses, letters_attempt, image_label, game_over

    alphabet_buttons()
    game_over = False

    chosen_word = random.choice(words)
    word.set(chosen_word)

    letters_attempt.clear()
    wrong_guesses = 0

    if image_label:
        image_label.destroy()
        image_label = None

    for entry in entries:
        entry.destroy()
    entries.clear()
    letters.clear()

    word_length = len(chosen_word)
    max_cols = 10
    start_index = (max_cols - word_length) // 2


    for x, char in enumerate(chosen_word):
        letter = StringVar()
        letter.set("_")
        letters.append(letter)

        entry = ttk.Entry(word_frame, width=2, textvariable=letter, font=("Arial", 20), justify="center", state="readonly")
        entry.grid(row=0, column=start_index + x, padx=5, pady=20)
        entry.insert(0, "_")
        entries.append(entry)


play_button = ttk.Button(frame, text="Play", command=display_covered_words)
play_button.grid(row=1, column=0, columnspan=10, pady=10)


buttons = {}


def alphabet_buttons():
    """
    The function aims to create a button for every letter in the alphabet.
    Each button is given the command param to execute on_button_click(char) accepting the param char
    which is the letter we want to check.
    Buttons are displayed on the main frame starting from row=3 and column=1 to column=7 respectively.
    The buttons are added to the buttons dictionary with key=char and value=button.
    """
    row, col = 3, 1
    for step in range(26):
        char = chr(97 + step)
        action = lambda x=char: on_button_click(x)

        button = ttk.Button(frame, text=char, width=2, command=action,)
        button.grid(row=row, column=col, padx=5, pady=5)
        buttons[char] = button

        col +=1
        if col > 7:
            col = 1
            row += 1


def on_keypress(event):
    """
    This function is called when the user presses a keyboard.
    If game_over=False and the character is present in the buttons and the button is not already pressed
    it calls the on_button_click function with value current key pressed.
    """
    key = event.char.lower()

    if not game_over and key in buttons and buttons[key]['state'] != 'disabled':
        on_button_click(key)

root.bind("<KeyPress>", on_keypress)

root.mainloop()
