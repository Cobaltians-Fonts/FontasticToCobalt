Font To Cobalt
==============

This python script will help you to include any [Fontastic](http://fontastic.me/) or [Icomoon](https://icomoon.io/) fonts on your Android or IOS Cobalt App. See the [How to use](#usage) below.

* This script create a standard Android|IOS module architecture.
* Parse the .css given by Fontastic|Icomoon, extract icons name and associated glyphs and put them in the created package.
* Android: Create a basic AndroidManifest.xml, build.gradle with [Cobalt](http://cobaltians.org/) dependency, and the corresponding java code according to the Cobalt framework in the package.
* IOS: Create a basic projet with a header and some generated .m code and fill them.
* Copy the font.ttf in the package's assets directory.
* The resulting module is generated in the ./Fonts-FontName-Android|IOS directory.

Installation
-----------

```
pip install tinycss
git clone https://github.com/Cobaltians-Fonts/FontToCobalt.git
```

Usage
-----

```
python fontToCobalt.py --arch android|ios youtFontName styles.css yourfont.ttf
```

Examples
--------

```
python fontToCobalt.py styles.css yourfont.ttf
python fontToCobalt.py myFontName styles.css yourfont.ttf
python fontToCobalt.py --arch ios myFontName styles.css yourfont.ttf
```

Installation
------------

*Note:* the specified font name param must match the font name as shown in your font book (Mac) or equivalent as in the screenshot below

![Font book](https://cloud.githubusercontent.com/assets/2175246/13926054/eb4b7dbc-ef8a-11e5-9758-d86c2e6302ed.png)

In cobalt.conf:

Add this example code at the end of cobalt.conf
```
"fonts" : {
 "fa": {
   "ios": "FontsAwesome",
   "android": "org.cobaltians.fonts.fontAwesome.FontAwesomeDrawable"
 }
}
```
In Android Studio:
* Open your project
* Select File/New/ImportModule/
* Then select the generated font module 'Fonts-FontName-Android'
* Clic Finish

In Xcode:
* Open your project or workspace
* Drag and drop the generated 'Fonts-FontName-iOS' folder into your project navigator and check the "Copy items if needed" in the pop-up which appears
![Import](https://cloud.githubusercontent.com/assets/2175246/13926345/24ba3646-ef8c-11e5-9eb1-4bed0b87e4eb.png)
* Add a `Fonts provided by application` array in the .plist file of your application project with an item whose value is the filename of your font file.
![plist](https://cloud.githubusercontent.com/assets/2175246/13926575/404fb1b4-ef8d-11e5-82d4-eb236ae838f4.png)

Voila! You can now use native bars icon using the name of the icon:
```
"icon": "fa house-icon"
```
