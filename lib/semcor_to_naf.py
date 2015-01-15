#!/usr/bin/env python

"""
This module implements functions to convert files from SemCor format
to NAF format
"""
import re
from KafNafParserPy import *


def get_fields(this_line):
    """
    Takes a line from semcor, parses it and returns it as a dictionary
    For <wf id=a lemma=b>hi</wf> would created m['id']=a m['lemma']=b m['text']=hi
    
    @type  this_line: string
    @param this_line: line from SemCor
    @rtype:  map
    @return: map with the attributes
    """
    ret = {}
    fields = this_line.strip().split('>')
    attribs = fields[0].split(' ')
    text = fields[1].split('<')[0]
    ret['text'] = text
    for at in attribs:
        pair = at.split('=')
        if len(pair) == 2:  #To avoid <wf
            ret[pair[0]] = pair[1]
    return ret
        
def semcor_file_to_naf(input_file, output_file,wn_ver,corpus_id='corpus_id'):
    """
    Takes an input file in SemCor format and converts it to NAF in outfile.
    
    @type input_file: string or file descriptor
    @param input_file: the filename of the input file, or an open file descriptor to the input file
    @type output_file: string or file descriptor
    @param output_file: the filename of the output file, or an open file descriptor to the input file
    @type wn_ver: string
    @param wn_ver: the wnversion of the senses in the input file. It will be used to create the resource
                label of the external references
    """
    
    #Both parameter can be string or file descriptor, so we check if the files are not open to open them
    re_p = re.compile('pnum=([0-9]+)')
    re_s = re.compile('snum=([0-9]+)')
    if isinstance(input_file, str):
        input_file = open(input_file,'r')
        
    out_obj = KafNafParser(type='NAF')
    current_p = None
    current_s = None
    current_offset = 0
    current_token = 0
    for line in input_file:
        if line.startswith('<p '):
            num_p = re.search(re_p,line).groups()[0]
            current_p = num_p
        elif line.startswith('<s '):
            num_s = re.search(re_s,line).groups()[0]
            current_s = num_s
        elif line.startswith('<wf') or line.startswith('<punc'):
            fields = get_fields(line)

            token = fields.get('text')

            new_token = Cwf(type='NAF')
            new_token.set_text(token)
            new_token.set_id('w'+str(current_token))
            new_token.set_offset(str(current_offset))
            new_token.set_sent(current_s)
            if current_p is not None:
                new_token.set_para(current_p)
            out_obj.add_wf(new_token)

            
            if line.startswith('<wf'):
                new_term = Cterm(type='NAF')
                new_term.set_id('t'+str(current_token))
                pos = fields.get('pos')
                new_term.set_pos(pos)
                lemma = fields.get('lemma')
                if lemma is None:
                    new_term.set_lemma(token.lower())
                else:
                    new_term.set_lemma(lemma)
                    
                cmd = fields.get('cmd')
                if cmd == 'ignore':
                    new_term.set_type('open')
                else:
                    new_term.set_type('close')
                    
                term_span = Cspan()
                term_span.create_from_ids([new_token.get_id()])
                new_term.set_span(term_span)
                    
                wnsn = fields.get('wnsn')
                lexsn = fields.get('lexsn')
                if wnsn is not None or lexsn is not None:
                    if wnsn is not None:
                        ext_ref = CexternalReference()
                        ext_ref.set_confidence('1.0')
                        ext_ref.set_reference(wnsn)
                        ext_ref.set_resource('WordNet-'+str(wn_ver))
                        ext_ref.set_reftype('sense_number')
                        new_term.add_external_reference(ext_ref)
                    
                    if lexsn is not None:
                        ext_ref2 = CexternalReference()
                        ext_ref2.set_confidence('1.0')
                        ext_ref2.set_reference(lexsn)
                        ext_ref2.set_resource('WordNet-'+str(wn_ver))
                        ext_ref2.set_reftype('lexical_key')
                        new_term.add_external_reference(ext_ref2) 

                # This is to include the id in case
                this_id = fields.get('id')
                if this_id is not None:
                    ext_ref = CexternalReference()
                    ext_ref.set_reference(this_id)
                    ext_ref.set_resource(corpus_id)
                    ext_ref.set_reftype('original_id')
                    new_term.add_external_reference(ext_ref)
                    
                out_obj.add_term(new_term)
                
            current_token += 1
            current_offset += (len(token)+1)        
    input_file.close()
    out_obj.add_linguistic_processor('text', Clp(name='SemCor tokenisation',version='1.0'))
    out_obj.add_linguistic_processor('terms', Clp(name='SemCor Brill POS',version='1.0'))
    out_obj.add_linguistic_processor('terms', Clp(name='SemCor Manual sense annotation',version='1.0'))

    out_obj.dump(output_file)
    
if __name__ == '__main__':
    import glob
    #for file in glob.glob('semcor1.6/brown*/tagfiles/*'):
    file = 'semcor1.6/brown1/tagfiles/br-a01'
    semcor_file_to_naf(file, 'ruben')
