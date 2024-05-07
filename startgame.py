import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from random import choice, shuffle
from PyQt5.QtGui import QPixmap

class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LTO Exam Reviewer "Tagalog Version"')
        self.setGeometry(100, 100, 600, 400)

        self.questions = {
            "Ang pagmamaneho sa gabi ay delikado dahil:": ["ang distansya na kita natin ay mas maiksi pag gabi", "ang mga ilaw sa kalsada ay nakakasilaw", "mas maraming sasakyan sa kalsada sa gabi"],
            # Add more questions here...
        }

        self.current_question = None
        self.current_answers = None
        self.correct_answer = None
        self.lives = 5
        self.max_attempts = 5
        self.body_parts = 0

        self.word_label = QLabel(self)
        self.word_label.setAlignment(Qt.AlignCenter)

        self.answer_buttons = []
        for i in range(3):
            button = QPushButton('', self)
            button.clicked.connect(lambda _, idx=i: self.check_answer(idx))
            self.answer_buttons.append(button)

        self.hangman_label = QLabel(self)
        self.hangman_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.word_label)
        for button in self.answer_buttons:
            self.layout.addWidget(button)
        self.layout.addWidget(self.hangman_label)

        self.setLayout(self.layout)

        self.hangman_images = [
            "head.png",
            "left_arm.png",
            "right_arm.png",
            "left_leg.png",
            "right_leg.png",
            "exodia2.png"
        ]

        self.labels = []  # List to store hangman image labels

        self.update_hangman()  # Moved after the initialization of self.hangman_images

        self.next_question()

    def update_hangman(self):
        if self.body_parts < len(self.hangman_images):
            current_hangman_image_path = self.hangman_images[self.body_parts]
            pixmap = QPixmap(current_hangman_image_path)
            pixmap = pixmap.scaledToHeight(100)  # Set the height of the image
            label = QLabel(self)
            label.setPixmap(pixmap)

            # Calculate position based on body_parts
            if self.body_parts == 0:
                x_offset = 600  # Center the first image
                y_offset = 450
            elif self.body_parts == 1:
                x_offset = 655  # Position the second image to the right of the first
                y_offset = 450
            elif self.body_parts == 2:
                x_offset = 550  # Position the third image to the left of the first
                y_offset = 450
            elif self.body_parts == 3:
                x_offset = 655  # Position the fourth image to the right of the second
                y_offset = 481
            elif self.body_parts == 4:
                x_offset = 548
                y_offset = 481
            else:
                x_offset = 580  # Position the fifth image to the left of the third
                y_offset = 450

            label.move(x_offset, y_offset)
            label.show()  # Show the hangman image

            # Save the label reference to remove later
            self.labels.append(label)
        else:
            # Clear all previous labels
            for label in self.labels:
                label.clear()
            self.labels = []

            # Show the final hangman image
            current_hangman_image_path = self.hangman_images[-1]
            final_pixmap = QPixmap(current_hangman_image_path)
            final_pixmap = final_pixmap.scaledToHeight(100)  # Set the height of the image
            self.hangman_label.setPixmap(final_pixmap)
            self.hangman_label.move(50, 250)  # Move the final hangman image to the bottom
            self.hangman_label.show()

    def next_question(self):
        if len(self.questions) == 0:
            QMessageBox.information(self, "Game Over", "Congratulations! You've answered all questions.")
            return

        self.current_question, self.current_answers = choice(list(self.questions.items()))
        self.correct_answer = choice(self.current_answers)

        self.word_label.setText(self.current_question)

        # Shuffle the answers and assign them to the buttons
        shuffled_answers = self.current_answers.copy()
        shuffle(shuffled_answers)
        for button, answer in zip(self.answer_buttons, shuffled_answers):
            button.setText(answer)
            button.setStyleSheet("")  # Reset button style

    def check_answer(self, idx):
        selected_answer = self.answer_buttons[idx]
        if selected_answer.text() == self.correct_answer:
            del self.questions[self.current_question]
            self.next_question()
        else:
            selected_answer.setStyleSheet("background-color: red")
            self.body_parts += 1
            self.update_hangman()
            if self.body_parts == len(self.hangman_images):
                QMessageBox.information(self, "Game Over", "Game Over. The correct answer was: " + self.correct_answer)
                self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
