#!/usr/bin/env python3
"""
Script to scrape polling data from Markaðs og miðlarannsóknir (MMR) and output
it as CSV to stdout.

There's a `chart on MMR's website`_ that uses `a Google spreadsheet`_ that
includes data for every poll MMR have completed since October 2010. The
spreadsheet is in a wide (aka unpivoted) format. It's downloaded as a CSV,
converted to long-form `tidy data`_, and output to stdout.

The script is written in Python 3 and has no dependencies.

.. _chart on MMR's website: http://mmr.is/fylgi-flokka-og-rikisstjornar
.. _a Google spreadsheet: http://goo.gl/0JPYkT
.. _tidy data: http://vita.had.co.nz/papers/tidy-data.html
"""
import codecs
import csv
import datetime
import sys
import urllib.request


SPREADSHEET_ID = "1T2t4HRHzTbFWp89fs-bUjOgk7X1FVt_zIThftmxy-IY"
EXPORT_URL = "https://docs.google.com/spreadsheets/d/{}/export?format=csv"


def scrape():
    """
    Download the source CSV data from Google Spreadsheets, convert it from
    wide-form to long-form, and output it to stdout.
    """
    output = csv.writer(sys.stdout)
    output.writerow(("date", "pollster", "party", "support"))

    response = urllib.request.urlopen(EXPORT_URL.format(SPREADSHEET_ID))
    # Since urllib returns bytes, iterate through the CSV data and decode it as
    # UTF-8.
    rows = csv.reader(codecs.iterdecode(response, "UTF-8"))
    # Party names are in the first row, from the second column onwards.
    parties = next(rows)[1:]
    for row in rows:
        # Dates are in the first column, from the second row onwards.
        date = datetime.datetime.strptime(row[0], "%d/%m/%Y").date()
        parties_support = []
        for party, support in zip(parties, row[1:]):
            try:
                output.writerow((date, "MMR", party,
                                 float(support.replace(",", "."))))
            except ValueError:
                # No value given for the party, and so no need to output a row.
                pass


if __name__ == "__main__":
    scrape()
