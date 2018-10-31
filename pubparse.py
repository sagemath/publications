#!/usr/bin/env python

###########################################################################
# Copyright (c) 2009--2014 Minh Van Nguyen <mvngu.name@gmail.com>
#                          Harald Schilly <harald.schilly@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# http://www.gnu.org/licenses/
###########################################################################

# This script requires Pybtex for parsing a BibTeX database. See
# https://launchpad.net/pybtex for more information about Pybtex.
#
# The general database of publications that cite Sage is contained in the
# text file named by the variable publications_general. The file referred to
# by this variable is a BibTeX database. Each publication entry is described
# in BibTeX format. If you want to add or delete items from the publications
# database, you should edit the file named by the variable
# publications_general. Make sure that your edit follows the formatting rules
# of BibTeX. Once you are done editing the file named by
# publications_general, then run this script which will generate an HTML
# page listing the publications. The HTML page listing the publications has a
# link to the BibTeX database, i.e. the file referred to by the variable
# publications_database.

# importing modules from Python library
import copy
import re
import os
import sys
from pprint import pprint

# importing modules from third-party library
try:
    import pybtex
except:
    print("you have to install pybtex")
    print("$ pip install -M -U --user pybtex")
    sys.exit(1)

from pybtex.database.input import bibtex
from pybtex.style.names.plain import NameStyle
plain = NameStyle().format

# script has to run from the location where it is
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# get the current working directory
PWD = os.getcwd()

# the file containing the general publications database
publications_general = os.path.join(PWD, "bibliography-sage.bib")
# the file containing the Sage-Combinat publications database
publications_combinat = os.path.join(PWD, "Sage-Combinat.bib")
# the file containing the general bibliography formatted in HTML
html_general = os.path.join(PWD, "publications-general.html")
# the file containing the Sage-Combinat bibliography formatted in HTML
html_combinat = os.path.join(PWD, "publications-combinat.html")
# upstream version of the BibTeX database of Sage-Combinat
#bibtex_sage_combinat = "http://combinat.sagemath.org/hgwebdir.cgi/misc/raw-file/tip/articles/Sage-Combinat.bib"
# the file containing the MuPAD-Combinat BibTeX database
publications_mupad = os.path.join(PWD, "MuPAD-Combinat.bib")
# the file containing the MuPAD publications list formatted in HTML
html_mupad = os.path.join(PWD, "publications-mupad.html")
# MathSciNet
publications_mathscinet = os.path.join(PWD, 'mathscinet.bib')
html_mathscinet = os.path.join(PWD, 'publications-mathscinet.html')

# Stuff relating to file permissions.
# whether we should change the permissions of a file
CHANGE_PERMISSIONS = True
# the permissions to enforce
PERMISSIONS = "755"

# Attributes associated with each type of publication. Attribute names
# are the same as in BibTeX. In all of the publication types below, we use
# the attribute "note" to specify a valid URL where the named publication
# could be downloaded. A special exception is the case of the publication
# type "misc". This type is used for specifying both a preprint and an
# undergraduate thesis. When "misc" is used for specifying an
# undergraduate thesis, the attribute "note" contains both a valid URL and
# the word "thesis".
#
# The attributes that describe an article should be listed in this order in
# the publications database.
#
# article
# author
# title
# journal
# volume
# number
# pages
# year
# note
#
# The attributes that describe a book should be listed in this order in
# the publications database.
#
# book
# author
# title
# edition
# publisher
# year
# note
#
# The attributes that describe a work in a collection should be listed in
# this order in the publications database.
#
# incollection
# author
# title
# editor
# booktitle
# pages
# publisher
# year
# note
#
# The attributes that describe a proceedings paper should be listed in
# this order in the publications database.
#
# inproceedings
# author
# title
# editor
# booktitle
# publisher
# series
# volume
# pages
# year
# note
#
# The attributes that describe a Master's thesis should be listed in
# this order in the publications database.
#
# mastersthesis
# author
# title
# school
# address
# year
# note
#
# The attributes that describe a miscellaneous item should be listed in
# this order in the publications database. This publication type is used for
# specifying both a preprint and an undergraduate thesis. When "misc" is
# used for specifying an undergraduate thesis, the attribute "note" contains
# both a valid URL and the word "thesis".
#
# misc
# author
# title
# howpublished
# year
# note
#
# The attributes that describe a PhD thesis should be listed in
# this order in the publications database.
#
# phdthesis
# author
# title
# school
# address
# year
# note
#
# The attributes that describe a technical report should be listed in
# this order in the publications database.
#
# techreport
# author
# title
# number
# institution
# address
# year
# note
#
# The attributes that describe an unpublished work should be listed in
# this order in the publications database.
#
# unpublished
# author
# title
# month
# year
# note

##############################
# helper functions
##############################


def extract_publication(entry_dict):
    r"""
    Extract a publication entry from the given dictionary.

    INPUT:

    - entry_dict -- a dictionary containing a publication entry that was
      parsed from a BibTeX database using Pybtex.

    OUTPUT:

    A dictionary representing a publication entry, where the keys are
    BibTeX attributes for a publication type and the values corresponding to
    the keys are attribute values. An article is represented using this
    dictionary:

    {'author': <authors-names>,
     'title': <article-title>,
     'journal': <journal-name>,
     'volume': <volume-number>,
     'number': <issue-number>,
     'pages': <article-page-span>,
     'year': <publication-year>,
     'note': <url>}

    A book is represented using this dictionary:

    {'author': <authors-names>,
     'title': <book-title>,
     'edition': <book-edition>,
     'publisher': <publisher-name>,
     'year': <publication-year>,
     'note': <url>}

    A work in a collection is represented using this dictionary:

    {'author': <authors-names>,
     'title': <work-title>,
     'editor': <collection-editor>,
     'booktitle': <collection-title>,
     'pages': <work-page-span>,
     'publisher': <publisher-name>,
     'year': <publication-year>,
     'note': <url>}

    A proceedings paper is represented using this dictionary:

    {'author': <authors-names>,
     'title': <article-title>,
     'editor': <proceedings-editor>,
     'booktitle': <proceedings-title>,
     'publisher': <publisher-name>,
     'series': <series-name>,
     'volume': <volume-number>,
     'pages': <article-page-span>,
     'year': <publication-year>,
     'note': <url>}

    A Master's thesis is represented using this dictionary:

    {'author': <authors-names>,
     'title': <thesis-title>,
     'school': <school-department-name>,
     'address': <institution-address>,
     'year': <completion-year>,
     'note': <url>}

    A miscellaneous item is represented using this dictionary:

    {'author': <authors-names>,
     'title': <item-title>,
     'howpublished': <how-where-published>,
     'year': <publication-year>,
     'note': <url>}

    A PhD thesis is represented using this dictionary:

    {'author': <authors-names>,
     'title': <thesis-title>,
     'school': <school-department-name>,
     'address': <institution-address>,
     'year': <completion-year>,
     'note': <url>}

    A technical report is represented using this dictionary:

    {'author': <authors-name>,
     'title': <report-title>,
     'number': <report-number>,
     'institution': <institution-name>,
     'address': <institution-address>,
     'year': <publication-year>,
     'note': <url>}

    An unpublished manuscript is represented using this dictionary:

    {'author': <authors-names>,
     'title': <manuscript-title>,
     'month': <day-month>,
     'year': <publication-year>,
     'note': <url>}
    """
    publication_dict = {}
    for attribute in entry_dict.fields.keys():
        publication_dict.setdefault(
            str(attribute).strip().lower(),
            unicode(entry_dict.fields[attribute]).strip())
    # The author field is a required field in BibTeX format.
    # Extract author names.
    authors_str = ""
    authors_list = entry_dict.persons["author"]
    authors_str = unicode(plain(authors_list[0]).format().plaintext())
    if len(authors_list) > 1:
        for author in authors_list[1:]:
            authors_str = u"".join([
                authors_str, " and ",
                unicode(plain(author).format().plaintext())
            ])
    authors_str = authors_str.replace("<nbsp>", " ")
    publication_dict.setdefault("author", authors_str)
    # The editor field is an optional field in BibTeX format.
    # Extract editor names.
    if "editor" in entry_dict.persons:
        editors_str = ""
        editors_list = entry_dict.persons["editor"]
        editors_str = unicode(plain(editors_list[0]).format().plaintext())
        if len(editors_list) > 1:
            for editor in editors_list[1:]:
                editors_str = u"".join([
                    editors_str, " and ",
                    unicode(plain(editor).format().plaintext())
                ])
        editors_str = editors_str.replace("<nbsp>", " ")
        publication_dict.setdefault("editor", editors_str)
    return publication_dict


def filter_undergraduate_theses(publications):
    r"""
    Filter out the preprints from the undergraduate theses in the given
    list of miscellaneous publications.

    INPUT:

    - publications -- a list of dictionaries of miscellaneous publications.
      These publications include preprints and undergraduate theses.

    OUTPUT:

    Separate the preprints from the undergraduate theses. The publication
    type 'misc' is used for specifying both a preprint and an undergraduate
    thesis. When 'misc' is used for specifying an undergraduate thesis, the
    attribute 'note' contains both a valid URL and the word 'thesis'.
    """
    preprints = []
    undergraduate_theses = []
    for item in publications:
        if ("note" in item) and ("thesis" in item["note"]):
            undergraduate_theses.append(item)
        else:
            preprints.append(item)
    return {
        "preprints": preprints,
        "undergraduatetheses": undergraduate_theses
    }


def format_articles(articles):
    r"""
    Format each article in HTML format.

    INPUT:

    - articles -- a list of dictionaries of articles. All articles are
      assumed to be published, i.e. the list of articles considered does not
      contain any preprints. Use the function format_preprints() to format a
      list of preprints. Each article is required to have the following
      mandatory attributes: author, title, journal, and year. Optional
      attributes include: volume, number, pages, and note.

    OUTPUT:

    A list of articles all of which are formatted in HTML suitable for
    displaying on websites.
    """
    formatted_articles = []
    optional_attributes = ["volume", "number", "pages"]
    for article in articles:
        try:
            htmlstr = "".join([format_names(article["author"]), ". "])
            htmlstr = "".join([htmlstr, html_title(article)])
            aj = article.get("journal", article['journaltitle'])
            htmlstr = "".join([htmlstr, aj, ", "])
            for attribute in optional_attributes:
                if attribute in article:
                    htmlstr = "".join(
                        [htmlstr, attribute, " ", article[attribute], ", "])
            ay = article.get("year", article['date'])
            htmlstr = "".join([htmlstr, ay, "."])
            formatted_articles.append(htmlstr.strip())
        except Exception as ex:
            from pprint import pprint
            pprint(article)
            raise ex
    return map(replace_special, formatted_articles)


def format_books(books):
    r"""
    Format each book in HTML format.

    INPUT:

    - books -- a list of dictionaries of books. Each book must be published.
      Use the function format_unpublished() to format books that are
      unpublished. Each book is required to have the following mandatory
      attributes: author, title, publisher, and year. Optional attributes
      include: edition and note.

    OUTPUT:

    A list of books all of which are formatted in HTML suitable for
    displaying on websites.
    """
    formatted_books = []
    for book in books:
        try:
            htmlstr = "".join([format_names(book["author"]), ". "])
            htmlstr = "".join([htmlstr, html_title(book)])
            if "edition" in book:
                htmlstr = "".join([htmlstr, book["edition"], " edition, "])
            by = book.get("year", book["date"])
            htmlstr = "".join([htmlstr, book["publisher"], ", ", by, "."])
            formatted_books.append(htmlstr.strip())
        except Exception as ex:
            pprint(book)
            raise ex
    return map(replace_special, formatted_books)


def format_collections(collections):
    r"""
    Format each entry in a collection in HTML format.

    INPUT:

    - collections -- a list of dictionaries of collection entries. This
      usually means a book chapter in a book. The mandatory attributes of
      an entry in a collection are: author, title, booktitle, and year.
      Some optional attributes include: editor, pages, publisher, and note.
      Each entry in the collection must be published work.

    OUTPUT:

    A list of collection entries all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_entries = []
    for entry in collections:
        htmlstr = "".join([format_names(entry["author"]), ". "])
        htmlstr = "".join([htmlstr, html_title(entry)])
        if "editor" in entry:
            htmlstr = "".join(
                [htmlstr, "In ",
                 format_names(entry["editor"]), " (ed.). "])
        htmlstr = "".join([htmlstr, entry["booktitle"], ". "])
        if "publisher" in entry:
            htmlstr = "".join([htmlstr, entry["publisher"], ", "])
        if "pages" in entry:
            htmlstr = "".join([htmlstr, "pages ", entry["pages"], ", "])
        ay = entry.get("year", entry['date'])
        htmlstr = "".join([htmlstr, ay, "."])
        formatted_entries.append(htmlstr.strip())
    return map(replace_special, formatted_entries)


def format_masterstheses(masterstheses):
    r"""
    Format each Master's thesis in HTML format.

    INPUT:

    - masterstheses -- a list of dictionaries of Master's theses. Each
      Master's thesis has the following mandatory attributes: author, title,
      school, and year. Some optional attributes include: address and note.

    OUTPUT:

    A list of Master's theses all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_theses = []
    for thesis in masterstheses:
        htmlstr = "".join([format_names(thesis["author"]), ". "])
        htmlstr = "".join([htmlstr, html_title(thesis)])
        htmlstr = "".join([htmlstr, "Masters thesis, "])
        htmlstr = "".join([htmlstr, thesis["school"], ", "])
        if "address" in thesis:
            htmlstr = "".join([htmlstr, thesis["address"], ", "])
        htmlstr = "".join([htmlstr, thesis["year"], "."])
        formatted_theses.append(htmlstr.strip())
    return map(replace_special, formatted_theses)


def format_miscs(miscs, thesis=False):
    r"""
    Format each miscellaneous entry in HTML format. Here, a miscellaneous
    entry is usually a preprint.

    INPUT:

    - miscs -- a list of dictionaries of miscellaneous entries. There are no
      mandatory attributes. The supported optional attributes are: author,
      title, howpublished, year, and note. However, it is reasonable to
      expect that at least the following attributes are given specific
      values: author, title, and year.

    - thesis -- (default: False) True if miscs only contains undergraduate
      theses; False otherwise. If False, then miscs is assumed to only
      contain preprints.

    OUTPUT:

    A list of miscellaneous entries all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_miscs = []
    for entry in miscs:
        try:
            htmlstr = "".join([format_names(entry["author"]), ". "])
            htmlstr = "".join([htmlstr, html_title(entry)])
            if "howpublished" in entry:
                htmlstr = "".join([htmlstr, entry["howpublished"], ", "])
            if thesis:
                note = entry["note"]
                # handle the case: note = {<url> Bachelor thesis},
                if "http://" in note:
                    note = note[note.find(" "):].strip()
                htmlstr = "".join([htmlstr, note, ", "])
            y = entry.get("year", entry['date'])
            htmlstr = "".join([htmlstr, y, "."])
            formatted_miscs.append(htmlstr.strip())
        except Exception as ex:
            pprint(entry)
            raise ex
    return map(replace_special, formatted_miscs)


def format_names(names):
    r"""
    Format the given list of author names so that it's suitable for display
    on web pages.

    INPUT:

    - names -- a list of names.

    OUTPUT:

    The same list of author names, but formatted for display on web pages.
    """
    formatted_names = [name.strip() for name in names.split(" and ")]
    if len(formatted_names) == 1:
        return formatted_names[0]
    elif len(formatted_names) == 2:
        formatted_names.insert(1, " and ")
        return "".join(formatted_names)
    # the string of author names contains more than 2 names
    else:
        formatted_names.insert(-1, "and ")
        for i in xrange(len(formatted_names) - 2):
            formatted_names[i] = "".join([formatted_names[i], ", "])
        return "".join(formatted_names)


def format_phdtheses(phdtheses):
    r"""
    Format each PhD thesis in HTML format.

    INPUT:

    - phdtheses -- a list of dictionaries of PhD theses. The mandatory
      attributes of a PhD thesis are: author, title, school, and year.
      Some optional attributes include: address and note.

    OUTPUT:

    A list of PhD theses all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_theses = []
    for thesis in phdtheses:
        try:
            htmlstr = "".join([format_names(thesis["author"]), ". "])
            htmlstr = "".join([htmlstr, html_title(thesis)])
            htmlstr = "".join([htmlstr, "PhD thesis, "])
            ts = thesis.get('school', thesis['institution'])
            htmlstr = "".join([htmlstr, ts, ", "])
            if "address" in thesis:
                htmlstr = "".join([htmlstr, thesis["address"], ", "])
            ty = thesis.get('year', thesis['date'])
            htmlstr = "".join([htmlstr, ty, "."])
            formatted_theses.append(htmlstr.strip())
        except Exception as ex:
            pprint(thesis)
            raise ex
    return map(replace_special, formatted_theses)


def format_techreports(techreports):
    r"""
    Format each technical report in HTML format.

    INPUT:

    - techreports -- a list of dictionaries of technical reports. The
      mandatory attributes of a technical report are: author, title,
      institution, and year. Some optional attributes include: number,
      address, and note.

    OUTPUT:

    A list of technical reports all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_reports = []
    for report in techreports:
        htmlstr = "".join([format_names(report["author"]), ". "])
        htmlstr = "".join([htmlstr, html_title(report)])
        htmlstr = "".join([htmlstr, report["institution"], ", "])
        if "address" in report:
            htmlstr = "".join([htmlstr, report["address"], ", "])
        if "number" in report:
            htmlstr = "".join(
                [htmlstr, "technical report number ", report["number"], ", "])
        y = report.get("year", report['date'])
        htmlstr = "".join([htmlstr, y, "."])
        formatted_reports.append(htmlstr.strip())
    return map(replace_special, formatted_reports)


def format_proceedings(proceedings):
    r"""
    Format each proceedings article in HTML format.

    INPUT:

    - proceedings -- a list of dictionaries of proceedings articles. The
      mandatory attributes are: author, title, booktitle, and year. Some
      optional attributes include: editor, publisher, series, volume, pages,
      and note.

    OUTPUT:

    A list of proceedings articles all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_proceedings = []
    for article in proceedings:
        htmlstr = "".join([format_names(article["author"]), ". "])
        htmlstr = "".join([htmlstr, html_title(article)])
        if "editor" in article:
            htmlstr = "".join(
                [htmlstr, "In ",
                 format_names(article["editor"]), " (ed.). "])
        htmlstr = "".join([htmlstr, article["booktitle"], ". "])
        if "publisher" in article:
            htmlstr = "".join([htmlstr, article["publisher"], ", "])
        if "series" in article:
            htmlstr = "".join([htmlstr, article["series"], ", "])
        if "volume" in article:
            htmlstr = "".join([htmlstr, "volume ", article["volume"], ", "])
        if "pages" in article:
            if htmlstr.strip()[-1] == ".":
                htmlstr = "".join([htmlstr, "Pages ", article["pages"], ", "])
            else:
                htmlstr = "".join([htmlstr, "pages ", article["pages"], ", "])
        ay = article.get("year", article['date'])
        htmlstr = "".join([htmlstr, ay, "."])
        formatted_proceedings.append(htmlstr.strip())
    return map(replace_special, formatted_proceedings)


def format_unpublisheds(unpublisheds):
    r"""
    Format each unpublished entry in HTML format.

    INPUT:

    - unpublisheds -- a list of dictionaries of unpublished entries. An
      unpublished entry is required to have the following mandatory
      attributes: author, title, and year. Optional attributes include:
      month and note.

    OUTPUT:

    A list of unpublished entries all of which are formatted in HTML
    suitable for displaying on websites.
    """
    formatted_entries = []
    for entry in unpublisheds:
        try:
            htmlstr = "".join([format_names(entry["author"]), ". "])
            htmlstr = "".join([htmlstr, html_title(entry)])
            if "month" in entry:
                htmlstr = "".join([htmlstr, entry["month"], ", "])
            y = entry.get('year', entry['date'])
            htmlstr = "".join([htmlstr, y, "."])
            formatted_entries.append(htmlstr.strip())
        except Exception as ex:
            pprint(entry)
            raise ex
    return map(replace_special, formatted_entries)


def html_title(publication):
    r"""
    Format the title of the given publication as an HTML hyperlink. This
    depends on whether a URL is specified as part of the attributes of the
    publication.

    INPUT:

    - publication -- a publication entry. This can be an article, book, thesis
      and so on.

    OUTPUT:

    If possible, format the title of the given publication as a hyperlink.
    Here, it is assumed that the BibTeX attribute 'note' (if present)
    contains a valid URL.
    """
    url = ""
    if "note" in publication:
        url = publication["note"].split()[0]
        url = replace_special_url(url)
    # override note url's with url url's (if they exist)
    if "url" in publication:
        url = publication["url"].split()[0]
        url = replace_special_url(url)
    title = publication["title"]
    if url != "":
        if ("http://" in url) or ("https://" in url):
            return "".join(["<a href=\"", url, "\">", title, "</a>", ". "])
    # handle the case where no URL is provided or the "note" field doesn't
    # contain a URL
    return "".join([title, ". "])


def output_html(publications, filename):
    r"""
    Format each publication entry in HTML format, and output the resulting
    HTML formatted entries to a template file.
    This HTML template contains macros for the entries, which are
    included via the templating system into the actual page.

    INPUT:

    - publications -- a dictionary of publication entries. The following
      types of publications are supported: article, book, incollection,
      inproceedings, mastersthesis, misc, phdthesis, and unpublished.

    - filename -- the name of the file to write to.

    OUTPUT:

    Output the HTML formatted publication entries to the file named by
    filename. We are overwriting the content of this file.
    """
    # format the various lists of publications in HTML format
    articles = format_articles(publications["articles"])
    collections = format_collections(publications["incollections"])
    proceedings = format_proceedings(publications["inproceedings"])
    masterstheses = format_masterstheses(publications["masterstheses"])
    phdtheses = format_phdtheses(publications["phdtheses"])
    books = format_books(publications["books"])
    unpublisheds = format_unpublisheds(publications["unpublisheds"])
    miscs = filter_undergraduate_theses(publications["miscs"])
    preprints = format_miscs(miscs["preprints"])
    techreports = format_techreports(publications["techreports"])
    undergradtheses = format_miscs(miscs["undergraduatetheses"], thesis=True)

    htmlcontent = "{# DON'T EDIT! File has been autogenerated by pubparse.py #}\n"

    def macro(name, sorted_index, papers):
        ret = "\n"
        ret += "{%% macro %s() %%}\n" % name
        ret += "<ol>\n"
        for index in sorted_index:
            ret += "  <li>%s</li>\n" % papers[index]
        ret += "</ol>\n"
        ret += "{% endmacro %}\n\n"
        return ret

    # Sort the publication items. Journal articles, items in collections,
    # and proceedings papers are grouped in one section. Sort these.
    papers = articles + collections + proceedings + techreports
    sorted_index = sort_publications(
        publications["articles"] + publications["incollections"] +
        publications["inproceedings"] + publications["techreports"])
    # insert the new list of articles
    htmlcontent += macro("papers", sorted_index, papers)

    # Sort the list of theses. These include PhD, Master's, and undergraduate
    # theses.
    theses = masterstheses + phdtheses + undergradtheses
    sorted_index = sort_publications(publications["masterstheses"] +
                                     publications["phdtheses"] +
                                     miscs["undergraduatetheses"])
    # insert the new list of theses
    htmlcontent += macro("thesis", sorted_index, theses)

    # Sort the list of books. These include both published books and
    # unpublished manuscripts.
    books_list = books + unpublisheds
    sorted_index = sort_publications(publications["books"] +
                                     publications["unpublisheds"])
    htmlcontent += macro("books", sorted_index, books_list)

    # Sort the list of preprints.
    sorted_index = sort_publications(miscs["preprints"])
    htmlcontent += macro("preprints", sorted_index, preprints)

    # Replace the current publications page.
    with open(filename, "wb") as outfile:
        outfile.write(replace_maths(htmlcontent).encode("utf-8"))
        outfile.write(b"\n")

    if CHANGE_PERMISSIONS:
        os.system("".join(["chmod ", PERMISSIONS, " ", filename]))


def process_database(dbfilename):
    r"""
    Process the publications database.

    INPUT:

    - dbfilename -- the name of the publications database file to process.
      This is a BibTeX database.

    OUTPUT:

    A 9-key dictionary of processed publication entries. The number nine
    corresponds to the number of publication entries considered in this
    script. If other types of publication are added to the database besides
    the type already listed above, then the new publication type should be
    specified in the block at the beginning of this script. The 9-key
    dictionary output by this function is of the form

    {'articles': articles,
     'books': books,
     'incollections': incollections,
     'inproceedings': inproceedings,
     'masterstheses': masterstheses,
     'miscs': miscs,
     'phdtheses': phdtheses,
     'techreports': techreports,
     'unpublisheds': unpublisheds}

    where each value (corresponding to a key) in the dictionary is a list of
    processed publication entries. Each list is a dictionary of publications
    of the same type. For example, the dictionary value 'article' is a list
    of dictionaries of articles. Similarly, the dictionary value 'book' is a
    list of dictionaries of books.
    """
    # Lists of dictionaries of publication entries. Each list contains
    # several dictionaries of publication entries of the same type.
    article = []
    book = []
    incollection = []
    inproceedings = []
    mastersthesis = []
    misc = []
    phdthesis = thesis = []
    techreport = report = []
    unpublished = []
    # parse the BibTeX database
    parser = bibtex.Parser()
    bibdb = parser.parse_file(dbfilename)
    for key in bibdb.entries.keys():
        pub_type = bibdb.entries[key].type
        pub_list = locals()[pub_type]
        try:
            pub_list.append(extract_publication(bibdb.entries[key]))
        except Exception as ex:
            #raise ex
            import json
            print(key)
            print(json.dumps(bibdb.entries[key]))
            raise ex

    return {
        "articles": article,
        "books": book,
        "incollections": incollection,
        "inproceedings": inproceedings,
        "masterstheses": mastersthesis,
        "miscs": misc,
        "phdtheses": phdthesis,
        "techreports": techreport,
        "unpublisheds": unpublished
    }


def replace_maths(s):
    """
    Replace each special mathematics typesetting in the given string with
    italics.

    INPUT:

    - s -- a string in HTML format.
    """
    replace_table = [
        ("$0$", "0"), ("$_3F_2(1/4)$", "<i>_3F_2(1/4)</i>"), ("$_4$",
                                                              "<sub>4</sub>"),
        ("$\~A_2$", "&Atilde;<sub>2</sub>"), ("$f^*$", "f<sup>*</sup>"),
        ("$q$", "<i>q</i>"), ("$q=0$", "<i>q=0</i>"), ("$D$", "<i>D</i>"),
        ("$e$", "<i>e</i>"), ("$E_6$", "<i>E_6</i>"), ("$F_4$",
                                                       "F<sub>4</sub>"),
        ("$\\Gamma$",
         "&Gamma;"), ("$\\Gamma_0(9)$",
                      "&Gamma;<sub>0</sub>(9)"), ("$\\Gamma_H(N)$",
                                                  "&Gamma;<sub>H</sub>(N)"),
        ("$k$", "<i>k</i>"), ("$K$",
                              "<i>K</i>"), ("$L$",
                                            "<i>L</i>"), ("$\\mathbbF_q[t]$",
                                                          "<i>F_q[t]</i>"),
        ("$Br(k(\\mathcalC)/k)$",
         "<i>Br(k(C)/k)</i>"), ("$\\mathcalC$",
                                "<i>C</i>"), ("$\\mathcalJ$",
                                              "<i>J</i>"), ("$N$", "<i>N</i>"),
        ("$\~n$",
         "&ntilde;"), ("$p$", "<i>p</i>"), ("$PSL_2(\\mathbb Z)$",
                                            "<i>PSL_2(Z)</i>"), ("$S_n$",
                                                                 "<i>S_n</i>"),
        ("$S_N$", "<i>S_N</i>"), ("$U_7$", "<i>U_7</i>"), ("$w$", "<i>w</i>"),
        ("$Y^2=X^3+c$", "<i>Y^2=X^3+c</i>"), ("$Z_N$",
                                              "<i>Z_N</i>"), ("$\zeta(s) - c$",
                                                              "&zeta;(s) - c")
    ]
    cleansed_str = copy.copy(s)
    for candidate, target in replace_table:
        cleansed_str = cleansed_str.replace(candidate, target)
    return cleansed_str


def replace_special(entry):
    r"""
    Replace each special character from the publication entry with an
    equivalent that is suitable for display on web pages. The special
    characters we consider usually include escape sequences specific to LaTeX.

    INPUT:

    - entry -- a dictionary containing attribute/value pairs that describe
      a publication entry.

    OUTPUT:

    A dictionary containing attribute/value pairs that describes the same
    publication entry as represented by 'entry'. However, all special
    characters are replaced with equivalent characters.
    """
    replace_table = [
        ("$\\frac{1}{2}$ + \\emph{it}", "1/2 + <i>it</i>"),
        ("\\emph{via}", "<i>via</i>"),
        ("\\&", "&amp;"),  # ampersand
        ("\\'a", "&aacute;"),  # a acute
        ("\\u{a}", "&#259;"),  # a breve
        ("\\'A", "&Aacute;"),  # A acute
        ("\\`a", "&agrave;"),  # a grave
        ("\\k{a}", "&#261;"),  # a ogonek (Polish)
        ('\\"a', "&auml;"),  # a umlaut
        ("\\'{c}", "&#263;"),  # c acute (Polish)
        ("\\c{c}", "&ccedil;"),  # c cedilla
        ("\\v{c}", "&#269;"),  # c czech (Czech)
        ("\\'e", "&eacute;"),  # e acute
        ("\\'E", "&Eacute;"),  # E acute
        ("\\`e", "&egrave;"),  # e grave
        ("\\k{e}", "&#281;"),  # e ogonek (Polish)
        ('\\"e', "&euml;"),  # e umlaut
        ("\\'i", "&iacute;"),  # i acute
        ("\\`i", "&igrave;"),  # i grave
        ('\\"i', "&iuml;"),  # i umlaut
        ("\\l", "&#0322;"),  # l bar (Polish)
        ("\\tilde{n}", "&ntilde;"),  # n tilde
        ("\\'o", "&oacute;"),  # o acute
        ("\\^o", "&ocirc;"),  # o circumflex
        ("\\`o", "&ograve;"),  # o grave
        ('\\"o', "&ouml;"),  # o umlaut
        ("\\o", "&oslash;"),  # o slash
        ("\\c{s}", "&scedil;"),  # s cedilla
        ("\\c{t}", "&tcedil;"),  # t cedilla
        ("\\'u", "&uacute;"),  # u acute
        ("\\^u", "&ucirc;"),  # u circumflex
        ('\\"u', "&uuml;"),  # u umlaut
        ("\\ss", "&szlig;"),  # sz ligature
        ("\\scr{R}", "&#x211b;"),
        ("\\textsc{", ""),
        ("\\texttt{", ""),
        ("{", ""),
        ("}", "")
    ]
    cleansed_entry = copy.copy(entry)
    for candidate, target in replace_table:
        cleansed_entry = cleansed_entry.replace(candidate, target)
    return cleansed_entry


def replace_special_url(url):
    r"""
    Replace each special character in the given URL with its equivalent
    HTML encoding.

    INPUT:

    - url -- a valid URL.

    OUTPUT:

    A URL equivalent to the given URL. However, all special characters are
    replaced with their equivalent HTML encoding.
    """
    replace_table = [("&", "&amp;")]
    cleansed_url = copy.copy(url)
    for candidate, target in replace_table:
        cleansed_url = cleansed_url.replace(candidate, target)
    return cleansed_url


def sort_publications(publications):
    r"""
    Sort the given list of publications in chronological, non-decreasing
    order.

    INPUT:

    - publications -- a list of publication items. Each item in the list
      can be a journal article, a paper in a proceedings, a book, a book
      chapter, a thesis, or a preprint paper.

    OUTPUT:

    Arrange the given list of publications in chronological, non-decreasing
    order. Where two or more publication items share the same year, sort
    those items alphabetically according to the authors' last name. The output
    is a list of the same length as the given list of publications, but the
    list items are non-negative integers. Each such integer corresponds to
    the item position in the publications list. The order in which the
    integers are given in the output list corresponds to a chronological,
    non-decreasing ordering of the publications item.
    """
    publications_sorted_years = sort_by_year(publications)
    sorted_years = sorted(publications_sorted_years.keys())
    sorted_publications = []
    for year in sorted_years:
        pub_items = sort_by_name(publications_sorted_years[year])
        sorted_publications += [publications.index(item) for item in pub_items]
    return sorted_publications


def sort_by_name(publications):
    r"""
    Sort the given list of publications in alphabetical order.

    INPUT:

    - publications -- a list of publication items. Each item in the list
      can be a journal article, a paper in a proceedings, a book, a book
      chapter, a thesis, or a preprint paper. Each publication item is
      described by a dictionary of attributes.

    OUTPUT:

    Arrange the given list of publications alphabetically by authors' last
    names.
    """
    NAME_INDEX = 0
    POSITION_INDEX = 1
    author_names = [(publications[i]["author"], i)
                    for i in xrange(len(publications))]
    last_names = [(surname(author_names[i][NAME_INDEX]), i)
                  for i in xrange(len(author_names))]
    sorted_names = sorted(last_names)
    return [
        publications[sorted_names[i][POSITION_INDEX]]
        for i in xrange(len(sorted_names))
    ]


def sort_by_year(publications):
    r"""
    Sort the given list of publications in chronological, non-decreasing
    order.

    INPUT:

    - publications -- a list of publication items. Each item in the list
      can be a journal article, a paper in a proceedings, a book, a book
      chapter, a thesis, or a preprint paper. Each publication item is
      described by a dictionary of attributes.

    OUTPUT:

    Arrange the given list of publications in chronological, non-decreasing
    order. The output is a dictionary of publication year, publications list
    pairs. Each publication year is a four-digit year. The publications list
    contains items published during that year.
    """
    item_years = [(publications[i].get("year", publications[i]['date']), i)
                  for i in xrange(len(publications))]
    sorted_years = sorted(item_years)
    items_dict = {}
    for year, item in sorted_years:
        if year in items_dict:
            items_dict.setdefault(year,
                                  items_dict[year].append(publications[item]))
        else:
            items_dict.setdefault(year, [publications[item]])
    return items_dict


def surname(name):
    r"""
    Return the surname of the first author in the given string of author
    names.

    INPUT:

    - name -- a string giving the names of the authors of a publication item.
      The author names are given in the same format as per BibTeX.

    OUTPUT:

    The last name of the first author in the string of names. If the string
    of names contains only one author, then return the surname of that author.
    Where the string of names contains more than one author, only return the
    last name of the first author.
    """
    author_names = name.split(" and ")
    first_author = author_names[0].split()
    return first_author[-1]


##############################
# the script starts here
##############################

# the driver section; this is where everything starts from
if __name__ == "__main__":
    # os.system("rm " + publications_combinat)
    # os.system("wget " +  bibtex_sage_combinat)
    import sys
    if len(sys.argv) >= 2:
        what = sys.argv[1]
    else:
        what = True
    if what is True or what == "sage":
        print("  ... sage")
        db = process_database(publications_general)
        output_html(db, html_general)
    if what is True or what == "combinat":
        print("  ... combinat")
        db = process_database(publications_combinat)
        output_html(db, html_combinat)
    if what is True or what == "mupad":
        print("  ... mupad")
        db = process_database(publications_mupad)
        output_html(db, html_mupad)
    if what is True or what == "mathscinet":
        print(" ... mathscinet")
        db = process_database(publications_mathscinet)
        output_html(db, html_mathscinet)
    print("done doing %s" % ("all" if what is True else what))
