#!/usr/bin/env python3
"""
Script to scrape polling data (from January 2012 to April 2013) from
Morgunblaðið and output it as CSV to stdout.

From `a Morgunblaðið article`_ you can find a `CSV archive of all polls`_
produced between January 2012 and April 2013. If we discard those that are
scraped from other more complete sources we're left with polls produced by
Félagsvísindastofnun and Fréttablaðið/Stöð 2.

The script is written in Python 3 and has no dependencies.

.. _a Morgunblaðið article: http://www.mbl.is/frettir/kosning/2013/06/14/59_9_prosent_stydja_rikisstjornina/
.. _CSV archive of all polls: http://www.mbl.is/frettir/kosningar/kannanir.csv

"""
import codecs
import csv
import datetime
import sys
import urllib.request


SOURCE_URL = "http://www.mbl.is/frettir/kosningar/kannanir.csv"
POLLSTERS = ("Fréttablaðið / Stöð 2", "Félagsvísindast. f. Morgunblaðið")


def scrape():
    """
    Download the source CSV data from Morgunblaðið, discard rows we get from
    elsewhere, and output the rest to stdout.
    """
    output = csv.writer(sys.stdout)
    output.writerow(("date", "pollster", "party", "support"))

    response = urllib.request.urlopen(SOURCE_URL)
    # Since urllib returns bytes, iterate through the CSV data and decode it as
    # ISO-8859-1.
    rows = csv.reader(codecs.iterdecode(response, "ISO-8859-1"), delimiter=";")
    next(rows)  # Skip header row.
    for date, pollster, party, support in rows:
        if pollster in POLLSTERS:
            output.writerow((date, pollster, party, support.replace(",", ".")))


if __name__ == "__main__":
    scrape()
