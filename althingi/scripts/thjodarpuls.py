#!/usr/bin/env python3
"""
Script to collect polling data from Gallup (né Capacent) and output it as CSV
to a file-like object (stdout by default).

Gallup store their polling data in a `dataset on DataMarket`_. Using the
`DataMarket API`_ we can download a CSV containing every poll since March 1994.

The script is written in Python 3 and has no dependencies.

.. _dataset on DataMarket: https://datamarket.com/data/set/yf5/
.. _DataMarket API: https://datamarket.com/api/v1/
"""
import codecs
import csv
import datetime
import re
import sys
import urllib.request


SOURCE_URL = "https://datamarket.com/api/v1/list.csv?ds=yf5&callback="
# Parties are prefixed by their ballot letter, except Hreyfingin.
PARTY_NAME_RE = re.compile(r"\(\w\) (.+)|(Hreyfingin)")


def scrape(file_obj=None, include_header=True):
    """
    Download the source data as a CSV using DataMarket's API, clean it up and
    discard uninteresting rows, and output it to a file-like object (stdout by
    default).

    Args:
        file_obj: file-like object in which to output the parsed CSV data
        include_header: if True (default), include a header row in the output
    """
    if file_obj is None:
        file_obj = sys.stdout
    output = csv.writer(file_obj)
    if include_header:
        output.writerow(("date", "pollster", "party", "support"))

    response = urllib.request.urlopen(SOURCE_URL)
    # Since urllib returns bytes, iterate through the CSV data and decode it as
    # UTF-8.
    rows = csv.reader(codecs.iterdecode(response, "ISO-8859-1"))
    for party, date, support in rows:
        # Only match rows that contain data for distinct political parties.
        # That way we can ignore rows containing data on government support
        # (e.g. "1995-2007 (B og D)").
        match = PARTY_NAME_RE.match(party)
        if match:
            # Dates are only year-and-month. Normalise it to a full date,
            # although that won't actually be an accurate date.
            date = datetime.datetime.strptime(date, "%Y-%m").date()
            # Use the first non-null group in the regex as the party name.
            party = next(g for g in match.groups() if g is not None)
            output.writerow((date, "Gallup", party, float(support)))


if __name__ == "__main__":
    scrape()
