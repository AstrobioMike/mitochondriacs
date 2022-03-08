
# PURPOSE  

- Afshin got a master spreadsheet from Sam: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo  
- It was missing the strain ID for most plants (and other stuff)  
- Richard noted this info is often in an "ecotype" column for plants  

This was quickly hacking together an automated way of getting the unique values for all samples from the strain or ecotype column for each GLDS that had one.  

# GENERAL PROCESS FOR EACH GLDS  

- get the ISA file
- get-ecotype
- get the study table
- get the unique values from either the strain or ecotype column (if they exist, reports "None found" if not, reports "Not clear" if multiple exist)
- append those to a building table ("Strain-tab.tsv" by default)
- store study info table in subdirectory


# WHAT I DID  

Sorted the master spreadsheet (https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) by column A, to get all target GLDS IDs, put them into "target-GLDS-IDs.txt".

Running:
```bash
bash get-ecotype-info.sh target-GLDS-IDs.txt
```

When done, the produced "Strain-tab.tsv" looks like this:

```bash
head Strain-tab.tsv | column -ts $'\t' | sed 's/^/# /'
```
```
# GLDS-1    None found
# GLDS-100  None found
# GLDS-101  None found
# GLDS-102  None found
# GLDS-103  None found
# GLDS-104  None found
# GLDS-105  None found
# GLDS-106  UA159
# GLDS-107  None found
# GLDS-108  C57BL/6CR
```

Pasted these columns into the master spreadsheet, double-checked the order was the same, removed newly-pasted GLDS ID column that was used to check.

