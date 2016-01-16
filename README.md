Fontastic To Cobalt
===================

This python script will help you to include any [Fontastic](http://fontastic.me/) or [Icomoon](https://icomoon.io/) fonts on your Android or IOS Cobalt App. See the [How to use](#usage) below.

* This script create a standard Android|IOS module architecture.
* Parse the .html given by Fontastic|Icomoon, extract icons name and associated glyphs and put them in the created package.
* Android: Create a basic AndroidManifest.xml, build.gradle with [Cobalt](http://cobaltians.org/) dependency, and the corresponding java code according to the Cobalt framework in the package.
* IOS: Create a basic projet with a header and some generated .m code and fill them.
* Copy the font.ttf in the package's assets directory.
* The resulting module is generated in the ./Fonts-FontName-Android|IOS directory.

Please see our [contributing guidelines](CONTRIBUTING.md) before reporting an issue.

Installation
-----------

```
git clone https://github.com/Cobaltians-Fonts/FontasticToCobalt.git
```

Usage
-----

```
python fontasticToCobalt.py --source fontastic|icomoon --name fontname --arch android|ios icons-reference.html|Reference.html yourfont.ttf
```

In Android Studio:
* Open your projet
* Select File/New/ImportModule/
* Then select the generated font module 'fontYourFontName'
* Clic Finish... Voila!
