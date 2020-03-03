import sys
import pymorphy2
from PyQt5.QtWidgets import (QApplication,QLineEdit)
from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QPushButton
from urllib.request import urlopen, URLError
from xml.etree import ElementTree as etree
from ddmmyy import days, months, years, acts
from PyQt5.QtCore import QDate
from decimal import getcontext, Decimal, InvalidOperation


def nominative(s):
    morph = pymorphy2.MorphAnalyzer()
    s = s.split()
    for i in range(len(s)):
        p = morph.parse(s[i])[0]
        s[i] = p.normal_form
    return ' '.join(s)

def fl(s):
    s = s.replace(',', '.')
    s = Decimal(s).quantize(Decimal('1.01'))
    return s


def cur(day, month, year):

    global d

    if int(day) < 10:
        day = '0%s' % day

    if int(month) < 10:
        month = '0%s' % month

    try:
        with urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s" % (day, month, year), timeout=10) as r:
            tree = etree.parse(r)
            root = tree.getroot()
            d = {}
            for child in root:
                a = fl(child[4].text) / fl(child[2].text)
                if int(child[2].text) != 1:
                    s = nominative(child[3].text)
                else:
                    s = child[3].text
                d[child[1].text] = (s.capitalize(), a)
            d['RUB'] = ('Рубль', Decimal(1.0))
        print(day,month,year)

    except URLError:
        return 'no host given'


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        years(self)
        days(self)
        months(self)
        acts(self)

        ok_button = QPushButton('OK', self)
        ok_button.resize(50, 25)
        ok_button.move(210,130)

        ok_button.clicked.connect(self.request)

        self.combo = QComboBox(self)
        self.combo.move(115, 50)
        self.combo.resize(75,25)

        self.wombo = QComboBox(self)
        self.wombo.move(195, 50)
        self.wombo.resize(75, 25)

        self.result = QLineEdit(' ', self)
        self.result.resize(75, 25)
        self.result.move(275, 50)

        self.textbox = QLineEdit(self)
        self.textbox.move(45, 50)
        self.textbox.resize(65, 25)

        self.month_combo.activated[str].connect(self.act)
        self.year_combo.activated[str].connect(self.act)
        '''switch = QPushButton('<>', self)
        switch.resize(25, 25)
        switch.move(192,50)
        switch.clicked.connect(str('Fock'))'''
        self.setGeometry(500, 300, 420, 200)
        self.setWindowTitle('CurrencyCalc')
        self.show()

    def act(self):
        curday = self.days_combo.currentText()
        month_value = int(self.month_combo.currentText())
        year_value = int(self.year_combo.currentText())
        n = QDate(year_value, month_value, 1).daysInMonth()
        self.days_combo.clear()
        for day in range(1, n + 1):
            self.days_combo.addItem('%d' % day)
        if n >= int(curday):
            self.days_combo.setCurrentIndex(self.days_combo.findText(curday))
        else:
            self.days_combo.setCurrentIndex(self.days_combo.count()-1)

    def onChanged(self, text):  #changes in textbox showing in result
        x = self.cur1
        y = self.cur2
        print(x, y, type(d[y][1]))
        try:
            tex = Decimal(str(text))
            s = tex*d[x][1]/d[y][1]
            print(s)
            self.result.setText(str(s))
        except InvalidOperation:
            self.result.setText('adin')

    def request(self):
        day_value = self.days_combo.currentText()
        month_value = self.month_combo.currentText()
        year_value = self.year_combo.currentText()
        cur(day_value, month_value, year_value)

        self.combo.clear()
        self.combo.addItems(sorted(list(d)))
        self.combo.activated[str].connect(self.onActivated)
        self.cur1 = str(self.combo.currentText())
        self.combo.setToolTip(d[self.cur1][0])

        self.textbox.textEdited[str].connect(self.onChanged)

        self.wombo.clear()
        self.wombo.addItems(sorted(list(d)))
        self.wombo.activated[str].connect(self.onActivated1)
        self.cur2 = str(self.wombo.currentText())
        self.wombo.setToolTip(d[self.cur2][0])

        self.onChanged(self.textbox.text())
        print(d)

    def onActivated(self):  # Left combobox
        self.cur1 = str(self.combo.currentText())
        self.combo.setToolTip(d[self.cur1][0])
        self.onChanged(self.textbox.text())

    def onActivated1(self):   #Right combobox
        self.cur2 = str(self.wombo.currentText())
        self.wombo.setToolTip(d[self.cur2][0])
        self.onChanged(self.textbox.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
