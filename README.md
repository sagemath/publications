Sage Publications
-----------------

License: GPLv2+

Authors:
* Minh Van Nguyen <mvngu.name@gmail.com>

Description:

This script requires Pybtex for parsing a BibTeX database. See
https://launchpad.net/pybtex for more information about Pybtex.

Install it this way:

    $ pip install -M -U --user pybtex

The general database of publications that cite Sage is contained in the
text file named by the variable publications_general. The file referred to
by this variable is a BibTeX database. Each publication entry is described
in BibTeX format. If you want to add or delete items from the publications
database, you should edit the file named by the variable
publications_general. Make sure that your edit follows the formatting rules
of BibTeX. Once you are done editing the file named by
publications_general, then run this script which will generate an HTML
page listing the publications. The HTML page listing the publications has a
link to the BibTeX database, i.e. the file referred to by the variable
publications_database.

