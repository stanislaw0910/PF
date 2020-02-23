from urllib.request import urlopen, URLError
from xml.etree import ElementTree as etree
import pymorphy2


def nominative(s):
    morph = pymorphy2.MorphAnalyzer()
    s = s.split()
    for i in range(len(s)):
        p = morph.parse(s[i])[0]
        s[i] = p.normal_form
    return ' '.join(s)
def fl(s):
    s = s.replace(',', '.')
    s = float(s)
    return s

def cur(day, month, year):
    d = {}
    if int(day) < 10:
        day = '0%s' % day

    if int(month) < 10:
        month = '0%s' % month

    try:
        with urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s" % (day, month, year), timeout=10) as r:
            tree = etree.parse(r)
            root = tree.getroot()
            for child in root:
                a = fl(child[4].text) / fl(child[2].text)
                if int(child[2].text) != 1:
                    s = nominative(child[3].text)
                else:
                    s = child[3].text
                d[child[1].text] = (s, a)
            d['RUB'] = ('Рубль', 1.0)
        print(day,month,year)
        return d

    except URLError:
        return 'no host given'

if __name__ == '__main__':
    pass