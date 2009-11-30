#!/usr/bin/env python

###########################################################################
# Copyright (c) 2009 Minh Van Nguyen <nguyenminh2@gmail.com>
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

# README
#
# The database of publications that cite Sage are contained in
# the text file named by the variable publications_database. Each
# publication entry is described in the format below. If you want to add
# or delete items from the publications database, you should edit the file
# named by the variable publications_database. Make sure that your edit
# follows the formatting rules as documented below. Once you are done
# editing the file named by publications_database, then run this script
# which will generate an HTML page listing the publications. This script also
# generates a BibTeX file listing the publications in BibTeX format. The
# HTML page listing the publications has a link to this BibTeX file.

import os

# make sure we're at the directory where the script is located
os.chdir("/home/sage/www2-dev")
# get the current working directory
PWD = os.getcwd()

# the file containing the publications database
# publications_database = "publications-db.txt"
publications_database = "".join([PWD, "/www/files/publications-db.txt"])
# the file containing the bibliography formatted as per BibTeX style
# bibtex_filename = "bibliography.bib"
bibtex_filename = "".join([PWD, "/www/files/bibliography.bib"])
# the file containing the bibliography formatted in HTML
# html_filename = "library-publications.html"
html_filename = "".join([PWD, "/www/library-publications.html"])

# Stuff relating to file permissions.
# whether we should change the permissions of a file
CHANGE_PERMISSIONS = True
# the permissions to enforce
PERMISSIONS = "755"

# Attributes associated with each type of publication. Attribute names
# are the same as in BibTeX, except for the name "url". The name "url" is
# designed for the purpose of this script. In the publications database,
# each type of publication is represented as a block of lines. The first
# line describes the type of that publication, and subsequent lines give
# values for each attribute of that publication entry. For example, an
# article is represented in the following format:
#
# entry_type
# author
# title
# journal
# volume
# number
# pages
# year
# note
# url
#
# A book is represented in the following format:
#
# entry_entry
# author
# title
# publisher
# year
# url
#
# Here is a snippet of the publications database where two publication
# entries have been formatted according to the rules above:
#
# article
# William Stein and David Joyner
# SAGE: System for Algebra and Geometry Experimentation
# ACM SIGSAM Bulletin
# 39
# 2
# 61--64
# 2005
# <BLANK>
# <BLANK>
#
# book
# William Stein
# Modular Forms, A Computational Approach
# American Mathematical Society
# 2007
# http://www.ams.org/bookstore-getitem/item=gsm-79
#
# Note that each entry is separated by exactly one blank line. If there is
# no specific value for an attribute, then we use the stub "<BLANK>".
# Whenever possible, entries in the publications database should be sorted
# alphabetically according to the authors' last name. Here's a
# specification of the format of each entry in the publications database.

BLANK = "<BLANK>"

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
# url
article_attributes = [
    "author", "title", "journal", "volume", "number", "pages", "year",
    "note", "url"]

# The attributes that describe a book should be listed in this order in
# the publications database.
#
# book
# author
# title
# edition
# publisher
# year
# url
book_attributes = ["author", "title", "edition", "publisher", "year", "url"]

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
# url
incollection_attributes = [
    "author", "title", "editor", "booktitle", "pages", "publisher",
    "year", "url"]

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
# url
inproceedings_attributes = [
    "author", "title", "editor", "booktitle", "publisher", "series",
    "volume", "pages", "year", "note", "url"]

# The attributes that describe a Master's thesis should be listed in
# this order in the publications database.
#
# mastersthesis
# author
# title
# school
# address
# year
# url
mastersthesis_attributes = [
    "author", "title", "school", "address", "year", "url"]

# The attributes that describe a miscellaneous item should be listed in
# this order in the publications database.
#
# misc
# author
# title
# howpublished
# year
# note
# url
misc_attributes = ["author", "title", "howpublished", "year", "note", "url"]

# The attributes that describe a PhD thesis should be listed in
# this order in the publications database.
#
# phdthesis
# author
# title
# school
# address
# year
# url
phdthesis_attributes = ["author", "title", "school", "address", "year", "url"]

# The attributes that describe an unpublished work should be listed in
# this order in the publications database.
#
# unpublished
# author
# title
# note
# month
# year
# url
unpublished_attributes = ["author", "title", "note", "month", "year", "url"]

### helper functions ######################################################

def bibtex_citation(names, year):
    r"""
    Abbreviate the given authors' names so that the abbreviation could be
    used when citing the authors' publication.

    INPUT:

    - names -- a string of author names, each name separated by 'and' just
      as author names are separated in BibTeX format. The argument names
      is assumed to contain at least one author name.

    - year -- a year in four digits, e.g. 2009.

    OUTPUT:

    An abbreviation of the given author names. This abbreviation can be
    used when citing the authors' publication.
    """
    formatted_names = [name.strip() for name in names.split(" and ")]
    # get author names for citation; only use last name
    citation_name = ""
    if len(formatted_names) == 1:
        citation_name = formatted_names[0].split()[-1] + str(year)
    elif len(formatted_names) == 2:
        citation_name = formatted_names[0].split()[-1] + \
            formatted_names[1].split()[-1] + str(year)
    # the string of author names contains more than 2 names
    else:
        citation_name = formatted_names[0].split()[-1] + "EtAl" + str(year)
    return remove_special(citation_name)

def filter_undergraduate_theses(publications):
    r"""
    Filter out the preprints from the undergraduate theses in the given
    list of miscellaneous publications.

    INPUT:

    - publications -- a list of dictionaries of miscellaneous publications.
      These publications include preprints and undergraduate theses.

    OUTPUT:

    Separate the preprints from the undergraduate theses.
    """
    preprints = []
    undergraduate_theses = []
    for item in publications:
        if "thesis" in item["note"].strip():
            undergraduate_theses.append(item)
        else:
            preprints.append(item)
    return {"preprints": preprints,
            "undergraduatetheses": undergraduate_theses}

def format_articles(articles, output="html"):
    r"""
    Format each article in either HTML or BibTeX format.

    INPUT:

    - articles -- a list of dictionaries of articles. All articles are
      assumed to be published, i.e. the list of articles considered does not
      contain any preprints. Use the function format_preprints() to format a
      list of preprints. Each article is required to have the following
      mandatory attributes: author, title, journal, and year. Optional
      attributes include: volume, number, pages, note, and url.

    - output -- (default: 'html') the format in which to output each
      article. The supported output formats are:

      - 'html' -- output each article in HTML format suitable for displaying
        on websites.

      - 'bibtex' -- output each article in BibTeX format suitable for
        further processing using LaTeX.

    OUTPUT:

    A list of articles all of which are formatted in either HTML or BibTeX
    format.
    """
    formatted_articles = []
    if output == "html":
        # format each article in HTML format
        for article in articles:
            article_noblanks = remove_blanks(article)
            htmlstr = format_names(article_noblanks["author"]) + ". "
            htmlstr += html_title(article_noblanks)
            htmlstr += article_noblanks["journal"].strip() + ", "
            attributes = ["volume", "number", "pages"]
            for attribute in attributes:
                if attribute in article_noblanks:
                    htmlstr += attribute + " " + \
                        article_noblanks[attribute].strip() + ", "
            if "note" in article_noblanks:
                htmlstr += article_noblanks["note"].strip() + ", "
            htmlstr += article_noblanks["year"].strip() + "."
            formatted_articles.append(htmlstr.strip())
        return [replace_special(article) for article in formatted_articles]
    elif output == "bibtex":
        # format each article in BibTeX format
        for article in articles:
            article_noblanks = remove_blanks(article)
            bibtexstr = format_author_title(article_noblanks, "article")
            bibtexstr += "  journal = {" + \
                article_noblanks["journal"].strip() + "},\n"
            attributes = ["volume", "number", "pages"]
            for attribute in attributes:
                if attribute in article_noblanks:
                    bibtexstr += "  " + attribute + " = {" + \
                        article_noblanks[attribute].strip() + "},\n"
            bibtexstr += "  year = {" + article_noblanks["year"].strip() + \
                "},\n"
            if "url" in article_noblanks:
                bibtexstr += "  note = {" + article_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_articles.append(bibtexstr.strip())
        return formatted_articles
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_author_title(entry, entry_type):
    r"""
    Format the author's name and publication title in BibTeX format.

    INPUT:

    - entry -- a publication entry, e.g. article, book, thesis, etc.

    - entry_type -- the BibTeX type of the given publication entry. The
      supported BibTeX types are: article, book, incollection, inproceedings,
      mastersthesis, misc, phdthesis, and unpublished.

    OUTPUT:

    For the given publication entry, format the author's name and the entry's
    title in BibTeX format. The author's name and publication title are
    preceded by the citation name.
    """
    bibtexstr = "@" + entry_type + "{" + \
        bibtex_citation(entry["author"], entry["year"]) + ",\n"
    bibtexstr += "  author = {" + entry["author"].strip() + "},\n"
    bibtexstr += "  title = {" + entry["title"].strip() + "},\n"
    return bibtexstr

def format_books(books, output="html"):
    r"""
    Format each book in either HTML or BibTeX format.

    INPUT:

    - books -- a list of dictionaries of books. Each book must be published.
      Use the function format_unpublished() to format books that are
      unpublished. Each book is required to have the following mandatory
      attributes: author, title, publisher, and year. Optional attributes
      include: edition and url.

    - output -- (default: 'html') the format in which to output each
      book. The supported output formats are:

      - 'html' -- output each book in HTML format suitable for displaying
        on websites.

      - 'bibtex' -- output each book in BibTeX format suitable for
        further processing using LaTeX.

    OUTPUT:

    A list of books all of which are formatted in either HTML or BibTeX
    format.
    """
    formatted_books = []
    if output == "html":
        # format each book in HTML format
        for book in books:
            book_noblanks = remove_blanks(book)
            htmlstr = format_names(book_noblanks["author"]) + ". "
            htmlstr += html_title(book_noblanks)
            if "edition" in book_noblanks:
                htmlstr += book_noblanks["edition"].strip() + " edition, "
            htmlstr += book_noblanks["publisher"].strip() + ", "
            htmlstr += book_noblanks["year"].strip() + "."
            formatted_books.append(htmlstr.strip())
        return [replace_special(book) for book in formatted_books]
    elif output == "bibtex":
        # format each book in BibTeX format
        for book in books:
            book_noblanks = remove_blanks(book)
            bibtexstr = format_author_title(book_noblanks, "book")
            if "edition" in book_noblanks:
                bibtexstr += "  edition = {" + \
                    book_noblanks["edition"].strip() + "},\n"
            bibtexstr += "  publisher = {" + \
                book_noblanks["publisher"].strip() + "},\n"
            bibtexstr += "  year = {" + book_noblanks["year"].strip() + "},\n"
            if "url" in book_noblanks:
                bibtexstr += "  note = {" + book_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_books.append(bibtexstr.strip())
        return formatted_books
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_collections(collections, output="html"):
    r"""
    Format each entry in a collection in either HTML or BibTeX format.

    INPUT:

    - collections -- a list of dictionaries of collection entries. This
      usually means a book chapter in a book. The mandatory attributes of
      an entry in a collection are: author, title, booktitle, and year.
      Some optional attributes include: editor, pages, publisher, and url.
      Each entry in the collection must be published work.

    - output -- (default: 'html') the format in which to output each
      collection entry. The supported output formats are:

      - 'html' -- output each collection entry in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each collection entry in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of collection entries all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_entries = []
    if output == "html":
        # format each collection entry in HTML format
        for entry in collections:
            entry_noblanks = remove_blanks(entry)
            htmlstr = format_names(entry_noblanks["author"]) + ". "
            htmlstr += html_title(entry_noblanks)
            if "editor" in entry_noblanks:
                htmlstr += "In " + \
                    format_names(entry_noblanks["editor"]) + " (ed.). "
            htmlstr += entry_noblanks["booktitle"].strip() + ". "
            if "publisher" in entry_noblanks:
                htmlstr += entry_noblanks["publisher"].strip() + ", "
            if "pages" in entry_noblanks:
                htmlstr += "pages " + entry_noblanks["pages"] + ", "
            htmlstr += entry_noblanks["year"].strip() + "."
            formatted_entries.append(htmlstr.strip())
        return [replace_special(entry) for entry in formatted_entries]
    elif output == "bibtex":
        # format each collection entry in BibTeX format
        for entry in collections:
            entry_noblanks = remove_blanks(entry)
            bibtexstr = format_author_title(entry_noblanks, "incollection")
            if "editor" in entry_noblanks:
                bibtexstr += "  editor = {" + \
                    entry_noblanks["editor"].strip() + "},\n"
            bibtexstr += "  booktitle = {" + \
                entry_noblanks["booktitle"].strip() + "},\n"
            if "publisher" in entry_noblanks:
                bibtexstr += "  publisher = {" + \
                    entry_noblanks["publisher"].strip() + "},\n"
            if "pages" in entry_noblanks:
                bibtexstr += "  pages = {" + \
                    entry_noblanks["pages"].strip() + "},\n"
            bibtexstr += "  year = {" + entry_noblanks["year"].strip() + "},\n"
            if "url" in entry_noblanks:
                bibtexstr += "  note = {" + entry_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_entries.append(bibtexstr.strip())
        return formatted_entries
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_masterstheses(masterstheses, output="html"):
    r"""
    Format each Master's thesis in either HTML or BibTeX format.

    INPUT:

    - masterstheses -- a list of dictionaries of Master's theses. Each
      Master's thesis has the following mandatory attributes: author, title,
      school, and year. Some optional attributes include: address and url.

    - output -- (default: 'html') the format in which to output each
      Master's thesis. The supported output formats are:

      - 'html' -- output each Master's thesis in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each Master's thesis in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of Master's theses all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_theses = []
    if output == "html":
        # format each thesis in HTML format
        for thesis in masterstheses:
            thesis_noblanks = remove_blanks(thesis)
            htmlstr = format_names(thesis_noblanks["author"]) + ". "
            htmlstr += html_title(thesis_noblanks)
            htmlstr += thesis_noblanks["school"].strip() + ", "
            if "address" in thesis_noblanks:
                htmlstr += thesis_noblanks["address"].strip() + ", "
            htmlstr += thesis_noblanks["year"].strip() + "."
            formatted_theses.append(htmlstr.strip())
        return [replace_special(thesis) for thesis in formatted_theses]
    elif output == "bibtex":
        # format each thesis in BibTeX format
        for thesis in masterstheses:
            thesis_noblanks = remove_blanks(thesis)
            bibtexstr = format_author_title(thesis_noblanks, "mastersthesis")
            bibtexstr += "  school = {" + thesis_noblanks["school"].strip() + \
                "},\n"
            if "address" in thesis_noblanks:
                bibtexstr += "  address = {" + \
                    thesis_noblanks["address"].strip() + "},\n"
            bibtexstr += "  year = {" + thesis_noblanks["year"].strip() + \
                "},\n"
            if "url" in thesis_noblanks:
                bibtexstr += "  note = {" + thesis_noblanks["url"].strip() + \
                    "},\n"
            formatted_theses.append(bibtexstr.strip())
        return formatted_theses
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_misc(misc, output="html"):
    r"""
    Format each miscellaneous entry in either HTML or BibTeX format. Here,
    a miscellaneous entry is usually a preprint.

    INPUT:

    - misc -- a list of dictionaries of miscellaneous entries. There are no
      mandatory attributes. The supported optional attributes are: author,
      title, howpublished, year, note, and url. However, it is reasonable
      to expect that at least the following attributes are given specific
      values: author, title, and year.

    - output -- (default: 'html') the format in which to output each
      miscellaneous entry. The supported output formats are:

      - 'html' -- output each miscellaneous entry in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each miscellaneous entry in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of miscellaneous entries all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_miscs = []
    if output == "html":
        # format each miscellaneous entry in HTML format
        for entry in misc:
            entry_noblanks = remove_blanks(entry)
            htmlstr = format_names(entry_noblanks["author"]) + ". "
            htmlstr += html_title(entry_noblanks)
            attributes = ["howpublished", "note"]
            for attribute in attributes:
                if attribute in entry_noblanks:
                    htmlstr += entry_noblanks[attribute].strip() + ", "
            htmlstr += entry_noblanks["year"].strip() + "."
            formatted_miscs.append(htmlstr.strip())
        return [replace_special(entry) for entry in formatted_miscs]
    elif output == "bibtex":
        # format each miscellaneous entry in BibTeX format
        for entry in misc:
            entry_noblanks = remove_blanks(entry)
            bibtexstr = format_author_title(entry_noblanks, "misc")
            attributes = ["howpublished", "note"]
            for attribute in attributes:
                if attribute in entry_noblanks:
                    bibtexstr += "  " + attribute + " = {" + \
                        entry_noblanks[attribute].strip() + "},\n"
            bibtexstr += "  year = {" + entry_noblanks["year"].strip() + "},\n"
            if "url" in entry_noblanks:
                bibtexstr += "  note = {" + entry_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_miscs.append(bibtexstr.strip())
        return formatted_miscs
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_names(names):
    r"""
    Format the given list of author names so that it's suitable for display
    on web pages.

    INPUT:

    - names -- a string of author names, each name separated by 'and' just
      as author names are separated in BibTeX format. The argument names
      is assumed to contain at least one author name.

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

def format_phdtheses(phdtheses, output="html"):
    r"""
    Format each PhD thesis in either HTML or BibTeX format.

    INPUT:

    - phdtheses -- a list of dictionaries of PhD theses. The mandatory
      attributes of a PhD thesis are: author, title, school, and year.
      Some optional attributes include: address and url.

    - output -- (default: 'html') the format in which to output each
      PhD thesis. The supported output formats are:

      - 'html' -- output each PhD thesis in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each PhD thesis in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of PhD theses all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_theses = []
    if output == "html":
        # format each PhD thesis in HTML format
        for thesis in phdtheses:
            thesis_noblanks = remove_blanks(thesis)
            htmlstr = format_names(thesis_noblanks["author"]) + ". "
            htmlstr += html_title(thesis_noblanks)
            htmlstr += thesis_noblanks["school"].strip() + ", "
            if "address" in thesis_noblanks:
                htmlstr += thesis_noblanks["address"].strip() + ", "
            htmlstr += thesis_noblanks["year"].strip() + "."
            formatted_theses.append(htmlstr.strip())
        return [replace_special(thesis) for thesis in formatted_theses]
    elif output == "bibtex":
        # format each PhD thesis in BibTeX format
        for thesis in phdtheses:
            thesis_noblanks = remove_blanks(thesis)
            bibtexstr = format_author_title(thesis_noblanks, "phdthesis")
            bibtexstr += "  school = {" + thesis_noblanks["school"].strip() + \
                "},\n"
            if "address" in thesis_noblanks:
                bibtexstr += "  address = {" + \
                    thesis_noblanks["address"].strip() + "},\n"
            bibtexstr += "  year = {" + thesis_noblanks["year"].strip() + \
                "},\n"
            if "url" in thesis_noblanks:
                bibtexstr += "  note = {" + thesis_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_theses.append(bibtexstr.strip())
        return formatted_theses
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_proceedings(proceedings, output="html"):
    r"""
    Format each proceedings article in either HTML or BibTeX format.

    INPUT:

    - proceedings -- a list of dictionaries of proceedings articles. The
      mandatory attributes are: author, title, booktitle, and year. Some
      optional attributes include: editor, publisher, series, volume, pages,
      note, and url.

    - output -- (default: 'html') the format in which to output each
      proceedings article. The supported output formats are:

      - 'html' -- output each proceedings article in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each proceedings article in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of proceedings articles all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_proceedings = []
    if output == "html":
        # format each proceedings article in HTML format
        for article in proceedings:
            article_noblanks = remove_blanks(article)
            htmlstr = format_names(article_noblanks["author"]) + ". "
            htmlstr += html_title(article_noblanks)
            if "editor" in article_noblanks:
                htmlstr += "In " + format_names(article_noblanks["editor"]) + \
                    " (ed.). "
            htmlstr += article_noblanks["booktitle"].strip() + ". "
            if "publisher" in article_noblanks:
                htmlstr += article_noblanks["publisher"].strip() + ", "
            if "series" in article_noblanks:
                htmlstr += article_noblanks["series"].strip() + ", "
            attributes = ["volume", "pages"]
            for attribute in attributes:
                if attribute in article_noblanks:
                    htmlstr += attribute + " " + \
                        article_noblanks[attribute] + ", "
            if "note" in article_noblanks:
                htmlstr += article_noblanks["note"].strip() + ", "
            htmlstr += article_noblanks["year"].strip() + "."
            formatted_proceedings.append(htmlstr.strip())
        return [replace_special(article) for article in formatted_proceedings]
    elif output == "bibtex":
        # format each proceedings article in BibTeX format
        for article in proceedings:
            article_noblanks = remove_blanks(article)
            bibtexstr = format_author_title(article_noblanks, "inproceedings")
            if "editor" in article_noblanks:
                bibtexstr += "  editor = {" + \
                    article_noblanks["editor"].strip() + "},\n"
            bibtexstr += "  booktitle = {" + \
                article_noblanks["booktitle"].strip() + "},\n"
            attributes = ["publisher", "series", "volume", "pages"]
            for attribute in attributes:
                if attribute in article_noblanks:
                    bibtexstr += "  " + attribute + " = {" + \
                        article_noblanks[attribute].strip() + "},\n"
            if "url" in article_noblanks:
                bibtexstr += "  note = {" + \
                    article_noblanks["url"].strip() + "},\n"
            bibtexstr += "  year = {" + article_noblanks["year"].strip() + \
                "},\n"
            bibtexstr += "}"
            formatted_proceedings.append(bibtexstr.strip())
        return formatted_proceedings
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

def format_unpublished(unpublished, output="html"):
    r"""
    Format each unpublished entry in either HTML or BibTeX format.

    INPUT:

    - unpublished -- a list of dictionaries of unpublished entries. An
      unpublished entry is required to have the following mandatory
      attributes: author, title, and year. Optional attributes include:
      month, note, and url.

    - output -- (default: 'html') the format in which to output each
      unpublished entry. The supported output formats are:

      - 'html' -- output each unpublished entry in HTML format suitable for
        displaying on websites.

      - 'bibtex' -- output each unpublished entry in BibTeX format suitable
        for further processing using LaTeX.

    OUTPUT:

    A list of unpublished entries all of which are formatted in either HTML
    or BibTeX format.
    """
    formatted_entries = []
    if output == "html":
        # format each entry in HTML format
        for entry in unpublished:
            entry_noblanks = remove_blanks(entry)
            htmlstr = format_names(entry_noblanks["author"]) + ". "
            htmlstr += html_title(entry_noblanks)
            attributes = ["note", "month"]
            for attribute in attributes:
                if attribute in entry_noblanks:
                    htmlstr += entry_noblanks[attribute].strip() + ", "
            htmlstr += entry_noblanks["year"].strip() + "."
            formatted_entries.append(htmlstr.strip())
        return [replace_special(entry) for entry in formatted_entries]
    elif output == "bibtex":
        # format each entry in BibTeX format
        for entry in unpublished:
            entry_noblanks = remove_blanks(entry)
            bibtexstr = format_author_title(entry_noblanks, "unpublished")
            attributes = ["note", "month"]
            for attribute in attributes:
                if attribute in entry_noblanks:
                    bibtexstr += "  " + attribute + " = {" + \
                        entry_noblanks[attribute].strip() + "},\n"
            bibtexstr += "  year = {" + entry_noblanks["year"].strip() + "},\n"
            if "url" in entry_noblanks:
                bibtexstr += "  note = {" + entry_noblanks["url"].strip() + \
                    "},\n"
            bibtexstr += "}"
            formatted_entries.append(bibtexstr.strip())
        return formatted_entries
    else:
        raise ValueError("'output' must be either 'html' or 'bibtex'")

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
    """
    url = ""
    if "url" in publication:
        url = publication["url"].strip()
        url = replace_special_url(url)
    title = publication["title"].strip()
    if url != "":
        return "<a href=\"" + url + "\">" + title + "</a>" + ". "
    else:
        return title + ". "

def output_html(publications, filename):
    r"""
    Format each publication entry in HTML format, and output the resulting
    HTML formatted entries to a text file.

    INPUT:

    - publications -- a dictionary of publication entries. The following
      types of publications are supported: article, book, incollection,
      inproceedings, mastersthesis, misc, phdthesis, and unpublished.

    - filename -- the name of the file to write to.

    OUTPUT:

    Output the HTML formatted publication entries to the file named by
    filename.
    """
    # for regular expressions
    import re
    output_bibtex(publications, bibtex_filename)
    # format the various lists of publications in HTML format
    articles = format_articles(publications["articles"], output="html")
    collections = format_collections(publications["incollections"],
                                     output="html")
    proceedings = format_proceedings(publications["inproceedings"],
                                     output="html")
    masterstheses = format_masterstheses(publications["masterstheses"],
                                         output="html")
    phdtheses = format_phdtheses(publications["phdtheses"], output="html")
    books = format_books(publications["books"], output="html")
    unpublisheds = format_unpublished(publications["unpublisheds"],
                                      output="html")
    miscs = filter_undergraduate_theses(publications["miscs"])
    preprints = format_misc(miscs["preprints"], output="html")
    undergraduate_theses = format_misc(miscs["undergraduatetheses"],
                                       output="html")
    FOUR_SPACES = "    "
    # compiled regular expressions to speed up searches
    re_start_articles = re.compile(r"START_TOKEN_ARTICLES")
    re_end_articles = re.compile(r"END_TOKEN_ARTICLES")
    re_start_theses = re.compile(r"START_TOKEN_THESES")
    re_end_theses = re.compile(r"END_TOKEN_THESES")
    re_start_books = re.compile(r"START_TOKEN_BOOKS")
    re_end_books = re.compile(r"END_TOKEN_BOOKS")
    re_start_preprints = re.compile(r"START_TOKEN_PREPRINTS")
    re_end_preprints = re.compile(r"END_TOKEN_PREPRINTS")
    # open the HTML file that contains the current list of publications
    htmlfile = open(filename, "r")
    htmlcontent = ""
    line = htmlfile.readline()
    # get everything before the section that lists the articles
    while not re_start_articles.search(line):
        htmlcontent += line
        line = htmlfile.readline()
    # include the stub that delimits the beginning of the list of articles
    htmlcontent += line + "\n"
    # Ignore everthing between the start of the list of articles and the
    # end of that list. We do this because we want to insert a new list
    # of articles in between the stubs that delimit the start and end of
    # the list of articles.
    while not re_end_articles.search(line):
        line = htmlfile.readline()
    # Sort the publication items. Journal articles, items in collections,
    # and proceedings papers are grouped in one section. Sort these.
    papers = articles + collections + proceedings
    sorted_index = sort_publications(publications["articles"] +
                                     publications["incollections"] +
                                     publications["inproceedings"])
    # insert the new list of articles
    htmlcontent += "  <ol>\n"
    for index in sorted_index:
        htmlcontent += FOUR_SPACES + "<li>" + papers[index] + "</li>\n"
    htmlcontent += "  </ol>\n\n"
    # Get everything before the section that lists the theses. This also
    # include the stub that delimits the end of the list of articles.
    while not re_start_theses.search(line):
        htmlcontent += line
        line = htmlfile.readline()
    # include the stub that delimits the beginning of the list of theses
    htmlcontent += line + "\n"
    # Ignore everything between the start of the list of theses and the
    # end of that list. We do this because we want to insert a new list
    # of theses in between the stubs that delimit the start and end of
    # the list of theses.
    while not re_end_theses.search(line):
        line = htmlfile.readline()
    # Sort the list of theses. These include PhD, Master's, and undergraduate
    # theses.
    theses = masterstheses + phdtheses + undergraduate_theses
    sorted_index = sort_publications(publications["masterstheses"] +
                                     publications["phdtheses"] +
                                     miscs["undergraduatetheses"])
    # insert the new list of theses
    htmlcontent += "  <ol>\n"
    for index in sorted_index:
        htmlcontent += FOUR_SPACES + "<li>" + theses[index] + "</li>\n"
    htmlcontent += "  </ol>\n\n"
    # Get everything before the section that lists the books. This also
    # include the stub that delimits the end of the list of theses.
    while not re_start_books.search(line):
        htmlcontent += line
        line = htmlfile.readline()
    # include the stub that delimits the beginning of the list of books
    htmlcontent += line + "\n"
    # Ignore everything between the start of the list of books and the
    # end of that list. We do this because we want to insert a new list
    # of books in between the stubs that delimit the start and end of
    # the list of books.
    while not re_end_books.search(line):
        line = htmlfile.readline()
    # Sort the list of books. These include both published books and
    # unpublished manuscripts.
    books_list = books + unpublisheds
    sorted_index = sort_publications(publications["books"] +
                                     publications["unpublisheds"])
    # insert the new list of books
    htmlcontent += "  <ol>\n"
    for index in sorted_index:
        htmlcontent += FOUR_SPACES + "<li>" + books_list[index] + "</li>\n"
    htmlcontent += "  </ol>\n\n"
    # Get everything before the section that lists the preprints. This also
    # include the stub that delimits the end of the list of books.
    while not re_start_preprints.search(line):
        htmlcontent += line
        line = htmlfile.readline()
    # include the stub that delimits the beginning of the list of preprints
    htmlcontent += line + "\n"
    # Ignore everything between the start of the list of preprints and the
    # end of that list. We do this because we want to insert a new list
    # of preprints in between the stubs that delimit the start and end of
    # the list of preprints.
    while not re_end_preprints.search(line):
        line = htmlfile.readline()
    # Sort the list of preprints.
    sorted_index = sort_publications(miscs["preprints"])
    # insert the new list of preprints
    htmlcontent += "  <ol>\n"
    for index in sorted_index:
        htmlcontent += FOUR_SPACES + "<li>" + preprints[index] + "</li>\n"
    htmlcontent += "  </ol>\n\n"
    # Get everything from here to the end of the file. This also include the
    # stub that delimits the end of the list of preprints.
    try:
        # When the end of the file is reached, this will raise a StopIteration
        # exception.
        while True:
            htmlcontent += line
            line = htmlfile.next()
    except StopIteration:
        # We have reached the end of the file. We don't need to do
        # anything further, apart from closing the file.
        pass
    finally:
        htmlfile.close()
    # Replace the current publications page with another page that contains
    # updated lists of publications. This overwrites the current publications
    # page.
    outfile = open(filename, "w")
    outfile.write(htmlcontent)
    outfile.close()
    if CHANGE_PERMISSIONS:
        import os
        os.system("chmod " + PERMISSIONS + " " + filename)

def output_bibtex(publications, filename):
    r"""
    Format each publication entry in BibTeX format, and output the resulting
    BibTeX formatted entries to a text file.

    INPUT:

    - publications -- a list of publication entries.

    - filename -- the name of a file.

    OUTPUT:

    Output the BibTeX formatted publication entries to the file named by
    filename.
    """
    from datetime import date
    articles = format_articles(publications["articles"], output="bibtex")
    collections = format_collections(publications["incollections"],
                                     output="bibtex")
    proceedings = format_proceedings(publications["inproceedings"],
                                     output="bibtex")
    masterstheses = format_masterstheses(publications["masterstheses"],
                                         output="bibtex")
    phdtheses = format_phdtheses(publications["phdtheses"], output="bibtex")
    books = format_books(publications["books"], output="bibtex")
    unpublisheds = format_unpublished(publications["unpublisheds"],
                                      output="bibtex")
    miscs = format_misc(publications["miscs"], output="bibtex")
    bibliography = "% $Publications citing Sage $\n" + \
        "% $Last updated: " + date.isoformat(date.today()) + " $\n\n" + \
        "--- articles ----------------------------------------\n\n"
    for article in articles:
        bibliography += article + "\n\n"
    bibliography += "--- collections ----------------------------------------\n\n"
    for item in collections:
        bibliography += item + "\n\n"
    bibliography += "--- proceedings ----------------------------------------\n\n"
    for item in proceedings:
        bibliography += item + "\n\n"
    bibliography += "--- Master's theses ----------------------------------------\n\n"
    for thesis in masterstheses:
        bibliography += thesis + "\n\n"
    bibliography += "--- PhD theses ----------------------------------------\n\n"
    for thesis in phdtheses:
        bibliography += thesis + "\n\n"
    bibliography += "--- books ----------------------------------------\n\n"
    for book in books:
        bibliography += book + "\n\n"
    bibliography += "--- unpublished manuscripts ----------------------------------------\n\n"
    for item in unpublisheds:
        bibliography += item + "\n\n"
    bibliography += "--- preprints ----------------------------------------\n\n"
    for item in miscs:
        bibliography += item + "\n\n"
    outfile = open(filename, "w")
    outfile.write(bibliography)
    outfile.close()

def process_database(dbfilename):
    r"""
    Process the publications database.

    INPUT:

    - dbfilename -- the name of the publications database file to process.

    OUTPUT:

    An 8-tuple of processed publication entries. The number eight corresponds
    to the number of publication entries considered in this script. If other
    types of publication are added to the database besides the type already
    listed above, then the new publication type should be specified in the
    block above. The 8-tuple output by this function is of the form

    (article, book, incollection, inproceedings, mastersthesis, misc,
     phdthesis, unpublished)

    where each element in the tuple is a list of processed publication
    entries. Each list is a dictionaries of publications of the same type. For
    example, the tuple element 'article' is a list of dictionaries of
    articles. Similarly, the tuple element 'book' is a list of dictionaries
    of books.
    """
    # Lists of dictionaries of publication entries. Each list contains a
    # number of dictionaries of publication entries of the same type.
    articles = []
    books = []
    incollections = []
    inproceedings = []
    masterstheses = []
    miscs = []
    phdtheses = []
    unpublisheds = []
    # some useful constants
    ARTICLE_ATT_LENGTH = len(article_attributes)
    BOOK_ATT_LENGTH = len(book_attributes)
    INCOLLECTION_ATT_LENGTH = len(incollection_attributes)
    INPROCEEDINGS_ATT_LENGTH = len(inproceedings_attributes)
    MASTERSTHESIS_ATT_LENGTH = len(mastersthesis_attributes)
    MISC_ATT_LENGTH = len(misc_attributes)
    PHDTHESIS_ATT_LENGTH = len(phdthesis_attributes)
    UNPUBLISHED_ATT_LENGTH = len(unpublished_attributes)
    # read in the file containing the database of publication entries
    dbfile = open(dbfilename, "r")
    try:
        # Process the whole database using the next() function. This will
        # raise a StopIteration exception once it reaches the end of the
        # database file.
        while True:
            line = dbfile.next().strip()
            if line == "article":
                # process article entry
                article_dict = {}
                for i in xrange(ARTICLE_ATT_LENGTH):
                    article_dict.setdefault(
                        article_attributes[i], dbfile.next().strip())
                articles.append(article_dict)
            elif line == "book":
                # process book entry
                book_dict = {}
                for i in xrange(BOOK_ATT_LENGTH):
                    book_dict.setdefault(
                        book_attributes[i], dbfile.next().strip())
                books.append(book_dict)
            elif line == "incollection":
                # process incollection entry
                incollection_dict = {}
                for i in xrange(INCOLLECTION_ATT_LENGTH):
                    incollection_dict.setdefault(
                        incollection_attributes[i], dbfile.next().strip())
                incollections.append(incollection_dict)
            elif line == "inproceedings":
                # process inproceedings entry
                inproceedings_dict = {}
                for i in xrange(INPROCEEDINGS_ATT_LENGTH):
                    inproceedings_dict.setdefault(
                        inproceedings_attributes[i], dbfile.next().strip())
                inproceedings.append(inproceedings_dict)
            elif line == "mastersthesis":
                # process Master's thesis entry
                mastersthesis_dict = {}
                for i in xrange(MASTERSTHESIS_ATT_LENGTH):
                    mastersthesis_dict.setdefault(
                        mastersthesis_attributes[i], dbfile.next().strip())
                masterstheses.append(mastersthesis_dict)
            elif line == "misc":
                # process miscellaneous entry
                misc_dict = {}
                for i in xrange(MISC_ATT_LENGTH):
                    misc_dict.setdefault(
                        misc_attributes[i], dbfile.next().strip())
                miscs.append(misc_dict)
            elif line == "phdthesis":
                # process PhD thesis entry
                phdthesis_dict = {}
                for i in xrange(PHDTHESIS_ATT_LENGTH):
                    phdthesis_dict.setdefault(
                        phdthesis_attributes[i], dbfile.next().strip())
                phdtheses.append(phdthesis_dict)
            elif line == "unpublished":
                # process unpublished entry
                unpublished_dict = {}
                for i in xrange(UNPUBLISHED_ATT_LENGTH):
                    unpublished_dict.setdefault(
                        unpublished_attributes[i], dbfile.next().strip())
                unpublisheds.append(unpublished_dict)
    except StopIteration:
        # We have reached the end of the file. We don't need to do
        # anything further, apart from closing the file.
        pass
    finally:
        dbfile.close()
    return {"articles": articles,
            "books": books,
            "incollections": incollections,
            "inproceedings": inproceedings,
            "masterstheses": masterstheses,
            "miscs": miscs,
            "phdtheses": phdtheses,
            "unpublisheds": unpublisheds}

def remove_blanks(entry):
    r"""
    Remove all attributes from the publication entry that contain the value
    '<BLANK>'.

    INPUT:

    - entry -- a dictionary containing attribute/value pairs that describe
      a publication entry.

    OUTPUT:

    A dictionary containing attribute/value pairs that describes the same
    publication entry as represented by 'entry'. However, all attributes with
    the value '<BLANK>' are removed from this output dictionary.
    """
    # remove all but one 'blank' from the publication entry
    processed_entry = dict(zip(entry.values(), entry.keys()))
    # finally remove the last remaining 'blank'
    try:
        del processed_entry[BLANK]
    except:
        pass
    return dict(zip(processed_entry.values(), processed_entry.keys()))

def remove_special(entry):
    r"""
    Remove each special character from the publication entry. The special
    characters we consider usually include escape sequences specific to LaTeX.

    INPUT:

    - entry -- a dictionary containing attribute/value pairs that describe
      a publication entry.

    OUTPUT:

    A dictionary containing attribute/value pairs that describes the same
    publication entry as represented by 'entry'. However, all special
    characters are removed.
    """
    from copy import copy
    remove_targets = ["{", "\\", "'", "\"", "}"]
    cleansed_entry = copy(entry)
    for item in remove_targets:
        cleansed_entry = cleansed_entry.replace(item, "")
    return cleansed_entry

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
    from copy import copy
    replace_table = [("{\\\"a}", "&auml;"),
                     ("{\\'a}", "&aacute;"),
                     ("{\\\"e}", "&euml;"),
                     ("{\\'e}", "&eacute;"),
                     ("{\\'i}", "&iacute;"),
                     ("{\\'o}", "&oacute;"),
                     ("\\&", "&amp;"),
                     ("\\textsc{", ""),
                     ("{", ""),
                     ("}", "")]
    cleansed_entry = copy(entry)
    for candidate, target in replace_table:
        cleansed_entry = cleansed_entry.replace(candidate, target)
    return cleansed_entry

def replace_special_url(url):
    r"""
    Replace each special character in the given URL with its equivalent
    HTML encoding.

    INPUT:

    - url -- some URL.

    OUTPUT:

    A URL equivalent to the given URL. However, all special characters are
    replaced with their equivalent HTML encoding.
    """
    from copy import copy
    replace_table = [("&", "&amp;")]
    cleansed_url = copy(url)
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
    return [publications[sorted_names[i][POSITION_INDEX]]
                for i in xrange(len(sorted_names))]

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
    item_years = [(publications[i]["year"], i)
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

### the main part #########################################################

# the driver section; this is where everything starts from
if __name__ == "__main__":
    db = process_database(publications_database)
    output_html(db, html_filename)
