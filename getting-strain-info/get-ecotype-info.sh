#!/usr/bin/env bash
set -e

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then

    printf "\n  Gets strain info from the ecotype or strain column of all GLDS IDs provided in\n"
    printf "  a single-column file given to positional argument 1. Builds table with GLDS ID and\n"
    printf "  unique ecotype/strain values onto positional argument 2 (or default 'Strain-tab.tsv')\n"
    printf "  It will put finished study tables into a subdirectory called 'GLDS-study-info/'.\n\n"
    printf "  Ex. usage: bash get-ecotype-info.sh target-GLDS-IDs.txt\n\n"
    exit
fi

if [ -z "${2}" ]; then
    output_file="Strain-tab.tsv"
fi

# making sure output file doesn't exist already
if [ -s ${output_file} ]; then

    printf "\n    The output file '${output_file}' already exists.\n"
    printf "    We don't want to overwrite anything accidentally. Remove it\n"
    printf "    or change the 2nd positional argument.\n\n"
    printf "  Exiting for now.\n\n"
    exit 1

fi

info_dir="GLDS-study-info"


for ID in $(cat ${1}); do

    printf "\n Doing: ${ID}\n\n"

    ./get-ISA.py -g ${ID}

    unzip -j -qq ${ID}-ISA.zip

    # alot of them have this file, so removing if so
    rm -rf .DS_store

    # we want the study table, so removing assay and investigation ones
    rm a_* i_*

    # making sure there is only one we are going to try to pull from
    num_potential_files=$(ls s_* | wc -l)

    if [ ${num_potential_files} != 1 ]; then 
        printf "\n    More than one (or 0) potential assay tables were found :(\n\n"
        printf "\n  Exiting for now.\n\n"
        exit 1
    fi

    # removing ISA zip
    rm ${ID}-ISA.zip

    # renaming study table so standardized
    study_info_tab=${ID}-study-info.tsv
    mv s_* ${study_info_tab}

    # getting unique strains listed (whether in strain or ecotype column)
    if grep -q "Ecotype" ${study_info_tab} ; then

        ecotype_column_found="yes"
        ecotype_col=$(head -n 1 ${study_info_tab} | tr "\t" "\n" | cat -n | grep -v "Factor" | grep "Ecotype" | tr -s " " "\t" | cut -f 2)

        # checking we only have 1 column as expected, and storing as "Not clear" if not
        num_potential_cols=$(echo ${ecotype_col} | wc -w | sed 's/^ *//' | cut -f 1)
        if [ ${num_potential_cols} != 1 ]; then
            unique_ecotypes_listed="Not clear"
        else
            unique_ecotypes_listed=$(cut -f ${ecotype_col} ${study_info_tab} | tail -n +2 | tr -d '"' | sort -u | tr "\n" "|" | sed 's/|$//' | sed 's/|/ | /g')
        fi

    else

            ecotype_column_found="no"

    fi

    if grep -q "Strain" ${study_info_tab} ; then

        strain_column_found="yes"
        strain_col=$(head -n 1 ${study_info_tab} | tr "\t" "\n" | cat -n | grep -v "Factor" | grep "Strain" | tr -s " " "\t" | cut -f 2)

        # checking we only have 1 column as expected, and storing as "Not clear" if not
        num_potential_cols=$(echo ${strain_col} | wc -w | sed 's/^ *//' | cut -f 1)
        if [ ${num_potential_cols} != 1 ]; then
            unique_strains_listed="Not clear"
        else
            unique_strains_listed=$(cut -f ${strain_col} ${study_info_tab} | tail -n +2 | tr -d '"' | sort -u | tr "\n" "|" | sed 's/|$//' | sed 's/|/ | /g')
        fi

    else

        strain_column_found="no"

    fi

    # if both, making sure they are identical
    if [ ${ecotype_column_found} == "yes" ] && [ ${strain_column_found} == "yes" ]; then

        if [ ${unique_ecotypes_listed} != ${unique_strains_listed} ]; then

            printf "\n    Both 'ecotype' and 'strain' columns were found, and they do not match :(\n\n"
            printf "  Exiting for now.\n\n"
            exit 1

        fi

    fi

    if [ ${ecotype_column_found} == "yes" ]; then

        strains_listed=${unique_ecotypes_listed}

    elif [ ${strain_column_found} == "yes" ]; then

        strains_listed=${unique_strains_listed}

    fi

    ## if neither found, then reporting NA
    if [ ${ecotype_column_found} == "no" ] && [ ${strain_column_found} == "no" ]; then

        strains_listed="None found"

    fi

    echo -e "${ID}\t${strains_listed}" >> ${output_file}

    mkdir -p ${info_dir}
    mv ${study_info_tab} ${info_dir}

done
