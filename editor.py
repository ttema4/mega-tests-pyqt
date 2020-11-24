from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import uic


class EditScreen(QWidget):  # редактирование теста
    def __init__(self, test_id, parent=None):
        self.test_id = test_id
        self.parent = parent
        self.con = self.parent.con
        self.cur = self.parent.cur
        self.questions = self.cur.execute("SELECT DISTINCT question, var, ans FROM qwe WHERE test_id = ?",
                                          (self.test_id,)).fetchall()
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('editor.ui', self)
        self.pushButton.clicked.connect(self.leave)
        self.pushButton_2.clicked.connect(self.del_test)
        self.pushButton_3.clicked.connect(self.del_que)
        self.pushButton_4.clicked.connect(self.add_que)
        self.tableWidget.setRowCount(len(self.questions))
        for i in range(len(self.questions)):
            for j in range(3):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.questions[i][j])))

    def del_test(self):
        button_reply = QMessageBox.question(self, 'Exit', "Вы точно собираетесь удалить этот тест?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if button_reply == QMessageBox.Yes:
            self.cur.execute("DELETE FROM qwe WHERE test_id = ?", (self.test_id,))
            self.cur.execute("DELETE FROM res WHERE test_id = ?", (self.test_id,))
            self.con.commit()
            self.leave()

    def add_que(self):
        text, ok = QInputDialog.getText(self, "Добавление вопроса", "Введите новый вопрос")
        if ok:
            var, ok_p = QInputDialog.getText(self, "Варианты", "Введите варианты через ';' (до 4)")
            if ok_p:
                ans, ok_pressed = QInputDialog.getItem(
                    self, "Выбор ответа", "Выберите правильный ответ", tuple(var.split(';')), 0, False)
                if ok_pressed:
                    self.cur.execute("INSERT INTO qwe VALUES (?, ?, ?, ?, ?)",
                                     (self.test_id, text, var, ans,
                                      self.cur.execute("SELECT DISTINCT autor FROM qwe WHERE test_id = ?",
                                                       (self.test_id,)).fetchone()[0]))
                    self.con.commit()
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(text))
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(var))
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(ans))

    def del_que(self):
        row = self.tableWidget.row(self.tableWidget.selectedItems()[0])
        self.cur.execute("DELETE FROM qwe WHERE test_id = ? AND question = ?",
                         (self.test_id, self.tableWidget.item(row, 0).text()))
        self.con.commit()
        self.tableWidget.removeRow(row)

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
