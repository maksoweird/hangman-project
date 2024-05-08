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
            "Ang mga seatbelt ay dapat isuot ng mga batang may edad:": ["7 taong gulang at pataas", "5 na taong gulang at pataas", "6 na taong gulang at pataas"],
            "Ano ang marapat na asal kapag ikaw ay pinara ng trapik enforcer:": ["Isuko ang lisensya at ibang dokumento kung hingin ito.", "Huminto at makipagtalo sa trapik enforcer", "Huwag pansinin ang trapik enforcer at bilisan ang patakbo papalayo"],
            "Ang magandang asal sa pagmamaneho ay ang:": ["maging defensive na drayber", "pag sugal kung may pagkakataon", "pagpapatakbo ng mabagal"],
            "Anong mga dokumento ang dapat mong dalhin tuwing nagmamaneho ka ng ""for hire"" na sasakyan": ["Professinal driver's license, at kasalukuyang or/cr", "Non-professional driver's license, at kasalukuyang or/cr", "driver' s license, at kasalukuyag or/cr"],
            "Bago makapag-apply ang isang motor vehicle ng prankisa sa DOT, ito ay dapat na nakarehistro na sa:" :["Land Transportation office","Constabulary Highway Patrol Group","Philippine Motors Association"],
            "Sa direksyon at kontrol ng trapiko, kapag ang mga traffic lights at law enforcer ay nagdidirekta sa trapiko, alin ang susundin mo upang maiwasan ang pagkalito? /nAng kotse sa ilalim ng masamang kondisyon ay nakasalalay sa:" :["Traffic enforcers","Parehong traffic light at enforcer","Traffic lights"],
            "Ang pagsususpindi ng lisensya ay nangangahulugan na:" :["ito ay pansamantalng kukunin ng LTO","ito ay permanenteng kukunin ng LTO","kailangan itong a-revalida ng LTO"],
            "Ayon sa RA 4136, ang preno sa bawat sasakyan(maliban sa isang motorsiklo) ay dapat:" :["Binubuo ng isang mahusay na foot brake at hand brake.","Binubuo ng isang mahusay na foot brake na gumagana ayon sa nilalayon","binubuo ng brake fluid sa lahat ng oras."],
            "Ang hindi marunong magbasa at sumunod sa ilaw trapiko ay:" :["maaring masangkot sa aksidente","nagpapatunay na mahusay kang drayber","nakatipid sa gasolina"]
            # Add more questions here...
        }

        self.current_question = None
        self.current_answers = None
        self.correct_answer = None
        self.lives = 5
        self.max_attempts = 5
        self.body_parts = 0
        self.right_answers = 0
        self.wrong_answers = 0

        self.word_label = QLabel(self)
        self.word_label.setAlignment(Qt.AlignCenter)

        self.answer_buttons = []
        for i in range(3):
            button = QPushButton('', self)
            button.clicked.connect(lambda _, idx=i: self.check_answer(idx))
            self.answer_buttons.append(button)

        self.hangman_label = QLabel(self)
        self.hangman_label.setAlignment(Qt.AlignCenter)

        self.play_again_button = QPushButton('Play Again', self)
        self.play_again_button.hide()
        self.play_again_button.clicked.connect(self.restart_game)

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.start_game)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.hide()
        self.quit_button.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.word_label)
        for button in self.answer_buttons:
            self.layout.addWidget(button)
        self.layout.addWidget(self.hangman_label)
        self.layout.addWidget(self.play_again_button)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.quit_button)

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

        self.load_counts()

    def load_counts(self):
        try:
            with open("counts.txt", "r") as f:
                counts = f.read().split(",")
                self.right_answers = int(counts[0])
                self.wrong_answers = int(counts[1])
        except FileNotFoundError:
            pass

    def save_counts(self):
        with open("counts.txt", "w") as f:
            f.write("{},{}".format(self.right_answers, self.wrong_answers))

    def update_hangman(self):
        if self.body_parts < len(self.hangman_images) - 1:
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
            final_pixmap = final_pixmap.scaledToHeight(300)  # Set the height of the image
            self.hangman_label.setPixmap(final_pixmap)
            self.hangman_label.move(50, 450)  # Move the final hangman image to the bottom
            self.hangman_label.show()
            self.play_again_button.show()
            self.quit_button.show()

            self.save_counts()

    def start_game(self):
        self.play_button.hide()
        self.quit_button.hide()
        self.next_question()

    def restart_game(self):
        self.play_again_button.hide()
        self.quit_button.hide()
        self.right_answers = 0
        self.wrong_answers = 0
        self.body_parts = 0
        self.update_hangman()
        self.next_question()

    def next_question(self):
        if len(self.questions) == 0:
            QMessageBox.information(self, "Game Over", "Congratulations! You've answered all questions.\nRight answers: {}\nWrong answers: {}".format(self.right_answers, self.wrong_answers))
            return

        self.current_question, self.current_answers = choice(list(self.questions.items()))
        shuffled_answers = self.current_answers.copy()
        shuffle(shuffled_answers)
        self.correct_answer = choice(shuffled_answers)

        self.word_label.setText(self.current_question)

        for button, answer in zip(self.answer_buttons, shuffled_answers):
            button.setText(answer)
            button.setStyleSheet("")  # Reset button style

    def check_answer(self, idx):
        selected_answer = self.answer_buttons[idx]
        answer_text = selected_answer.text()
        is_correct = answer_text == self.correct_answer

        if is_correct:
            self.right_answers += 1
            del self.questions[self.current_question]
            self.next_question()
        else:
            self.wrong_answers += 1
            selected_answer.setStyleSheet("background-color: red")
            self.body_parts += 1
            self.update_hangman()
            if self.body_parts == len(self.hangman_images):
                QMessageBox.information(self, "Game Over", "Game Over. The correct answer was: " + self.correct_answer)
                self.play_again_button.show()
                self.quit_button.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
