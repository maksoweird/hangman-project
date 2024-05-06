import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from random import choice, shuffle
from PyQt5.QtGui import QPixmap

class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LTO Exam Reviewer "Tagalog Version"')
        self.setGeometry(100, 100, 600, 400)

        self.questions = {
            "Ang pagmamaneho sa gabi ay delikado dahil:": ["ang distansya na kita natin ay mas maiksi pag gabi", "ang mga ilaw sa kalsada ay nakakasilaw", "mas maraming sasakyan sa kalsada sa gabi", ],
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
        self.layout.addWidget(self.hangman_label)

        answer_layout = QHBoxLayout()
        for button in self.answer_buttons:
            answer_layout.addWidget(button)
        self.layout.addLayout(answer_layout)

        self.setLayout(self.layout)

        self.hangman_images = [
            "head.png",
            "right_arm.png",
            "left_arm.png",
            "right_leg.png",
            "left_leg.png",
            "exodia2.png"
        ]

        self.update_hangman()  # Moved after the initialization of self.hangman_images

        self.next_question()

    def update_hangman(self):
        current_hangman_image_path = self.hangman_images[self.body_parts]
        pixmap = QPixmap(current_hangman_image_path)
        pixmap = pixmap.scaledToHeight(100)  # Set the height of the image
        self.hangman_label.setPixmap(pixmap)

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

    def check_answer(self, idx):
        selected_answer = self.answer_buttons[idx].text()
        if selected_answer == self.correct_answer:
            del self.questions[self.current_question]
            self.next_question()
        else:
            self.body_parts += 1
            self.update_hangman()
            if self.body_parts == len(self.hangman_images) - 1:
                QMessageBox.information(self, "Game Over", "Game Over. The correct answer was: " + self.correct_answer)
                self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
