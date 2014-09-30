#!/usr/bin/env python

"""
Converts to NAF a set of semcor files. The inpuyt is a folder with the original structure of SemCor.
Run the program with the parameter -h to get information.
"""

import sys
import os
import glob
from argparse import ArgumentParser
from lib.semcor_to_naf import semcor_file_to_naf


if __name__ == '__main__':
    my_arg_parser = ArgumentParser(description='Convert a Semcor Corpus into NAF format')
    my_arg_parser.add_argument('-i',help='Input folder',dest='in_folder', required=True)
    my_arg_parser.add_argument('-o',help='Output folder',dest='out_folder', required=True)
    my_arg_parser.add_argument('-wn_ver',help='WordNet version of sense annotated in the corpus.', dest='wn_ver', required=True)
    
    
    arguments = my_arg_parser.parse_args()
    
    
    if not os.path.exists(arguments.in_folder):
        print 'The input folder',arguments.in_folder,'can not be found. Closing...'
        sys.exit(0)
        
    ## Check if the output folder exists
    if os.path.exists(arguments.out_folder):
        print 'The output folder',arguments.out_folder,'exists already. Remove first or use another folder. Closing...'
        sys.exit(0)
    
    ## Create the output folder
    os.mkdir(arguments.out_folder)
    
    
    for subfolder in glob.glob(arguments.in_folder+'/brown*'):
        fields = subfolder.split('/')
        subout_folder = arguments.out_folder+'/'+fields[-1]
        os.mkdir(subout_folder)
        print 'Processing subfolder',subfolder
        n = 0 
        
        for infile in glob.glob(subfolder+'/tagfiles/*'):
            fields = infile.split('/')
            outfile = subout_folder+'/'+fields[-1]+'.naf'
            semcor_file_to_naf(infile,outfile, arguments.wn_ver)
            n += 1
        print '\tNumber files converted to NAF:',n
    print
    sys.exit(0)


  
