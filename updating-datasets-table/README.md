
# PURPOSE  

- We have this spreadsheet of datasets available from GeneLab: https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo  
- We want to update it to add on any new ones

This repo holds what I hacked together to automate this. It starts with a text file holding all the currently held GLDS IDs from column A in our [spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo).

It starts with a text file of all the GLDS IDs in the current 

The result table from this is "GLDS-strain-info.tsv" above, and I added the info as a new column to the [master spreadsheet](https://docs.google.com/spreadsheets/d/1PfNkLWrcs-D5Yx9nqNYDHqNygJfk9nhmDW6A0-b_3Zo) called "strain/ecotype listed".   

# General process
- get full list of all avalable GLDS IDs and compare it to the list of ones we have to make a list of just the ones we're missing
- for each one we're missing
    - get the ISA zip
    - get the study table from the ISA zip
    - parse it to create the info we want as closely as possible


# Updating on 7-Feb-2023

## Getting list of wanted GLDS IDs
I manually put all the GLDS IDs we have in our spreadsheet already into a text file called "7-Feb-2023-currently-held-GLDS-IDs.txt".

```bash
# sorting and uniquing the ones we currently have
sort -u 7-Feb-2023-currently-held-GLDS-IDs.txt > t && mv t 7-Feb-2023-currently-held-GLDS-IDs.txt

# getting all available GLDS IDs (link based on visualization api here: https://visualization.genelab.nasa.gov/GLOpenAPI/)
curl https://visualization.genelab.nasa.gov/GLOpenAPI/assays/?format=tsv | tr -d '"' | grep -v "^#" | cut -f 1 | sort -u > 7-Feb-2023-all-current-GLDS-IDs.txt

# getting list of just those we don't have (important they are both sorted and uniqued as done above before this)
comm -13 7-Feb-2023-currently-held-GLDS-IDs.txt 7-Feb-2023-all-current-GLDS-IDs.txt > 7-Feb-2023-currently-wanted-GLDS-IDs.txt

wc -l 7-Feb-2023-all-current-GLDS-IDs.txt
# 377

wc -l 7-Feb-2023-currently-held-GLDS-IDs.txt
# 331

    # so there should be 46 we are missing
wc -l 7-Feb-2023-currently-wanted-GLDS-IDs.txt
# 46
    # good to move on with these target GLDS-IDs
```

## Running the above scripts on those files

This utilizes my genelab-utils program, which can be installed with conda/mamba like so:

```bash
# if you don't have the faster drop-in mamba already
conda install -n base -c conda-forge mamba
mamba create -n genelab-utils -c conda-forge -c bioconda -c defaults -c astrobiomike genelab-utils=1.2.12

conda activate genelab-utils
```

```bash
# running script with wanted input GLDS IDs
bash get-info-for-GLDS-IDs.sh 7-Feb-2023-currently-wanted-GLDS-IDs.txt GL-dataset-info.tsv
```

The output GL-dataset-info.tsv table looks like this:

```
GLDS      Study Title                                                                                                                                                                              Assay(s)                         Measument Type(s)                                     Organism(s)                                                                                                                                                                          Factor(s)                                    Sex                 Age                 Strain
GLDS-110  The influence of simulated microgravity on the proteome of Daphnia magna                                                                                                                 gel electrophoresis, proteomics  protein expression profiling, protein identification  Daphnia magna                                                                                                                                                                        Weightlessness Simulation                    Not auto-detected.  Not auto-detected.  Not auto-detected.
GLDS-115  Gene expression profiling in human fibroblast after low-LET irradiation                                                                                                                  microarray                       transcription profiling                               Homo sapiens                                                                                                                                                                         Irradiation, Timepoint                       Not auto-detected.  Not auto-detected.  Not auto-detected.
GLDS-132  Whole genome sequencing and assembly of Eukaryotic microbes isolated from ISS environmental surface, Kirovograd region soil, Chernobyl Nuclear Power Plant and Chernobyl Exclusion Zone  nucleotide sequencing            genome sequencing                                     Cladosporium cladosporioides, Aspergillus niger, Aspergillus terreus, Beauveria bassiana, Trichoderma virens, Aureobasidium pullulans, Fusarium solani, Cladosporium sphaerospermum  radiation                                    Not auto-detected.  Not auto-detected.  IMV 01167, IMV 00236, IMV 00045, IMV 00454, IMV 00293, nan, IMV 00882, IMV 00265
GLDS-177  Draft Genome Sequences of Two Fusarium oxysporum Isolates Cultured from Infected Zinnia hybrida Plants Grown on the International Space Station                                          nucleotide sequencing            genome sequencing                                     Fusarium oxysporum                                                                                                                                                                   Spaceflight                                  Not auto-detected.  Not auto-detected.  VEG-01C1, VEG-01C2
GLDS-2    Response of human lymphoblastoid cells to HZE (iron ions) or gamma-rays                                                                                                                  microarray                       transcription profiling                               Homo sapiens                                                                                                                                                                         Ionizing Radiation, Absorbed Radiation Dose  Not auto-detected.  Not auto-detected.  Not auto-detected.
GLDS-262  Draft Genome Sequence of Solibacillus kalamii, Isolated from an Air Filter Aboard the International Space Station                                                                        nucleotide sequencing            genome sequencing                                     Solibacillus kalamii                                                                                                                                                                 Spaceflight                                  Not auto-detected.  Not auto-detected.  ISSFR-015
```

I added the new rows to the bottom of our spreadsheet and organized the columns as needed.
