#
# Created by Roxane P. on 13/01/2016
#

from xml.dom.minidom import Document
from string import Template
import os, errno
import shutil
import sys
import imp
import getopt

class bcolors:
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        BOLD = '\033[1m'
        ENDC = '\033[0m'

# defaults values
packagename = 'org.cobaltians'
version = '0.4'
debug = True
#debug = False

try:
    androidtpl = imp.load_source('templates_android', 'templates/tpl.android.py')
    iostpl = imp.load_source('templates_ios', 'templates/tpl.ios.py')
except:
    print bcolors.FAIL + "I'm missing my templates. Exiting..." + bcolors.ENDC
    raise

try:
    css_parser = imp.load_source('parsers_css', 'parsers/css.py')
except:
    print bcolors.FAIL + "I'm missing my parsers. Exiting..." + bcolors.ENDC
    raise


def main():
        names = []
        glyphs = []

        # True if user override default font name
        customFontName = False
        
        # prefix of the font (fontAwesome -> fa)
        prefix = 'icon' # default value
        
        # optional parameter
        fontname = 'cobaltians'
        fontname = fontname.title()
        
        # Use optional parameter to create only the wanted package (--arch ios|android)
        android = True
        ios = True

        # Needed parameters
        css_file_name = None
        ttf_file_name = None

        # Parse arguments
        try:
                options, remainder = getopt.getopt(sys.argv[1:], 'a:n:hv', ['arch=', 'name=', 'help'])
        except getopt.GetoptError as err:
                print str(err) # print help information and exit
                sys.exit(2)

        for opt, arg in options:
                if opt in ('-a', '--arch'):
                        if arg == 'android': ios = False
                        elif arg == 'ios': android = False
                        else:
                                print bcolors.FAIL + arg + ": this architecture is not supported yet. Try 'android' or 'ios'" + bcolors.ENDC
                                exit(1)
                elif opt in ('-h', '--help'):
                        usage()
                        sys.exit(0)
                elif opt in ('-n', '--name'):
                        logme('Set ' + arg + ' as font name.')
                        fontname = arg.title()
                        customFontName = True
                elif opt in ('-v'):
                        print 'Version', version
                        exit(0)
        try:
                css_file_name = remainder[0]
                ttf_file_name = remainder[1]
        except IndexError as exc:
                print bcolors.FAIL + 'Bad arguments, see help:' + bcolors.ENDC
                usage()
                exit(1)

        # Init css parser
        parser = css_parser

        # Opening CSS file
        logme('Opening ' + css_file_name + ' and parsing CSS...')
        try:
                parser.parseCSS(css_file_name)
        except IOError as exc:
                logme(bcolors.FAIL + 'Error: File ' + css_file_name + ' not found' + bcolors.ENDC)
                exit(4)

        # Get Result from CSS parsing
        names = parser.get_names()
        glyphs = parser.get_glyphs()
        if (customFontName == False):
                fontname = parser.get_fontName()
        prefix = parser.get_prefix()

        #print shortName(ttf_file_name)

        # Create packages
        if android == True:
                android_package_creator(fontname, prefix, names, glyphs, ttf_file_name).create()
                print bcolors.OKGREEN + ' * Android ' + fontname + ' font package added.' + bcolors.ENDC
        if ios == True:
                ios_package_creator(fontname, prefix, names, glyphs, ttf_file_name).create()
                print bcolors.OKGREEN + ' * IOS ' + fontname + ' font package added.' + bcolors.ENDC

#
# Functions and class definitions
#

# print help
def usage():
        print bcolors.BOLD + 'Usage: python fontToCobalt [-a android|ios] [-n fontname] styles.css Fontxxx.ttf' + bcolors.ENDC        

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
    try:
            file = open(path + name, "w")
    except IOError as exc:
            print bcolors.FAIL + 'Error: File ' + path + name + ' not found' + bcolors.ENDC
            raise
    file.write(content)
    file.close

# Usage:
# src  : file to copy
# dst  : where to copy it
def copyfile(src, dst):
    logme(bcolors.OKBLUE + 'Copying ' + src + ' to ' + dst + '...' + bcolors.ENDC)
    shutil.copy(src, dst)
    
# Generate an Ios librairy containing the font
# fontname : name of the package
# prefix: prefix of the font name
# names : icons names
# glyphs : icons glyphs
# ttf : true type file path
class ios_package_creator(object):
        def __init__(self, fontname, prefix, names, glyphs, ttf):
                self.fontname = fontname
                self.prefix = prefix
                self.names = names
                self.glyphs = glyphs
                self.ttf = ttf

        def create(self):
                logme(bcolors.BOLD + 'Starting to create IOS ' + self.fontname + ' package.' + bcolors.ENDC)
                print self.fontname
                # Identifiers contains names of font charaters: fa_glass -> fa-glass
                identifiers = []

                for name in self.names:
                        identifiers.append(name.replace("_", "-"))

                # Token dictionary generation: fa-glass, &#xxxxx -> @"fa-glass" : @"\uxxxx",\n
                tokenlist = ''
                nbglyph = len(self.glyphs)
                it = 1
                for identifier, glyph in zip(identifiers, self.glyphs):
                        if glyph[0] == '\\':
                                glyph = '\\u' + glyph[1:] # Add 'u' after antislash \e500 -> \ue500
                        tokenlist = tokenlist + '        @"' + identifier + '": @"' + glyph + '"'
                        if it != nbglyph:
                                tokenlist = tokenlist + ',\n'
                        it = it + 1

                tokenlist = tokenlist.replace('&#x', '\u') # converting to ios .m format
                tokenlist = tokenlist.strip()

                # IOS package architecture
                iospackagepath = 'Fonts-Font' + self.fontname + '-iOS/'

                # building IOS architecture
                mkdir_p(iospackagepath)

                # Creating FontFontastic.h
                generatefile('Font' + self.fontname + '.h', iospackagepath,
                             iostpl.tplfonth.substitute(fontkey = self.fontname))

                # Creating FontFontastic.m
                generatefile('Font' + self.fontname + '.m', iospackagepath,
                             iostpl.tplfontm.substitute(fontkey = self.fontname, tokenlistkey = tokenlist))

                # Creating LICENCE file
                generatefile('LICENCE', iospackagepath, iostpl.licence)

                # Copy font.ttf
                path = iospackagepath + 'Font' + self.fontname + '.ttf'
                copyfile(self.ttf, path)

# Generate an android module containing the font
# fontname : name of the package
# prefix : prefix of the font name
# names : icons names
# glyphs : icons glyphs
# ttf : true type file path
class android_package_creator(object):
        def __init__(self, fontname, prefix, names, glyphs, ttf):
                self.fontname = fontname
                self.prefix = prefix
                self.names = names
                self.glyphs = glyphs
                self.ttf = ttf

        def create(self):
                prefixValue = '' # you can put here all your special entity ex:'&#x' '&amp'
                suffixValue = '' # ex: ';'

                logme(bcolors.BOLD + 'Starting to create Android ' + self.fontname + ' package.' + bcolors.ENDC)
                # Android package architecture
                packagepath = packagename.replace(".", "/") + '/'
                fontpath = 'Fonts-Font' + self.fontname + '-Android/'
                assetspath = fontpath + 'src/main/assets/'
                javapath = fontpath + 'src/main/java/' + packagepath + 'fonts/font' + self.fontname + '/'
                drawablepath = fontpath + 'src/main/res/drawable/'
                valuepath = fontpath + 'src/main/res/values/'

                # Creating package architecture
                mkdir_p(assetspath)
                mkdir_p(javapath)
                mkdir_p(drawablepath)
                mkdir_p(valuepath)

                # Create xml file
                logme('Setting strings.xml file infos...')
                doc = Document()
                base = doc.createElement('resources')
                doc.appendChild(base)
                
                for name, glyph in zip(self.names, self.glyphs):
                        entry = doc.createElement('string')
                        base.appendChild(entry)
                        entry.setAttribute("name", name.replace("-", "_")) # ex: glass -> fa_glass
                        entry.setAttribute("translatable"  , "false")
                        entry_content = doc.createTextNode(suffixValue + glyph.replace('\\', prefixValue))
                        entry.appendChild(entry_content)

                xmltxt = doc.toprettyxml(indent="    ", encoding="utf-8")
                xmltxt = xmltxt.replace('&amp;', '') # utf-8 fix
                generatefile('strings.xml', valuepath, xmltxt)

                # Create values.xml
                generatefile('values.xml', valuepath, androidtpl.values)

                # Create build.gradle
                generatefile('build.gradle', fontpath, androidtpl.gradle)

                # Create LICENCE file
                generatefile('LICENCE', fontpath, androidtpl.licence)

                # Create Manifest.xml
                generatefile('AndroidManifest.xml', fontpath + 'src/main/',
                             androidtpl.manifest.substitute(packagenamekey = packagename, fontkey = self.fontname))

                # Create FontDrawable.java
                generatefile('Font' + self.fontname + 'Drawable.java', javapath,
                             androidtpl.javadrawable.substitute(fontkey=self.fontname, packagekey=packagename))

                # Copy font.ttf
                path = assetspath + 'Font' + self.fontname + '.ttf'
                copyfile(self.ttf, path)

if __name__ == "__main__":
        main()
exit(0)
