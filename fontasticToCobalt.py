#
# Created by Roxane P. on 13/01/2016
#

from HTMLParser import HTMLParser
from xml.dom.minidom import Document
from string import Template
import os, errno
import shutil
import sys
import imp

class bcolors:
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        BOLD = '\033[1m'
        ENDC = '\033[0m'

# configuration
fontname = 'awesome'           # Change this before launching the script
fontname = fontname.title()
packagename = 'org.cobaltians'
debug = True

# todo: package to create with optional parameter
android = True
ios = True

try:
    androidtpl = imp.load_source('templates_android', 'templates/tpl.android.py')
    iostpl = imp.load_source('templates_ios', 'templates/tpl.ios.py')
except:
    print bcolors.FAIL + "I'm missing my templates. Exiting..." + bcolors.ENDC
    raise

try:
    fontastic_parser = imp.load_source('parsers_fontastic', 'parsers/fontastic.py')
    icomoon_parser = imp.load_source('parsers_icomoon', 'parsers/icomoon.py')
except:
    print bcolors.FAIL + "I'm missing my parsers. Exiting..." + bcolors.ENDC
    raise


if (len(sys.argv) != 4):
    print bcolors.FAIL + 'Usage: python', sys.argv[0], ' icons-references.html Fontxxx.ttf fontastic|icomoon' + bcolors.ENDC
    exit(2)

# todo: getopts -s=htmlsource | --sources=htmlsource
fontastic = False
icomoon = False
if sys.argv[3] == 'fontastic':
        fontastic = True
elif sys.argv[3] == 'icomoon':
        icomoon = True
else:
        print bcolors.FAIL + "Unknown html-type " + sys.argv[3] + ". Try 'fontastic' or 'icomoon'. Exiting..." + bcolors.ENDC
        exit(3)

# storage
names = []
glyphs = []

# Usage :
# str   : what to log
def logme(str):
    if debug == True : print str

# Usage:
# path : file path
def mkdir_p(path):
    logme('Creating path: ' + path)
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# Usage:
# name : the file name (ex: LICENCE)
# path : the path name without file name (ex: /src/main/)
# content : the content to add in the file (ex: "Copyright (c) 2015 Cobaltians...")
def generatefile(name, path, content):
    logme(bcolors.OKBLUE + 'Generating ' + path + name + '...' + bcolors.ENDC)
    file = open(path + name, "w")
    file.write(content)
    file.close

def copyfile(src, dst):
    logme(bcolors.OKBLUE + 'Copying ' + src + ' to ' + dst + '...' + bcolors.ENDC)
    shutil.copy(src, dst)

# Starting to parse HTML
logme('Opening ' + sys.argv[1] + ' and parsing HTML...')
file = open(sys.argv[1], 'r')

# IcoMoon parsing
if icomoon == True:
        icomoon_parser.parseHTML(file)
        names = icomoon_parser.get_names()
        glyphs = icomoon_parser.get_glyphs()

# fontastic parsing
elif fontastic == True:
        fontastic_parser.parseHTML(file)
        names = fontastic_parser.get_names()
        glyphs = fontastic_parser.get_glyphs()

print 'parser get', names
print 'parser get', glyphs
        
# End parsing
file.close()

# Android package architecture
packagepath = packagename.replace(".", "/") + '/'
fontpath = 'sandbox/Fonts-Font' + fontname + '-Android/'
assetspath = fontpath + 'src/main/assets/'
javapath = fontpath + 'src/main/java/' + packagepath + 'fonts/font' + fontname + '/'
drawablepath = fontpath + 'src/main/res/drawable/'
valuepath = fontpath + 'src/main/res/values/'

# IOS package architecture
iospackagepath = 'sandbox/Fonts-Font' + fontname + '-iOS/'

# Android pakage
logme(bcolors.BOLD + 'Starting to create Android ' + fontname + ' package.' + bcolors.ENDC)

# creating package architecture
mkdir_p(assetspath)
mkdir_p(javapath)
mkdir_p(drawablepath)
mkdir_p(valuepath)

# Create xml file
logme('Setting strings.xml file infos...')
doc = Document()
base = doc.createElement('resources')
doc.appendChild(base)

for name, glyph in zip(names, glyphs):
    entry = doc.createElement('string')
    base.appendChild(entry)
    entry.setAttribute("name", name)
    entry.setAttribute("translatable"  , "false")
    entry_content = doc.createTextNode(glyph)
    entry.appendChild(entry_content)

xmltxt = doc.toprettyxml(indent="    ", encoding="utf-8")
xmltxt = xmltxt.replace('&amp;', '&') # utf-8 fix
generatefile('strings.xml', valuepath, xmltxt)

# Create values.xml
generatefile('values.xml', valuepath, androidtpl.values)

# Create build.gradle
generatefile('build.gradle', fontpath, androidtpl.gradle)

# Create LICENCE file
generatefile('LICENCE', fontpath, androidtpl.licence)

# Create Manifest.xml
generatefile('AndroidManifest.xml', fontpath + 'src/main/', androidtpl.manifest.substitute(packagenamekey = packagename, fontkey = fontname))

# Create FontDrawable.java
generatefile('Font' + fontname + 'Drawable.java', javapath, androidtpl.javadrawable.substitute(fontkey=fontname, packagekey=packagename))

# Copy font.ttf
path = assetspath + 'Font' + fontname + '.ttf'
copyfile(sys.argv[2], path)

####### IOS packaging

if ios == True : logme(bcolors.BOLD + 'Starting to create IOS ' + fontname + ' package.' + bcolors.ENDC)

prefix = 'f' + fontname[0]
upperprefix = prefix.upper()    # ex: home -> @FAhome
lowerprefix = prefix.lower()    # ex: fontAwesome -> fa

# identifier list generation: glass -> fa-glass
identifiers = []

for name in names:
    identifiers.append(lowerprefix + '-' +  name.replace("_", "-"))

# dictionary token string generation: fa-glass,FAglass -> tmp[@"fa-glass"]= @(FAglass);\n
tokenlist = ''
nbglyph = len(glyphs)
it = 1

for identifier, glyph in zip(identifiers, glyphs):
    tokenlist = tokenlist + '        @"' + identifier + '": ' + glyph + '"'
    if it != nbglyph:
        tokenlist = tokenlist + ',\n'
    it = it + 1
tokenlist = tokenlist.replace('&#x', '@"\u'); # converting to ios .m format todo: replace + delete ';'
tokenlist = tokenlist.strip()

# building IOS architecture
mkdir_p(iospackagepath)

# Creating FontFontastic.h
generatefile('Font' + fontname + '.h', iospackagepath, iostpl.tplfonth.substitute(fontkey = fontname))

# Creating FontFontastic.m
generatefile('Font' + fontname + '.m', iospackagepath, iostpl.tplfontm.substitute(fontkey = fontname, tokenlistkey = tokenlist))

# Creating LICENCE file
generatefile('LICENCE', iospackagepath, iostpl.licence)

# Copy font.ttf
path = iospackagepath + 'Font' + fontname + '.ttf'
copyfile(sys.argv[2], path)

print 'Jobs done:'
if android == True:
    print bcolors.OKGREEN + ' * Android ' + fontname + ' font package added.' + bcolors.ENDC
if ios == True:
    print bcolors.OKGREEN + ' * IOS ' + fontname + ' font package added.' + bcolors.ENDC
exit(0)
