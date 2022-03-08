
# PURPOSE  

- Afshin got a master spreadsheet of GLDS info from Sam: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo  
- It was missing the strain ID for most plants and some other stuff  
- Richard noted this info is often in an "ecotype" column for plants  

This repo holds what I hacked together to automate getting the unique values for "strain" or "ecotype" for all samples for each GLDS that had either one or both of those columns in its Study table. 

The result table from this is "GLDS-strain-info.tsv" above, and I added the info as a new column to the [master spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) called "strain/ecotype listed".   

# GENERAL PROCESS FOR EACH GLDS  

- get the ISA file
- get the study table
- get the unique values from either the strain or ecotype column if they exist
  - multiple are linked with spaced-pipes (` | `)
  - reports "None found" if not found
  - reports "Not clear" if multiple exist or if something went wrong (like with file format)
- append those to a building table ("GLDS-strain-info.tsv" by default)
- store individual study info tables in a subdirectory, not included here due to size


# WHAT I DID  

Sorted the [master spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) by column A ("GLDS"), took these GLDS IDs and put them into "target-GLDS-IDs.txt".

Running the code above:
```bash
bash get-strain-info.sh target-GLDS-IDs.txt
```

When done, the produced "GLDS-strain-info.tsv" looks like this:

```bash
head GLDS-strain-info.tsv | column -ts $'\t' | sed 's/^/# /'
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

