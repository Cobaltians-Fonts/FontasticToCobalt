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

    def handle_starttag(self, tag, attrs):
        for attr, v in attrs:
            if v and v.startswith('icon'):
                if v[5:] != '':
                    names.append(v[5:])
            elif v and v.startswith('f'):
                if self.i % 3 == 0 and v != 'fgc1':
                    glyphs.append('&#x' + v[0:4])
                self.i = self.i + 1;                

def parseHTML(file):
    parser = IcomoonParser()
    parser.feed(file.read())
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
