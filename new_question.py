from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from created import CreatedScreen


class NewQuestionScreen(QWidget):  # окно по созданию вопроса
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.con = self.parent.con
        self.cur = self.parent.cur
        self.new_test_id = self.new_min_id()
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('new_question.ui', self)
        self.checkBox.stateChanged.connect(self.show_or_hide)
        self.checkBox_2.stateChanged.connect(self.show_or_hide)
        self.pushButton.clicked.connect(self.new_q)
        self.pushButton_2.clicked.connect(self.last_qwe)
        self.pushButton_3.clicked.connect(self.leave)

    def show_or_hide(self):
        if self.sender() == self.checkBox:
            if self.lineEdit_4.isEnabled():
                if self.radioButton_4.isChecked():
                    self.radioButton.setChecked(True)
                self.lineEdit_4.setEnabled(False)
                self.radioButton_4.setEnabled(False)
            else:
                self.lineEdit_4.setEnabled(True)
                self.radioButton_4.setEnabled(True)
                self.radioButton_4.setChecked(True)
        else:
            if self.lineEdit_3.isEnabled():
                if self.radioButton_3.isChecked():
                    self.radioButton.setChecked(True)
                self.lineEdit_3.setEnabled(False)
                self.radioButton_3.setEnabled(False)
            else:
                self.lineEdit_3.setEnabled(True)
                self.radioButton_3.setEnabled(True)
                self.radioButton_3.setChecked(True)

    def get_right_ans(self):
        if self.radioButton.isChecked():
            return self.lineEdit.text()
        if self.radioButton_2.isChecked():
            return self.lineEdit_2.text()
        if self.checkBox.isChecked() and self.radioButton_4.isChecked():
            return self.lineEdit_4.text()
        if self.checkBox_2.isChecked() and self.radioButton_3.isChecked():
            return self.lineEdit_3.text()

    def get_vars(self):
        ans = []
        if self.lineEdit.text():
            ans.append(self.lineEdit.text())
        if self.lineEdit_2.text():
            ans.append(self.lineEdit_2.text())
        if self.checkBox.isChecked() and self.lineEdit_4.text():
            ans.append(self.lineEdit_4.text())
        if self.checkBox_2.isChecked() and self.lineEdit_3.text():
            ans.append(self.lineEdit_3.text())
        return ans

    def new_min_id(self):
        ids = self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall()
        for i in range(1, 999):
            if (i,) not in ids:
                return i

    def new_q(self):
        new_question = self.textEdit.toPlainText()
        new_vars = self.get_vars()
        new_ans = self.get_right_ans()
        self.cur.execute("INSERT INTO qwe VALUES (?, ?, ?, ?, ?)",
                         (self.new_test_id, new_question, ';'.join(new_vars), new_ans, self.name))
        self.textEdit.clear()
        self.label_3.setText(str(int(self.label_3.text()) + 1))
        self.radioButton.setChecked(True)

    def last_qwe(self):
        self.new_q()
        self.con.commit()
        self.cr = CreatedScreen(self.new_test_id, self.parent)
        self.cr.move(self.x(), self.y())
        self.cr.show()
        self.hide()
        self.parent.test_counter += 1

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
