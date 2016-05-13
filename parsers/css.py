#
# Created by Roxane P. on 15/01/2016
# Parse fonts styles.css from fontastic or icomoon
#

import tinycss

names = []
glyphs = []
prefix = ''
fontName = ''

def parseCSS(file):
    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file(file);
    global prefix
    global fontName
    first = True
    content = False
    for rule in stylesheet.rules:
        # get raw glyph and name
        glyph = rule.declarations
        name = rule.selector.as_css().split(':', 1)[0].replace('.', '')
        if first == True:
            fontName = glyph[0].value.as_css().replace('\'', '').replace('"', '') # set fontName
            first = False
        else:
            if prefix == '': # we dont have the prefix yet
                tmp = rule.selector.as_css().split('-', 1)[0].replace('.', '')
                if tmp[0] != '[' and tmp != '':
                    prefix = tmp # set the prefix we are looking for
            if (glyph[0].value.as_css()[1] == '\\'):
                content = True # font selector with needed content appeared
            if content == True:
                glyph = glyph[0].value.as_css().replace('"', '')
                glyphs.append(glyph.lower()) # set a glyph in glyphs
            if name[0] != '[':
                names.append(name.lower()) # set a name in names
    
def get_names():
    return names;
def get_glyphs():
    return glyphs;
def get_fontName():
    return fontName;
def get_prefix():
    return prefix;
