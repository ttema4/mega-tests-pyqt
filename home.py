from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from PyQt5 import uic
from question import QuestionScreen
from new_question import NewQuestionScreen
from editor import EditScreen
from console import ConsoleScreen
import sys
import sqlite3


class HomeScreen(QWidget):  # домашнийй экран
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.test_counter = 1 if not self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall() else \
            len(self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall()) + 1
        self.initUI()

    def initUI(self):
        uic.loadUi('home.ui', self)
        self.start.clicked.connect(self.start_func)
        self.create_test.clicked.connect(self.createFunc)
        self.pushButton_3.clicked.connect(self.ex)
        self.edit_btn.clicked.connect(self.edit)
        self.edit_2.clicked.connect(self.del_all)
        self.pushButton_4.clicked.connect(self.data_base)

    def start_func(self):
        class IdException(Exception):
            pass

        class NameException(Exception):
            pass

        try:
            if (self.idSpinBox.value(),) not in self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall():
                raise IdException
            elif self.lineEdit.text() == '':
                raise NameException
        except IdException:
            QMessageBox.question(self, 'Error', "Теста с таким id ещё не создано!",
                                 QMessageBox.Ok, QMessageBox.Ok)
        except NameException:
            QMessageBox.question(self, 'Error', "Поле имя не может быть пустым!",
                                 QMessageBox.Ok, QMessageBox.Ok)
        else:
            buttonReply = QMessageBox.question(self, 'Подтверждение',
                                               f"Вы хотите пройти тест с id {self.idSpinBox.value()} "
                                               f"под именем {self.lineEdit.text()}?",
                                               QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.st = QuestionScreen(self.idSpinBox.value(), self.lineEdit.text(), self)
                self.st.move(self.x(), self.y())
                self.st.show()
                self.hide()

    def edit(self):
        tests = [str(x[0]) for x in self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall()]
        if len(tests):
            test_id, ok_pressed = QInputDialog.getItem(
                self, "Редактировние", "Выберите тест:", tests, 0, False)
            if ok_pressed:
                self.ed = EditScreen(test_id, self)
                self.ed.move(self.x(), self.y())
                self.ed.show()
                self.hide()

    def createFunc(self):
        self.name, self.ok = QInputDialog.getText(self, "Введите имя", "Как вас зовут?")
        if self.ok:
            self.st = NewQuestionScreen(self.name, self)
            self.st.move(self.x(), self.y())
            self.st.show()
            self.hide()

    def ex(self):
        buttonReply = QMessageBox.question(self, 'Exit', "Вы точно собираетесь выйти?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.con.close()
            sys.exit(0)

    def del_all(self):
        buttonReply = QMessageBox.question(self, 'DELETE ALL', "Вы уверены, что хотите удалить ВСЁ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.cur.execute("DELETE FROM qwe")
            self.cur.execute("DELETE FROM res")
            self.con.commit()
            self.hide()
            self.show()

    def data_base(self):
        self.cn = ConsoleScreen(self)
        self.cn.show()

    def showEvent(self, ev):
        self.lineEdit.setText('')
        self.test_counter = len(self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall()) + 1
        self.label_6.setText(
            f'Тестов в системе: {str(len(self.cur.execute("SELECT DISTINCT test_id FROM qwe").fetchall()))}')
        return QWidget.showEvent(self, ev)
