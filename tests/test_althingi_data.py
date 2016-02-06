import csv
import datetime
import os


def test_independence_party_id_is_correct():
    """
    Test that the Independence party (Sjálfstæðisflokkurinn) has the id 4. If
    not, something has changed in how the source data is parsed.
    """
    found_party = False
    with open("althingi/data/parties.csv") as fh:
        for party_id, party_name in csv.reader(fh):
            if party_name == "Sjálfstæðisflokkurinn":
                assert party_id == "4"
                found_party = True
                break
    assert found_party is True


def test_polls_ordered_chronologically():
    """
    Test that the polls in the CSV data are ordered chronologically, earliest
    first.
    """
    with open("althingi/data/polls.csv") as fh:
        polls = csv.reader(fh)
        next(polls)  # Skip header row.
        last_date = datetime.datetime.strptime(next(polls)[2], "%Y-%m-%d")
        for _, _, date, _, _ in polls:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            assert date >= last_date
