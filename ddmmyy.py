import sys
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QPushButton
from PyQt5.QtCore import QDate


def months(self):
    self.month_combo = QComboBox(self)
    now = QDate.currentDate()
    curr_mon = str(now.month())
    month_label = QLabel("Месяц", self)
    month_label.move(95, 110)

    for month_num in range(1, 13):
        self.month_combo.addItem('%d' % month_num)
    self.month_combo.setCurrentIndex(self.month_combo.findText(curr_mon))
    self.month_combo.move(95, 130)


def years(self):
    self.year_combo = QComboBox(self)
    now = QDate.currentDate()
    curr_year = str(now.year())
    month_label = QLabel("Год", self)
    month_label.move(145, 110)
    for year_num in range(1992, now.year() + 1):
        self.year_combo.addItem('%d' % year_num)
    self.year_combo.setCurrentIndex(self.year_combo.findText(curr_year))
    self.year_combo.move(145, 130)


def days(self):
    self.days_combo = QComboBox(self)
    now = QDate.currentDate()
    curr_day = str(now.day())
    days_label = QLabel("День", self)
    days_label.move(45, 110)
    for day in range(1, now.daysInMonth()+1):
        self.days_combo.addItem('%d' % day)
    self.days_combo.setCurrentIndex(self.days_combo.findText(curr_day))
    self.days_combo.move(45, 130)


def acts(self):
    curday = self.days_combo.currentText()
    month_value = int(self.month_combo.currentText())
    year_value = int(self.year_combo.currentText())
    no_day_date = QDate(year_value, month_value, 1)
    n = no_day_date.daysInMonth()
    self.days_combo.clear()
    for day in range(1, n+1):
        self.days_combo.addItem('%d' % day)
    self.days_combo.setCurrentIndex(self.days_combo.findText(curday))

if __name__ == '__main__':
    print('This is only a test')
'''
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def month(self):
        self.month_combo = QComboBox(self)
        now = QDate.currentDate()
        curr_mon = str(now.month())
        month_label = QLabel("Месяц", self)
        month_label.move(95, 110)

        for month_num in range(1, 13):
            self.month_combo.addItem('%d' % month_num)
        self.month_combo.setCurrentIndex(self.month_combo.findText(curr_mon))
        self.month_combo.move(95, 130)

    def year(self):
        self.year_combo = QComboBox(self)
        now = QDate.currentDate()
        curr_year = str(now.year())
        month_label = QLabel("Год", self)
        month_label.move(145, 110)

        for year_num in range(1992, now.year()+1):
            self.year_combo.addItem('%d' % year_num)
        self.year_combo.setCurrentIndex(self.year_combo.findText(curr_year))
        self.year_combo.move(145, 130)

    def days(self):
        self.days_combo = QComboBox(self)
        now = QDate.currentDate()
        curr_day = str(now.day())
        days_label = QLabel("День", self)
        days_label.move(45, 110)
        for day in range(1, now.daysInMonth()+1):
            self.days_combo.addItem('%d' % day)
        self.days_combo.setCurrentIndex(self.days_combo.findText(curr_day))
        self.days_combo.move(45, 130)

    def initUI(self):
        self.year()
        self.month()
        self.days()
        self.month_combo.activated[str].connect(self.act)
        self.year_combo.activated[str].connect(self.act)

        ok_button = QPushButton('OK', self)
        ok_button.resize(50, 25)
        ok_button.move(210,130)
        ok_button.clicked.connect(self.request)

        self.setGeometry(500, 300, 420, 200)
        self.setWindowTitle('CurrencyCalc')
        self.show()

    def request(self):
        day_value = self.days_combo.currentText()
        month_value = self.month_combo.currentText()
        year_value = self.year_combo.currentText()
        print(day_value, month_value, year_value)
        now = QDate.currentDate()
        print(now)

    def act(self):
        month_value = int(self.month_combo.currentText())
        year_value = int(self.year_combo.currentText())
        no_day_date = QDate(year_value, month_value, 1)
        n = no_day_date.daysInMonth()
        self.days_combo.clear()
        for day in range(1, n+1):
            self.days_combo.addItem('%d' % day)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())'''