#
# Created by Roxane P. on 13/01/2016
#

from HTMLParser import HTMLParser
from xml.dom.minidom import Document
from string import Template
import os, errno
import shutil
import sys

if (len(sys.argv) != 3):
    print 'Usage: python', sys.argv[0], 'icons-references.html Fontxxx.ttf'
    exit(1)

# configuration
fontname = 'fontastic'           # Change this before launching the script
fontname = fontname.title()
fontpath = 'font' + fontname + '/'
assetspath = 'font' + fontname + '/src/main/assets/'
javapath = 'font' + fontname + '/src/main/java/fr/cobaltians/fonts/font' + fontname + '/'
drawablepath = 'font' + fontname + '/src/main/res/drawable/'
valuepath = 'font' + fontname + '/src/main/res/values/'

# storage
names = []
glyphs = []

print 'Starting to create ' + fontname + ' package.' 

# creating package architecture
def mkdir_p(path):
    print 'Creating path:', path
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

print 'Creating package architecture...'
mkdir_p(assetspath)
mkdir_p(javapath)
mkdir_p(drawablepath)
mkdir_p(valuepath)
print 'All done.'

# create a subclass of HTMLParser and override the handler methods
class MyHTMLParser(HTMLParser):
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

# instantiate the parser and fed it some HTML
print 'Opening', sys.argv[1], 'and parsing HTML...',
file = open(sys.argv[1], 'r')
parser = MyHTMLParser()
parser.feed(file.read())
file.close()
print 'done.'

# Create xml file
print 'Setting strings.xml file infos...',
doc = Document()
base = doc.createElement('ressource')
doc.appendChild(base)

for i, j in zip(names, glyphs):
    entry = doc.createElement('string')
    base.appendChild(entry)
    entry.setAttribute("name"  , i)
    entry.setAttribute("translatable"  , "false")
    entry_content = doc.createTextNode(j)
    entry.appendChild(entry_content)

# store strings.xml
strings = open(valuepath + 'strings.xml', "w")
strings.write(doc.toprettyxml(indent="    ", encoding="utf-8"))
strings.close()
print 'done.'

# Create values.xml
print 'Creating values.xml...',
values = open(valuepath + 'values.xml', "w")
values.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <dimen name="padding">2dp</dimen>\n    <dimen name="textSize">20sp</dimen>\n</resources>\n')
values.close()
print 'done.'

# Create Manifest.xml
print 'Creating Manifest.xml...',
manifest = open(fontpath + 'src/main/AndroidManifest.xml', "w")
manifest.write('<manifest\n    package="fr.cobaltians.fonts.font' + fontname + '">\n</manifest>\n')
manifest.close()
print 'done.'

# Create build.gradle
print 'Creating build.gradle...',
gradle = open(fontpath + 'build.gradle', "w")
gradle.write("""apply plugin: 'com.android.library'

android {
    compileSdkVersion 23
    buildToolsVersion "23.0.2"

    defaultConfig {
        minSdkVersion 8
        targetSdkVersion 23
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
            sourceSets { main { assets.srcDirs = ['src/main/assets', 'src/main/assets/'] } }
}

dependencies {
    compile project(':cobalt')
}\n""")
gradle.close()
print 'done.'

# Copy font.ttf
path = assetspath + 'Font' + fontname + '.ttf'
print 'Copying', sys.argv[2], 'to', path, '...',
shutil.copy(sys.argv[2], path)
print 'done.'

# Create FontDrawable.java
templatefontdrawable = Template("""package fr.cobaltians.fonts.font${fontkey};

import android.content.Context;
import android.graphics.Color;
import android.util.Log;

import fr.cobaltians.cobalt.Cobalt;
import fr.cobaltians.cobalt.font.CobaltAbstractFontDrawable;

/**
 * Created by sebastienfamel on 16/10/2015.
 */
public class Font${fontkey}Drawable extends CobaltAbstractFontDrawable {
    private static final String TAG = Font${fontkey}Drawable.class.getSimpleName();

    private static final String FONT_FILE = "Font${fontkey}.ttf";
    public static final int TEXT_COLOR_LIGHT = Color.argb(153, 51, 51, 51);
    public static final int TEXT_COLOR_DARK = Color.argb(204, 255, 255, 255);

    public Font${fontkey}Drawable(Context context, String text, int color) {
        super(context, text, color, context.getResources().getDimensionPixelSize(R.dimen.textSize), context.getResources().getDimensionPixelSize(R.dimen.padding));
    }

    @Override
    protected String getStringResource(String identifier) {
        if (identifier.contains("-")) {
            identifier = identifier.replace("-", "_");
        }
        try {
            String packageName = mContext.getPackageName();
            int resourceId = mContext.getResources().getIdentifier(identifier, "string", packageName);
            if (resourceId != 0) {
                String iconId = mContext.getResources().getString(resourceId);
                return iconId;
            }
            else if (Cobalt.DEBUG) Log.e(TAG, "- getStringResource : no found resource");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }

    @Override
    protected String getFontFilePath() {
        return FONT_FILE;
    }
}
""")

path = javapath + 'Font' + fontname + 'Drawable.java'
print 'Generating ' + path + '...',
fontdrawable = open(path,'w')
fontdrawable.write(templatefontdrawable.substitute(fontkey=fontname))
fontdrawable.close()
print 'done.'

print 'All jobs done.'

exit(0)
