
import sys
from PyQt5.QtWidgets import (QApplication,QLineEdit)
from PyQt5.QtWidgets import QLabel, QWidget, QComboBox
from urllib.request import urlopen, URLError
from xml.etree import ElementTree as etree


def fl(s):
    s = s.replace(',', '.')
    s = float(s)
    return s


def cur():
    di = {}
    try:
        with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as r:
            tree = etree.parse(r)
            root = tree.getroot()
            for child in root:
                a = fl(child[4].text) / fl(child[2].text)
                di[child[1].text] = (child[3].text, a)
            di['RUB'] = ('Рублей', 1.0)
        return di
    except URLError:
        return 'no host given'


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.d = cur()
        d = self.d
        if type(d) is dict:
            a = sorted(list(d))
            self.lbl1 = QLabel(d[a[0]][0], self)
            self.lbl2 = QLabel(d[a[0]][0], self)

            self.combo = QComboBox(self)
            self.combo.addItems(sorted(list(d)))
            self.combo.move(125, 50)
            self.lbl1.move(50, 150)
            self.combo.activated[str].connect(self.onActivated)
            self.cur1 = str(self.combo.currentText())

            self.wombo = QComboBox(self)
            self.wombo.addItems(sorted(list(d)))
            self.wombo.move(200, 50)
            self.lbl2.move(200, 150)
            self.wombo.activated[str].connect(self.onActivated1)
            self.cur2 = str(self.wombo.currentText())

            self.result = QLineEdit('0.0', self)
            self.result.move(300, 50)

            self.result.textEdited[str].connect(self.onChanged1)

            self.textbox = QLineEdit(self)
            self.textbox.move(45, 50)
            self.textbox.resize(65, 25)

            self.textbox.textEdited[str].connect(self.onChanged)
        else:
            self.lbl1 = QLabel("Sorry, " + d, self)
            self.lbl1.move(125, 70)
        self.setGeometry(500, 300, 450, 200)
        self.setWindowTitle('CurrencyCalc')
        self.show()

    def onChanged(self,text):  #changes in textbox showing in result
        d = self.d
        x = self.cur1
        y = self.cur2
        print(x,y)
        try:
            s = float(text)*d[x][1]/d[y][1]
            self.result.setText(str(s))
        except ValueError:
            self.result.setText(str(0.0))

    def onChanged1(self,text): #changes in result showing in textbox
        d = self.d
        x = self.cur1
        y = self.cur2
        try:
            s = float(text)/d[x][1]*d[y][1]
            self.textbox.setText(str(s))
        except ValueError:
            self.textbox.setText(str(0.0))

    def onActivated(self, x):  # Left combobox
        d = self.d
        self.lbl1.setText(d[x][0])
        self.lbl1.adjustSize()
        self.cur1 = str(self.combo.currentText())
        self.onChanged(self.cur1)

    def onActivated1(self, x):   #Right combobox
        d = self.d
        self.lbl2.setText(d[x][0])
        self.lbl2.adjustSize()
        self.cur2 = str(self.wombo.currentText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
