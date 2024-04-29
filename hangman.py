import tkinter as tk
import random
from tkinter import messagebox

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("300x200")

        self.choice_label = tk.Label(root, text="taena mo laro kaba hang na may man?")
        self.choice_label.pack()

        self.play_button = tk.Button(root, text="sge ba gago ka ah", command=self.play_game)
        self.play_button.pack()

        self.quit_button = tk.Button(root, text="yoko tangina ka", command=root.quit)
        self.quit_button.pack()

    def play_game(self):
        self.root.withdraw()  # Hide the choice window
        game_window = tk.Toplevel(self.root)
        game = Hangman(self.root, game_window)

class Hangman:
    def __init__(self, root, game_window):
        self.root = root
        self.game_window = game_window
        self.game_window.title("Hangman Game")
        self.word_list = ["tite", "pepe", "ratbu", "burat", "haha", "heheh", "huhuhu", "hfffgfg"]
        self.word = random.choice(self.word_list)
        self.guessed_letters = []
        self.attempts = 6
        self.hangman_parts = ["head", "body", "left arm", "right arm", "left leg", "right leg"]
        self.current_part = 0

        self.word_label = tk.Label(game_window, text=self.display_word())
        self.word_label.pack()

        self.attempts_label = tk.Label(game_window, text=f"Attempts left: {self.attempts}")
        self.attempts_label.pack()

        self.guess_entry = tk.Entry(game_window)
        self.guess_entry.pack()

        self.guess_button = tk.Button(game_window, text="Guess", command=self.guess_letter)
        self.guess_button.pack()

        self.message_label = tk.Label(game_window, text="")
        self.message_label.pack()

        self.canvas = tk.Canvas(game_window, width=200, height=200)
        self.canvas.pack()

        # Bind the <Return> key to trigger the "Guess" button
        self.game_window.bind("<Return>", lambda event: self.guess_button.invoke())

        # Draw the initial hangman with head and rope
        self.canvas.create_line(100, 0, 100, 50, width=4)  # Thick rope
        self.canvas.create_oval(75, 50, 125, 100, width=4)  # Oval head

    def display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def draw_hangman(self):
        if self.current_part < len(self.hangman_parts):
            if self.current_part == 1:
                # Draw body
                self.canvas.create_line(100, 100, 100, 150, width=4)
            elif self.current_part == 2:
                # Draw left arm
                self.canvas.create_line(100, 125, 75, 100, width=4)
            elif self.current_part == 3:
                # Draw right arm
                self.canvas.create_line(100, 125, 125, 100, width=4)
            elif self.current_part == 4:
                # Draw left leg
                self.canvas.create_line(100, 150, 75, 175, width=4)
            elif self.current_part == 5:
                # Draw right leg
                self.canvas.create_line(100, 150, 125, 175, width=4)

    def guess_letter(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="You've already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess not in self.word:
            self.attempts -= 1
            self.attempts_label.config(text=f"Attempts left: {self.attempts}")
            self.message_label.config(text="Incorrect!")
            self.current_part += 1
            self.draw_hangman()
            if self.attempts == 0:
                messagebox.showinfo("Game Over", f"Game Over! The word was: {self.word}")
                self.disable_input()
        else:
            self.word_label.config(text=self.display_word())
            if all(letter in self.guessed_letters for letter in self.word):
                self.message_label.config(text="Congratulations, you've guessed the word!")
                self.disable_input()

    def disable_input(self):
        self.guess_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.game_window.destroy()
        self.root.deiconify()  # Show the choice window

# Create the main window
root = tk.Tk()
app = HangmanGame(root)
root.mainloop()
