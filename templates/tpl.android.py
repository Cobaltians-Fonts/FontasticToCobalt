from string import Template

### Strings

values = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <dimen name="padding">2dp</dimen>\n    <dimen name="textSize">20sp</dimen>\n</resources>\n'

gradle = """apply plugin: 'com.android.library'

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
}\n"""

licence = """The MIT License (MIT)

Copyright (c) 2015 Cobaltians

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

### Templates

manifest = Template ("""<manifest\n    package="${packagenamekey}.fonts.font${fontkey}">\n</manifest>\n""")

javadrawable = Template("""package ${packagekey}.fonts.font${fontkey};

import android.content.Context;
import android.graphics.Color;
import android.util.Log;

import org.cobaltians.cobalt.Cobalt;
import org.cobaltians.cobalt.font.CobaltAbstractFontDrawable;

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
