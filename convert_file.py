#!/usr/bin/env python

"""
Converts a single file from semcor format to NAF.

The program reads from the standard input and writes to the standard output. It has just one parameter,
the WordNet version of the senses in the input file, that will be used to generate the resource attribute in
the external references.

Usage:
\tcat my_semcorfile | python convert_file.py eng16
"""

from lib.semcor_to_naf import semcor_file_to_naf
import sys

if sys.stdin.isatty():
    print>>sys.stderr,'Script to convert a SemCor file to NAF format. Usage:'
    print>>sys.stderr,'  cat semcor.file |',sys.argv[0],' wnver (1.6) corpus_id (SemCor) > naf.file'
    sys.exit(-1)

semcor_file_to_naf(sys.stdin,sys.stdout,sys.argv[1],corpus_id = sys.argv[2])
  
