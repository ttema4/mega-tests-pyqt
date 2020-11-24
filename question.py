from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import uic
from end import EndScreen


class QuestionScreen(QWidget):  # окно по прохождению тета
    def __init__(self, test_id, name, parent=None):
        self.test_id = test_id
        self.name = name
        self.parent = parent
        self.con = self.parent.con
        self.cur = self.parent.cur
        self.questions = self.cur.execute("SELECT DISTINCT question, var, ans FROM qwe WHERE test_id = ?",
                                          (self.test_id,)).fetchall()
        self.counter = 0
        self.ans_count = 0
        self.answers = []
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('question.ui', self)
        self.btns_update(self.questions[self.counter][1].split(';'))
        self.pushButton_3.clicked.connect(self.leave)
        self.label_2.setText(self.questions[self.counter][0])
        self.label_3.setText(f'{self.counter + 1} / {len(self.questions)}')
        self.label_5.setText(
            'Автор теста: {}'.format(
                self.cur.execute("SELECT DISTINCT autor FROM qwe WHERE test_id = ?", (self.test_id,)).fetchone()[0]))

    def delete_items_of_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def btns_update(self, btns):
        self.delete_items_of_layout(self.gridLayout)
        for i, el in enumerate(btns):
            btn = QPushButton(el, self)
            btn.clicked.connect(self.next_qu)
            if i == 0:
                self.gridLayout.addWidget(btn, 0, 0)
            elif i == 1:
                self.gridLayout.addWidget(btn, 0, 1)
            elif i == 2:
                self.gridLayout.addWidget(btn, 1, 0)
            else:
                self.gridLayout.addWidget(btn, 1, 1)

    def next_qu(self):
        if self.sender().text() == str(self.questions[self.counter][2]):
            self.ans_count += 1
        self.answers.append(self.sender().text())

        if self.counter + 1 == len(self.questions):
            self.en = EndScreen(self.test_id, self.ans_count, self.name, len(self.questions), self.answers, self.parent)
            self.en.move(self.x(), self.y())
            self.en.show()
            self.hide()
        else:
            self.counter += 1
            self.btns_update(self.questions[self.counter][1].split(';'))
            self.label_2.setText(self.questions[self.counter][0])
            self.label_3.setText(f'{self.counter + 1} / {len(self.questions)}')

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
