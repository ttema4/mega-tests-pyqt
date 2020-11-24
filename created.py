from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import pyperclip


class CreatedScreen(QWidget):  # итоги создания теста
    def __init__(self, new_test_id, parent=None):
        self.new_test_id = new_test_id
        self.parent = parent
        self.cur = self.parent.cur
        self.con = self.parent.con
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('created.ui', self)
        self.label_3.setText(f'id: {str(self.new_test_id)}')
        self.textEdit.setText(
            f'Привет! Я создал создал тест на тему "Насколько хорошо ты меня знаешь?". '
            f'Пройти его ты можешь, введя id {str(self.new_test_id)} на главном экране!')
        self.copy_btn.clicked.connect(self.copy_clicked)
        self.pushButton_3.clicked.connect(self.leave)

    def copy_clicked(self):
        self.label_5.setText('Текст успешно скопирован!')
        pyperclip.copy(self.textEdit.toPlainText())

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
