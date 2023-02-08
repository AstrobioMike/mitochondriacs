#!/usr/bin/env python

"""
This pulls some wanted info from the investigation table. Meant to be used with this repo:
    https://github.com/AstrobioMike/mitochondriacs/tree/main/updating-datasets-table

ex. usage: python parse-investigation-tab.py GLDS-38 i_Investigation.txt a_Assay.txt s_Sample.txt output.tmp
"""

import sys
import pandas as pd

GLDS_ID = sys.argv[1]

my_null_result = "Not auto-detected."

# "Study Assay Technology Type" entries that we'd want to report a specific way
rna_seq_label = "rna seq" # to match what's in our table already
rna_seq_values = ["RNA Sequencing (RNA-Seq)"]

proteomics_label = "proteomics" # to match what's in our table already
proteomics_values = ["mass spectrometry"]

microarray_label = "microarray" # to match what's in our table already
microarray_values = "DNA microarray"


## working first on investigation table ##
study_assay_technology_types = []
study_assay_measurement_types = []
study_factors = []

### helper function ###
def get_values(target_column, df, return_next_column = False):

    """
    Gets the values for a specified column and returns them uniqued as a ", "-delimited string, if found.
    """

    # see get_wanted_column_name() function explanation for why we're doing this
    target_column = target_column.rstrip("]")
    target_column = get_wanted_column_name(target_column, df)

    if target_column in list(df.columns):

        target_list = df[target_column].tolist()

        # getting only unique values
        target_list = list(set(target_list))
        
        # ensuring it's a string
        target_list = [str(x) for x in target_list]
        target_value = ", ".join(target_list)

        if target_value == "":

            target_value = my_null_result

    else:

        target_value = my_null_result

    
    # getting following column if specified (typically to get unit after some measurement)
    if return_next_column and target_column in list(df.columns):

        # getting column name position
        wanted_column_pos = df.columns.get_loc(target_column) + 1

        next_col_list = df.iloc[:, wanted_column_pos].tolist()

        # getting only unique values
        next_col_list = list(set(next_col_list))
        next_col_value = ", ".join(next_col_list)

        # combining 
        target_value = f"{target_value} ({next_col_value})" 

    return(target_value)


def get_wanted_column_name(target_column_prefix, df):

    """
    Some columns have extra crap in them, like:
    Characteristics[Ecotype,http://purl.bioontology.org/ontology/MESH/D060146,MESH]
    from GLDS-205's s_GSE95388.txt table. So this finds the column name based on the prefix
    provided.
    """

    matches = []

    for colname in df.columns:

        if colname.startswith(target_column_prefix):

            matches.append(colname)

    if len(matches) == 1:

        wanted_column_name = matches[0]

    else:

        wanted_column_name = my_null_result

    return(wanted_column_name)


# iterating through each line and getting what we want
with open(sys.argv[2]) as input_file:

    for line in input_file:

        # splitting into list and also removing quotes if there are any
        line_list = line.strip().replace('"', '').replace("'", "").split('\t')

        # getting title
        if line_list[0] == "Study Title":

            if len(line_list) > 1:
    
                study_title = line_list[1]

            else:
                
                study_title = "Problem identifying title."

        # getting study assay technology types
        if line_list[0] == "Study Assay Technology Type":

            for entry in line_list[1:len(line_list)]:

                if entry in rna_seq_values:

                    entry = rna_seq_label

                if entry in proteomics_values:

                    entry = proteomics_label

                if entry in microarray_values:

                    entry = microarray_label
                
                study_assay_technology_types.append(entry)

        # getting study assay measurement types
        if line_list[0] == "Study Assay Measurement Type":

            for entry in line_list[1:len(line_list)]:

                study_assay_measurement_types.append(entry)

        # getting study factors
        if line_list[0] == "Study Factor Name":

            for entry in line_list[1:len(line_list)]:

                study_factors.append(entry)

study_assay_technology_types_str = ", ".join(study_assay_technology_types)
study_assay_measurement_types_str = ", ".join(study_assay_measurement_types)

if len(study_factors) == 0:

    study_factors_str = my_null_result

else:

    study_factors_str = ", ".join(study_factors)

## now working on study and sample tables to get other wanted info
study_df = pd.read_csv(sys.argv[3], sep = "\t")
sample_df = pd.read_csv(sys.argv[4], sep = "\t")

# i noticed sometime the case is different, e.g.,
    # GLDS-44 s_E-MTAB-3011.txt has "Characteristics[organism]", with lowercase o in organism
    # GLDS-38 s_PXD002096.txt has "Characteristics[Organism]", with uppercase
    # so changing them all to all be uppercase

new_names = []
for colname in list(study_df.columns):

    new_names.append(colname.upper())

study_df.columns = new_names

new_names = []
for colname in list(sample_df.columns):

    new_names.append(colname.upper())

sample_df.columns = new_names

# taking organism name if the column exists and the entry isn't empty
organism = get_values("Characteristics[Organism]".upper(), study_df)

# checking in sample table if not found there
if organism == my_null_result:

    organism = get_values("Characteristics[Organism]".upper(), sample_df)

# working on getting a strain if possible
strain = get_values("Characteristics[Strain]".upper(), study_df)

# trying ecotype column if strain column didn't work
if strain == my_null_result:

    strain = get_values("Characteristics[Ecotype]".upper(), study_df)

# checking in sample table if not found there
if strain == my_null_result:

    strain = get_values("Characteristics[Strain]".upper(), sample_df)

if strain == my_null_result:

    strain = get_values("Characteristics[Ecotype]".upper(), sample_df)


# getting sex if available
sex = get_values("Characteristics[Sex]".upper(), study_df)

# checking in sample table if not found in study table
if sex == my_null_result:

    sex = get_values("Characteristics[Sex]".upper(), sample_df)


# getting age if available
age = get_values("Characteristics[Age]".upper(), study_df, True)

# checking in sample table if not found in study table
if age == my_null_result:

    age = get_values("Characteristics[Age]".upper(), sample_df, True)


# combining 
out_line = f"{GLDS_ID}\t{study_title}\t{study_assay_technology_types_str}\t{study_assay_measurement_types_str}\t{organism}\t{study_factors_str}\t{sex}\t{age}\t{strain}\n"

# header = "GLDS\tStudy Title\tAssay(s)\tMeasument Type(s)\tOrganism(s)\tFactor(s)\tSex\tAge\tStrain\t\n"

# writing out
with open(sys.argv[5], "w") as out_file:

#    out_file.write(header)
    out_file.write(out_line)
