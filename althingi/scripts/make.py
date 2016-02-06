#!/usr/bin/env python3
"""
Script to run the poll scrapers, clean the data, and save the output to the
data files that make up the data package.

The script is written in Python 3 and has no dependencies. Run it from the
``althingi/scripts`` directory and the data files in the ``althingi/data``
will be updated.
"""
import csv
import io
import importlib
import operator


# Modules that scrape data from pollsters.
SCRAPERS = (
    "mmr",
    "thjodarpuls",
    "mbl_archive",
)
# Normalised version of misspellings, abbreviations, etc of party names.
PARTY_NAME_CORRECTIONS = {
    "Flokkur heimilana": "Flokkur heimilanna",
    "Framsóknarflokkur": "Framsóknarflokkurinn",
    "Sjálfstæðisflokkur": "Sjálfstæðisflokkurinn",
    "Vinstri-grænir": "Vinstri græn",
    "Vinstrihr. -grænt framb.": "Vinstri græn",
}


def scrape(file_obj=None, include_header=True):
    """
    Run the scrapers defined in ``SCRAPERS`` and output their output to a
    file-like object (stdout by default).

    Args:
        file_obj: file-like object in which to output the scrapers' data
        include_header: if True (default), include a header row in the output
    """
    if file_obj is None:
        file_obj = sys.stdout
    for i, scraper_name in enumerate(SCRAPERS):
        scraper = importlib.import_module(scraper_name)
        scraper.scrape(file_obj, include_header=include_header and i == 0)


def save_csv_files():
    """
    Run the scrapers defined in ``SCRAPERS``, combine their data, convert it to
    third-normal form, and save it in the files that make up the ``althingi``
    data package.
    """
    # Collect all the scrapers' data into a StringIO object.
    raw_data = io.StringIO()
    scrape(raw_data, include_header=False)
    raw_data.seek(0)
    # Order the data first by date, then party, then pollster. That way the
    # order of output will be stable over time, with new polls, parties, and
    # pollsters being added to the bottom of the CSV output (and being given
    # later ids) rather than being interpolated each run.
    data = sorted(csv.reader(raw_data), key=operator.itemgetter(0, 2, 1))

    # Output that data in a set of third-normal form CSVs.
    parties = []
    pollsters = []
    polls = []
    with open("../data/data.csv", "w") as fh:
        data_csv = csv.writer(fh)
        data_csv.writerow(("poll_id", "party_id", "support"))
        for date, pollster, party, support in data:
            # Keep a list of unique pollster names and use each pollster's
            # index in the list as a unique id.
            try:
                pollster_id = pollsters.index(pollster)
            except ValueError:
                pollster_id = len(pollsters)
                pollsters.append(pollster)
            # Normalise the party name, keep a list of unique party names, and
            # use each party's index in the list as a unique id.
            party = PARTY_NAME_CORRECTIONS.get(party, party)
            try:
                party_id = parties.index(party)
            except ValueError:
                party_id = len(parties)
                parties.append(party)
            # Keep a list of unique polls and use each poll's index in the list
            # as a unique id.
            try:
                poll_id = polls.index((date, pollster_id))
            except ValueError:
                poll_id = len(polls)
                polls.append((date, pollster_id))
            # Write each party's percentage support for each poll to a CSV.
            data_csv.writerow((poll_id, party_id, support))

    # Write the parties CSV.
    with open("../data/parties.csv", "w") as fh:
        parties_csv = csv.writer(fh)
        parties_csv.writerow(("party_id", "name"))
        parties_csv.writerows(enumerate(parties))

    # Write the pollsters CSV.
    with open("../data/pollsters.csv", "w") as fh:
        pollsters_csv = csv.writer(fh)
        pollsters_csv.writerow(("pollster_id", "name"))
        pollsters_csv.writerows(enumerate(pollsters))

    # Write the polls CSV.
    with open("../data/polls.csv", "w") as fh:
        polls_csv = csv.writer(fh)
        polls_csv.writerow(("poll_id", "pollster_id", "publish_date",
                            "sample_size", "response_rate"))
        for i, (date, pollster_id) in enumerate(polls):
            polls_csv.writerow((i, pollster_id, date, "", ""))


if __name__ == "__main__":
    save_csv_files()
