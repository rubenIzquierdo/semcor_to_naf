#!/bin/bash

#This script automatically downloads the SemCor corpus, converts it to NAF and adds the synset ids

#Get the version 1.6 of Semcor
wget http://lit.csci.unt.edu/~rada/downloads/semcor/semcor1.6.tar.gz

#Unzip it. It will generate the folder semcor1.6
tar xzf semcor1.6.tar.gz
rm semcor1.6.tar.gz

#Get the version 1.6 of WordNet
wget http://wordnetcode.princeton.edu/1.6/wn16.unix.tar.gz

#Unzip it in wordnet-1.6
tar xzf wn16.unix.tar.gz
rm wn16.unix.tar.gz

#Convert the original corpus into NAF, in the folder semcor1.6_naf
python convert_corpus.py -i semcor1.6 -o semcor1.6_naf -wn_ver eng16 -corpus SemCor16

#Add the synset information to the NAF files
python add_synset_ids.py -i semcor1.6_naf -wn wordnet-1.6 -wn_ver eng16
