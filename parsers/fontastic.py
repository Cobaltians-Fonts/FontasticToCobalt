#
# Created by Roxane P. on 15/01/2016
#

from HTMLParser import HTMLParser

names = []
glyphs = []

class FontasticParser (HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ulposition = 0
        
    def handle_starttag(self, tag, attrs):

        for name, value in attrs:
            if tag == 'ul':
                if value == 'glyphs css-mapping':
                    self.ulposition = 1;
                elif value == 'glyphs character-mapping':
                    self.ulposition = 2;
            if tag == 'input':
                if name == 'value':
                    if self.ulposition == 1:
                        names.append(value.replace("-", "_"))
                    elif self.ulposition == 2:
                        glyphs.append(value.replace("-", "_"))
    
def parseHTML(file):
    parser = FontasticParser()
    parser.feed(file.read())
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
