#!/usr/bin/env python

"""
This gets the ISA file for a specified GLDS dataset. Modified from previous
work by Kirill Grigorev and Jonathan Oribello. 
"""

import sys
import argparse
from json import loads
from urllib.request import urlopen, quote, urlretrieve
from re import search
from pathlib import Path
import requests


parser = argparse.ArgumentParser(description = "This script gets the ISA file for a specified GLDS dataset. Modified from \
                                                previous work by Kirill Grigorev and Jonathan Oribello.",
                                 epilog = "Ex. usage: GL-get-ISA -g GLDS-250\n")

parser.add_argument("-g", "--GLDS-ID", help = "e.g. 'GLDS-250'", action = "store", required = True)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(0)

args = parser.parse_args()

##################################################

def main():

    isazip = download_isa(args.GLDS_ID)


##################################################

GENELAB_ROOT = "https://genelab-data.ndc.nasa.gov"
GLDS_URL_PREFIX = GENELAB_ROOT + "/genelab/data/study/data/"
FILELISTINGS_URL_PREFIX = GENELAB_ROOT + "/genelab/data/study/filelistings/"
ISA_ZIP_REGEX = r'.*_metadata_.*[_-]ISA\.zip$'

output_ISA = args.GLDS_ID + str("-ISA.zip")

def read_json(url):
    with urlopen(url) as response:
        return loads(response.read().decode())


def get_isa(accession: str):
    """ Returns isa filename as well as GeneLab URLS from the associated file listing
    :param accession: GLDS accession ID, e.g. GLDS-194
    """
    glds_json = read_json(GLDS_URL_PREFIX + accession)
    try:
        _id = glds_json[0]["_id"]
    except (AssertionError, TypeError, KeyError, IndexError):
        raise ValueError("Malformed JSON?")
    isa_entries = [
        entry for entry in read_json(FILELISTINGS_URL_PREFIX + _id)
        if search(ISA_ZIP_REGEX, entry["file_name"])
    ]
    if len(isa_entries) == 0:
        raise ValueError("Unexpected: no ISAs found")
    elif len(isa_entries) > 1:
        raise ValueError("Unexpected: multiple files match the ISA regex")
    else:
        entry = isa_entries[0]
        version = entry["version"]
        url = GENELAB_ROOT + entry["remote_url"] + "?version={}".format(version)
        alt_url = (
            GENELAB_ROOT + "/genelab/static/media/dataset/" +
            quote(entry["file_name"]) + "?version={}".format(version)
        )
    
    return entry["file_name"], version, url, alt_url


def download_isa(accession: str):
    """ Downloads isa for given accession number.
    :param accession: GLDS accession number, e.g. GLDS-194
    """
    
    filename ,_, url, alt_url  = get_isa(accession)
    
    r = requests.get(url)

    try:
        # if failed to download, will raise exception and try alternate url
        r.raise_for_status()

    except:

        r = requests.get(alt_url)
    
    with open(output_ISA, "wb") as f:
        f.write(r.content)

    return filename


if __name__ == "__main__":
    main()
