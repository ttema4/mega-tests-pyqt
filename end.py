from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic, QtCore
import pyperclip


class EndScreen(QWidget):  # итоги теста
    def __init__(self, test_id, counter, name, size, answers, parent=None):
        self.test_id = test_id
        self.counter = counter
        self.name = name
        self.size = size
        self.answers = answers
        self.parent = parent
        self.con = self.parent.con
        self.cur = self.parent.cur
        self.author = self.cur.execute("SELECT DISTINCT autor FROM qwe WHERE test_id = ?", (self.test_id,)).fetchone()[
            0]
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('end.ui', self)
        self.tableWidget_2.hide()
        self.pushButton.clicked.connect(self.leave)
        self.pushButton_2.clicked.connect(self.clear)
        self.copy_btn.clicked.connect(self.copy)
        self.pushButton_3.clicked.connect(self.mistakes)
        self.label_5.setText(str(self.counter))
        self.cur.execute("INSERT INTO res VALUES (?, ?, ?)", (self.test_id, self.name, f'{self.counter} / {self.size}'))
        self.con.commit()
        self.res = self.cur.execute("SELECT name, percent FROM res WHERE test_id = ?",
                                    (self.test_id,)).fetchall()
        self.right_ans = self.cur.execute("SELECT DISTINCT question, ans FROM qwe WHERE test_id = ?",
                                          (self.test_id,)).fetchall()
        self.textEdit.setText(
            f'Привет! Я прошёл тест на тему "Насколько хорошо ты знаешь меня?" от {self.author} на {self.counter} '
            f'из {self.size}. Пройти его можешь и ты, введя id {str(self.test_id)} на главном экране!')

        self.tableWidget.setRowCount(len(self.res))
        for i in range(len(self.res)):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.res[i][j]))
        self.tableWidget.selectRow(len(self.res) - 1)
        self.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)

        self.tableWidget_2.setRowCount(len(self.answers))
        for i in range(len(self.answers)):
            for j in range(3):
                if j == 0:
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.right_ans[i][0])))
                elif j == 1:
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.answers[i])))
                else:
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.right_ans[i][1])))

    def mistakes(self):
        if self.pushButton_3.text() == 'Ошибки':
            self.pushButton_3.setText('Результаты')
            self.tableWidget.hide()
            self.pushButton_2.hide()
            self.textEdit.hide()
            self.copy_btn.hide()
            self.label_3.hide()
            self.tableWidget_2.show()
        else:
            self.pushButton_3.setText('Ошибки')
            self.tableWidget.show()
            self.pushButton_2.show()
            self.textEdit.show()
            self.copy_btn.show()
            self.label_3.show()
            self.tableWidget_2.hide()

    def clear(self):
        self.tableWidget.setRowCount(0)
        self.cur.execute("DELETE FROM res WHERE test_id = ?", (self.test_id,))
        self.con.commit()

    def copy(self):
        pyperclip.copy(self.textEdit.toPlainText())
        self.label_3.setText('Текст успешно скопирован!')

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
