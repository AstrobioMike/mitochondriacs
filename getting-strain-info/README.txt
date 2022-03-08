
# PURPOSE

## Afshin got a master spreadsheet from Sam: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo

## it was missing the strain ID for most plants (and other stuff)

## Richard noted this info is often in an "ecotype" column for plants

## this was hacking an automated way of getting the unique values for all samples from the strain or ecotype column for each GLDS that had one

# GENERAL PROCESS FOR EACH GLDS

#    - get the ISA file
#    - get-ecotype
#    - get the study table
#    - get the unique values from either the strain or ecotype column (if they exist, reports "None found" if not)
#    - append those to a building table ("Strain-tab.tsv" by default)
#    - store study info table in subdirectory


# WHAT I DID

## sorted the master spreadsheet by column A here: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo

## put all target GLDS IDs into "target-GLDS-IDs.txt"

## running on all:
    for target in $(cat target-GLDS-IDs.txt); do bash get-ecotype-info.sh ${target}; done

## when done, "Strain-tab.tsv" looks like this:

# GLDS-1	    None found
# GLDS-100	None found
# GLDS-101	None found
# GLDS-102	None found
# GLDS-103	None found
# GLDS-104	None found
# GLDS-105	None found
# GLDS-106	UA159
# GLDS-107	None found
# GLDS-108	C57BL/6CR


# pasted this into the master spreadsheet, double-checked the order was the same, removed newly-pasted GLDS ID column that was used to check

