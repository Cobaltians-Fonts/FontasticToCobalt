#
# Created by Roxane P. on 15/01/2016
# Parse fonts styles.css from fontastic or icomoon
#

import tinycss

names = []
glyphs = []
prefix = ''
debug = False

def parseCSS(file):
    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file(file);
    global prefix
    global fontName
    first = True
    content = False
    for rule in stylesheet.rules:
        if hasattr(rule, "declarations"):
            glyph = rule.declarations
            if glyph[0].name == 'content':
                cssglyph = glyph[0].value.as_css().replace('"', '').lower()
                cssname = rule.selector.as_css().split(':', 1)[0].replace('.', '').lower()
                if debug == True:
                    print '\nfont prefix:', rule.selector.as_css().split('-', 1)[0].replace('.', '')
                    print 'icon selector:', cssname
                    print 'icon value:', cssglyph
                    print 'rule attribute:', glyph[0].name
                    print 'rule priority:', glyph[0].priority
                    print 'rule column:', glyph[0].column
                    print 'rule line:', glyph[0].line
                names.append(cssname) # set a name in names
                glyphs.append(cssglyph) # set a glyph in glyphs
                if prefix == '': # set the font prefix only once
                    prefix = rule.selector.as_css().split('-', 1)[0].replace('.', '')
def get_names():
    if len(names) == 0:
        print '\033[93mWarning: parser returning empty selectors.\033[0m'
    return names;
def get_glyphs():
    if len(glyphs) == 0:
        print '\033[93mWarning: parser returning empty glyphs.\033[0m'    
    return glyphs;
def get_prefix():
    if len(prefix) == 0:
        print '\033[93mWarning: parser returning empty prefix.\033[0m'    
    return prefix;
