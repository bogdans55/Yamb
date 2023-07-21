from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, qApp, QHeaderView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import os
import sys
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from forms import start
from forms import game

class StartScreen(QMainWindow, start.Ui_StartScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.button_clicked)
        self.playButton.clicked.connect(self.open_form2)
      
    def button_clicked(self):
        sys.exit()

    def open_form2(self):
        self.second_form = Game()
        self.second_form.show()
        self.close()

class Game(QMainWindow, game.Ui_Game):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.turn = 0
        self.announced = False
        self.row_num = 16
        self.col_num = 5

        self.buttons = []
        self.played = []

        self.labels = [
            self.label1,
            self.label2,
            self.label3,
            self.label4,
            self.label5,
            self.label6
        ]
        self.checkBoxes = [
            self.checkBox_1,
            self.checkBox_2,
            self.checkBox_3,
            self.checkBox_4,
            self.checkBox_5,
            self.checkBox_6
        ]

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        for row in range(self.row_num):
            row_buttons = []
            row_states = []
            for col in range(self.col_num):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row, col, item)

                button = QPushButton()
                button.setAutoFillBackground(True)
                button.setFlat(True)
                button.setCursor(Qt.PointingHandCursor)
                button.setEnabled(False)
                if row in [6, 9, 15]:
                    button.setText('0')
                    button.setStyleSheet('background-color: #d0d0d0;border: none;')
                self.tableWidget.setCellWidget(row, col, button)

                row_buttons.append(button)
                row_states.append(button.isEnabled())
            self.buttons.append(row_buttons)
            self.played.append(row_states)
        
        self.buttons[0][0].setEnabled(True)
        self.played[0][0] = True
        self.buttons[14][1].setEnabled(True)
        self.played[14][1] = True
        for i in range(15):
            if i in [6, 9, 15]:
                continue
            self.buttons[i][2].setEnabled(True)
            self.played[i][2] = True
        for i in range(15):
            if i in [6, 9, 15]:
                continue
            self.buttons[i][3].setEnabled(True)
            self.played[i][3] = True
        for i in range(15):
            if i in [6, 9, 15]:
                continue
            self.buttons[i][4].setEnabled(True)
            self.played[i][4] = True
        
        for i in range(self.col_num):
            self.buttons[0][i].clicked.connect(self.ones)
        for i in range(self.col_num):
            self.buttons[1][i].clicked.connect(self.twos)
        for i in range(self.col_num):
            self.buttons[2][i].clicked.connect(self.threes)
        for i in range(self.col_num):
            self.buttons[3][i].clicked.connect(self.fours)
        for i in range(self.col_num):
            self.buttons[4][i].clicked.connect(self.fives)
        for i in range(self.col_num):
            self.buttons[5][i].clicked.connect(self.sixes)
        for i in range(self.col_num):
            self.buttons[7][i].clicked.connect(self.max)
        for i in range(self.col_num):
            self.buttons[8][i].clicked.connect(self.min)
        for i in range(self.col_num):
            self.buttons[10][i].clicked.connect(self.straight)
        for i in range(self.col_num):
            self.buttons[11][i].clicked.connect(self.three_of_a_kind)
        for i in range(self.col_num):
            self.buttons[12][i].clicked.connect(self.full)
        for i in range(self.col_num):
            self.buttons[13][i].clicked.connect(self.poker)
        for i in range(self.col_num):
            self.buttons[14][i].clicked.connect(self.yamb)

        self.roll()

        for i in range(6):
            self.labels[i].mousePressEvent = lambda event, index=i: self.toggle(index)

        self.dicerollButton.clicked.connect(self.roll)

    def toggle(self, index):
        self.checkBoxes[index].isChecked = not self.checkBoxes[index].isChecked

    def roll(self):
        if self.turn >= 3:
            QMessageBox.information(self, "Information", "You reached max number of rolls.")
            return

        isHand = True
        for cb in self.checkBoxes:
            if cb.isChecked():
                for i in range(self.row_num):
                    self.buttons[i][3].setEnabled(False)
                isHand = False
                break
        if isHand:
            for i in range(self.row_num):
                self.buttons[i][3].setEnabled(self.played[i][3])
            
        if self.turn != 0 and not self.announced:
            for i in range(self.row_num):
                self.buttons[i][4].setEnabled(False)
        
        dice_rolls = [random.randint(1, 6) for _ in range(6)]

        for i in range(6):
            if not self.checkBoxes[i].isChecked():
                pixmap = QPixmap('pictures/' + str(dice_rolls[i]) + '.png')
                self.labels[i].setPixmap(pixmap.scaled(100, 100, aspectRatioMode=True))
                self.labels[i].setToolTip(str(dice_rolls[i]))

        self.turn += 1

    def evaluate(self):
        values = []
        for label in self.labels:
            values.append(int(label.toolTip()))
        return values
        
    def ones(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(1 for value in values if value == 1)
        if score > 5:
            score = 5

        btn.setText(str(score))

        self.update_score(0, self.buttons[0].index(btn), score)

    def twos(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(2 for value in values if value == 2)
        if score > 10:
            score = 10

        btn.setText(str(score))

        self.update_score(1, self.buttons[1].index(btn), score)

    def threes(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(3 for value in values if value == 3)
        if score > 15:
            score = 15

        btn.setText(str(score))

        self.update_score(2, self.buttons[2].index(btn), score)

    def fours(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(4 for value in values if value == 4)
        if score > 20:
            score = 20

        btn.setText(str(score))

        self.update_score(3, self.buttons[3].index(btn), score)

    def fives(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(5 for value in values if value == 5)
        if score > 25:
            score = 25

        btn.setText(str(score))

        self.update_score(4, self.buttons[4].index(btn), score)

    def sixes(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(6 for value in values if value == 6)
        if score > 30:
            score = 30

        btn.setText(str(score))

        self.update_score(5, self.buttons[5].index(btn), score)

    def max(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(values) - min(values)

        btn.setText(str(score))

        self.update_score(7, self.buttons[7].index(btn), None)

    def min(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = sum(values) - max(values)

        btn.setText(str(score))

        self.update_score(8, self.buttons[8].index(btn), None)

    def straight(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        sorted_values = sorted(set(values))
        if sorted_values == [1,2,3,4,5,6] or sorted_values == [1,2,3,4,5] or sorted_values == [2,3,4,5,6]:
            if self.turn == 1:
                score = 66
            elif self.turn == 2:
                score = 56
            else:
                score = 46
        else:
            score = 0

        btn.setText(str(score))

        self.update_score(10, self.buttons[10].index(btn), score)
        

    def three_of_a_kind(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = 0
        for val in values:
            if values.count(val) >= 3 and 3*val > score:
                score = 3*val
        score = score + 20 if score != 0 else score

        btn.setText(str(score))

        self.update_score(11, self.buttons[11].index(btn), score)

    def full(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = 0
        for val in values:
            if values.count(val) >= 3:
                remaining_values = [n for n in values if n != val]
                for other_val in remaining_values:
                    if remaining_values.count(other_val) >= 2 and 3*val + 2*other_val > score:
                        score = 3*val + 2*other_val
        score = score + 30 if score != 0 else score

        btn.setText(str(score))

        self.update_score(12, self.buttons[12].index(btn), score)

    def poker(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = 0
        for val in values:
            if values.count(val) >= 4 and 4*val > score:
                score = 4*val
        score = score + 40 if score != 0 else score

        btn.setText(str(score))

        self.update_score(13, self.buttons[13].index(btn), score)

    def yamb(self):
        btn = qApp.focusWidget()

        values = self.evaluate()
        score = 0
        for val in values:
            if values.count(val) >= 5 and 5*val > score:
                score = 5*val
        score = score + 50 if score != 0 else score

        btn.setText(str(score))

        self.update_score(14, self.buttons[14].index(btn), score)

    def announce_move(self, row):
        self.announced = True
        for btns in self.buttons:
            for btn in btns:
                btn.setEnabled(False)
        self.buttons[row][4].setStyleSheet('background-color: #8f8f8f;border: none;')
        self.buttons[row][4].setEnabled(True)
        self.played[row][4] = True
        self.buttons[row][4].setText('')

    def announce_played(self, row):
        self.announced = False
        self.buttons[row][4].setStyleSheet('font-size: 9pt')
        for btns, states in zip(self.buttons, self.played):
            for btn, state in zip(btns, states):
                btn.setEnabled(state)

    def update_score(self, row, col, score):
        if col == 4:
            if not self.announced:
                self.announce_move(row)
                return
            else:
                self.announce_played(row)

        if row < 6:
            new_score = score + int(self.buttons[6][col].text())
            isOver = False
            for i in range(6):
                if i != row:
                    isOver |= self.buttons[i][col].text() == ''
            if isOver == False and new_score >= 60:
                new_score += 30
            self.buttons[6][col].setText(str(new_score))
        elif row > 9:
            new_score = score + int(self.buttons[15][col].text())
            self.buttons[15][col].setText(str(new_score))

        if self.buttons[7][col].text() != '' and self.buttons[8][col].text() != '' and self.buttons[0][col].text() != '':
                new_score = (int(self.buttons[7][col].text()) - int(self.buttons[8][col].text())) * int(self.buttons[0][col].text())
                self.buttons[9][col].setText(str(new_score))

        sum = 0
        for i in range(self.col_num):
            sum += int(self.buttons[6][i].text())
            sum += int(self.buttons[9][i].text())
            sum += int(self.buttons[15][i].text())

        self.buttons[row][col].setEnabled(False)
        self.played[row][col] = False
        self.scoreLabel.setText(str(sum))
        self.turn = 0
        for cb in self.checkBoxes:
            cb.setChecked(False)
        for i in range(15):
            if i in [6, 9, 15]:
                continue
            if self.buttons[i][3].text() == '':
                self.buttons[i][3].setEnabled(True)
                self.played[i][3] = True
            if self.buttons[i][4].text() == '':
                self.buttons[i][4].setEnabled(True)
                self.played[i][4] = True

        if col == 0 and row < 14:
            row = row + 1 if row in [5, 8] else row
            self.buttons[row+1][col].setEnabled(True)
            self.played[row+1][col] = True

        if col == 1 and row > 0:
            row = row - 1 if row in [7, 10] else row
            self.buttons[row-1][col].setEnabled(True)
            self.played[row-1][col] = True

        for states in self.played:
            for state in states:
                if state:
                    self.roll()
                    return
        
        QMessageBox.information(self, "The end", "Congratulations! You have completed your game. Final score is: " + str(sum))
        self.dicerollButton.setEnabled(False)
        self.checkBox_1.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.checkBox_5.setEnabled(False)
        self.checkBox_6.setEnabled(False)
        return

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = StartScreen()
    form.show()
    sys.exit(app.exec_())