#
# Created by Roxane P. on 15/01/2016
#

from HTMLParser import HTMLParser
import sys

names = []
glyphs = []

class IcomoonParser (HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.i = 0
        self.j = 0

    def handle_starttag(self, tag, attrs):
        for attr, v in attrs:
            if attr == 'value':
                if self.j % 3 == 0 :
                    glyphs.append(v)
                self.j = self.j + 1

            if tag == 'i':
                for attr in attrs:
                    print attr[1]
                    names.append(v)

def parseHTML(file):
    parser = IcomoonParser()
    parser.feed(file.read())
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
