Fontastic To Cobalt
===================

This python script will help you to include any [Fontactic](http://fontastic.me/)) fonts on your Android App. See the [How to use](#usage) below.

* This script create a standard Android module architecture.
* Parse the .html given by Fontastic, extract icons name and associated glyphs and put them into strings.xml.
* Create a basic AndroidManifest.xml and a build.gradle with [Cobalt](http://cobaltians.org/) dependency.
* Copy the font.ttf in the package's assets directory.
* Add the corresponding java code according to the Cobalt framework in the package.
* The resulting module is generated in the ./fontname directory.

Please see our [contributing guidelines](CONTRIBUTING.md) before reporting an issue.

Installation
-----------

```
git clone https://github.com/Cobaltians-Fonts/FontasticToCobalt.git
```

Usage
-----

```
python fontasticToCobalt.py icons-reference.html yourFontName.ttf
```

In Android Studio:
* Open your projet
* Select File/New/ImportModule/
* Then select the generated font module 'fontYourFontName'
* Clic Finish... Voila!
