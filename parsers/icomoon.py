#
# Created by Roxane P. on 15/01/2016
#

from HTMLParser import HTMLParser
import sys

names = []
glyphs = []

# stay back ! this HTML parsing may hurt your eyes
class IcomoonParser (HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.notthistag1 = False
        self.notthistag2 = True
        self.notthistag3 = True
        self.notthistag4 = False
        self.i = 0

    def handle_starttag(self, tag, attrs):
        for attr, v in attrs:
            if attr == 'readonly':
                self.notthistag4 = True
                self.notthistag1 = True
            if attr == 'value':
                if self.notthistag4 == True and self.notthistag2 == True:
                    if self.notthistag3 == True:
                        self.i = self.i + 1
                        if self.i % 3 != 0 :
                            if self.i % 3 == 1:
                                a = ''
                                a = '&#x' + v
                                glyphs.append(a)
                            elif self.i % 3 == 2: names.append(v.split(',', 1)[0])
                        self.notthistag3 = False
                    elif self.notthistag3 == False:
                        self.i = self.i + 1
                        if self.i % 3 != 0 :
                            if self.i % 3 == 1:
                                a = ''
                                a = '&#x' + v
                                glyphs.append(a)
                            elif self.i % 3 == 2: names.append(v.split(',', 1)[0])
                        self.notthistag3 = True
                    self.notthistag2 = False
                    self.notthistag1 = False
                if self.notthistag4 == True and self.notthistag1 == True:
                    self.notthistag1 = False
                    self.notthistag2 = True
                it = False

def parseHTML(file):
    parser = IcomoonParser()
    parser.feed(file.read())
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
