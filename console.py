from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class ConsoleScreen(QWidget):  # Печать нынешний баз данных
    def __init__(self, parent=None):
        self.parent = parent
        self.cur = self.parent.cur
        self.con = self.parent.con
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('console.ui', self)
        self.pushButton.clicked.connect(self.create_dock)

    def add_text(self, st):
        self.textEdit.setText(self.textEdit.toPlainText() + '\n' + st)

    def create_dock(self):
        questions = self.cur.execute("SELECT DISTINCT * FROM qwe").fetchall()
        reses = self.cur.execute("SELECT DISTINCT * FROM res").fetchall()
        self.add_text('----------QUESTIONS------------')
        self.add_text('test_id\tquestions\tvar\tright ans\tauthor')
        for el in questions:
            self.add_text('\t'.join([str(el2) for el2 in el]))
        self.add_text('----------RESULTS------------')
        self.add_text('test_id\tname\tpercent')
        for el in reses:
            self.add_text('\t'.join([str(el2) for el2 in el]))
        self.add_text('-' * 25)
        self.add_text('')

    def leave(self):
        self.parent.move(self.x(), self.y())
        self.parent.show()
        self.hide()
