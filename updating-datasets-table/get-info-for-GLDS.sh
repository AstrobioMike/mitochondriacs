#!/use/bin/env bash
set -eu

# ad-hoc script for getting some general info about a given GLDS ID
# ex. usage: bash get-info-for-GLDS.sh GLDS-38 GL-dataset-info.tsv
# expected to be run in genelab-utils conda environment
# see repo here: https://github.com/AstrobioMike/mitochondriacs/tree/main/updating-datasets-table

curr_GLDS_ID=${1}

mkdir ${curr_GLDS_ID}
cd ${curr_GLDS_ID}

# downloading isa
GL-download-GLDS-data -g ${curr_GLDS_ID} -p metadata,ISA.zip -f > /dev/null

# checking any were downloaded
if [ ! -f *-wanted-file-download-commands.sh ]; then
    printf "${curr_GLDS_ID}\tISA file not found.\n"
    exit
fi

# checking to make sure exactly 1 was downloaded
num_dld=$(wc -l *-wanted-file-download-commands.sh | cut -d " " -f 1)

if [ ${num_dld} != 1 ]; then
    printf "${curr_GLDS_ID}\tMore than one ISA found.\n"
    exit
fi

# unzipping isa (the -j ignores if there are sub-directories as some have them and some don't)
unzip -j -qq *-ISA.zip

# checking there is only one investigation table
num_i_prefix_files=$(ls i_* | wc -l | cut -d " " -f 1)

if [ ${num_i_prefix_files} != 1 ]; then
    printf "${curr_GLDS_ID}\tLess or more than one investigation table found.\n"
    exit
fi

investigation_table_path=$(ls i_*)


# checking there is only one assay table, what we're pulling should be the same in multiple, so taking one anyway, but reporting
num_a_prefix_files=$(ls a_* | wc -l | cut -d " " -f 1)

if [ ${num_a_prefix_files} != 1 ]; then
    printf "\n    Just a note that ${curr_GLDS_ID} has more than one assay table. We are going to use the first one,\n"
    printf "    as what we're pulling is likely the same, but maybe double check.\n"
fi

assay_table_path=$(ls a_* | head -n 1)


# checking there is only one sample table, what we're pulling should be the same in multiple, so taking one anyway, but reporting
num_s_prefix_files=$(ls s_* | wc -l | cut -d " " -f 1)

if [ ${num_s_prefix_files} != 1 ]; then
    printf "\n    Just a note that ${curr_GLDS_ID} has more than one sample table. We are going to use the first one,\n"
    printf "    as what we're pulling is likely the same, but maybe double check.\n"
fi

sample_table_path=$(ls s_* | head -n 1)

python ../parse-ISA-tables.py ${curr_GLDS_ID} ${investigation_table_path} ${assay_table_path} ${sample_table_path} output.tmp

cat output.tmp >> ../${2}

cd ../

# rm -rf ${curr_GLDS_ID}
