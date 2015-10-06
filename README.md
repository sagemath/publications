# Sage Publications [![Build Status](https://travis-ci.org/sagemath/publications.svg?branch=master)](https://travis-ci.org/sagemath/publications)


License: GPLv2+

Authors:
* Minh Van Nguyen <mvngu.name@gmail.com>
* Harald Schilly <harald.schilly@gmail.com>

Description:

This script requires [Pybtex](https://launchpad.net/pybtex)
for parsing a BibTeX database.

Install it this way:

    $ pip install -M -U --user pybtex

The general database of publications that cite Sage is contained in the
text file named by the variable `publications_general`.
The file referred to by this variable is a BibTeX database.
Each publication entry is described in BibTeX format.
If you want to add or delete items from the publications database,
you should edit the file named by the variable `publications_general`.
Besides that,
files for `*-combinat` and `*-mupad` citations do the analogous.

Make sure that your edit follows the formatting rules of BibTeX.
Once you are done editing, call `make` to rebuild the files.

The resulting `*.html` files are macro-templates for jinja. 

To integrate the new page on the actual website,
the [website project](http://www.github.com/sagemath/website)
calls the `makefile` here and
uses the generated templates and copies over the `*.bib` files.

