#
# Created by Roxane P. on 15/01/2016
#

from HTMLParser import HTMLParser

names = []
glyphs = []

class FontasticParser (HTMLParser):
    def handle_starttag(self, tag, attrs):
        global ulmapping
        for name, value in attrs:
            if tag == 'ul':
                if value == 'glyphs css-mapping':
                    ulmapping = True;
                elif value == 'glyphs character-mapping':
                    ulmapping = False;
            if tag == 'input':
                if name == 'value':
                    if ulmapping == True:
                        names.append(value.replace("-", "_"))
                    elif ulmapping == False:
                        glyphs.append(value.replace("-", "_"))
    
def parseHTML(file):
    parser = FontasticParser()
    parser.feed(file.read())
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
