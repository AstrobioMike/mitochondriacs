
# PURPOSE  

- Afshin got a master spreadsheet of GLDS info from Sam: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo  
- It was missing the strain ID for most plants and some other stuff  
- Richard noted this info is often in an "ecotype" column for plants  

This was quickly hacking together an automated way of getting the unique values for all samples from the strain or ecotype column for each GLDS that had one or both of those columnes.  

# GENERAL PROCESS FOR EACH GLDS  

- get the ISA file
- get the study table
- get the unique values from either the strain or ecotype column if they exist
  - multiple are linked with spaced-pipes (` | `)
  - reports "None found" if not found
  - reports "Not clear" if multiple exist or if something went wrong (like with file format)
- append those to a building table ("Strain-tab.tsv" by default)
- store individual study info tables in a subdirectory, not included here due to size


# WHAT I DID  

Sorted the [master spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) by column A ("GLDS"), took these GLDS IDs and put them into "target-GLDS-IDs.txt".

Running the code above:
```bash
bash get-strain-info.sh target-GLDS-IDs.txt
```

When done, the produced "Strain-tab.tsv" looks like this:

```bash
head Strain-tab.tsv | column -ts $'\t' | sed 's/^/# /'
```
```
# GLDS-1    Oregon R
# GLDS-100  C57BL/6J
# GLDS-101  C57BL/6J
# GLDS-102  C57BL/6J
# GLDS-103  C57BL/6J
# GLDS-104  C57BL/6J
# GLDS-105  C57BL/6J
# GLDS-106  UA159
# GLDS-107  C57BL/6
# GLDS-108  C57BL/6CR
```

I added the second column to the [master spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) as "strain/ecotype listed". 

