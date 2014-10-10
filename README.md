#Converter from semcor format to NAF format#

Scripts to convert files in semcor format, into NAF format. There are 2 scripts:
* convert_file.py --> converts a single file
* convert_corpus.py -> converts a whole corpus
* add_synset_ids.py -> add synset ids to a set of NAF files

API documentation can be found at http://kyoto.let.vu.nl/~izquierdo/api/semcor_to_naf

#Installation and requirements#

You will need to have the KafNafParserPy library installed. You can clone it from our CLTL repository. These are the steps required
after cloning this repository:
```shell
cd path_where_you_cloned_the_semcor_to_naf
cd lib
git clone https://github.com/cltl/KafNafParserPy.git
```

This should be enough. You will need to have lxml (http://lxml.de) installed in order to use the KafNafParser. If you have `pip` installed
you can install lxml very easy:
```shell
pip install lxml
```


#Converting a single file#

The script convert_file.py reads from the standard input and writes in the standard output, so you need just to do:
```shell
cat semcor.file | convert_file.py eng16> naf.file
```

There is only one extra parameter required (eng16) which is a label indicating the wordnet version of the sense annotations. It will be included
in the resource of the external references, to keep track of the exact version of the sense annotation.

#Converting a whole corpus#

The script convert_corpus.py gets a SemCor corpus (for a given version) and an output folder, and convert all the files in the input folder
into NAF format. You can get information about the expected parameters by calling to the script with the -h option.
```shell
convert_corpus.py -h
usage: convert_corpus.py [-h] -i IN_FOLDER -o OUT_FOLDER

Convert a Semcor Corpus into NAF format

optional arguments:
  -h, --help     show this help message and exit
  -i IN_FOLDER   Input folder
  -o OUT_FOLDER  Output folder
  -wn_ver WN_VER  WordNet version of sense annotated in the corpus.
```

The expected structure of the input folder is the typical structure of the SemCor corpus as can be found at http://www.cse.unt.edu/~rada/downloads.html#semcor
```shell
semcor1.6
  brown1
    tagfiles
      *
  brown2
    tagfiles
      *
  brownv
    tagfiles
      *
```

The structure of the output folder is similar, removing the tagfiles subfolder:
```shell
semcor1.6
  brown1
    *.naf
  brown2
    *.naf
  brownv
    *.naf
```

These are the steps to get the version 1.6 of Semcor in NAF after installing this repository:
```shell
cd path_where_you_cloned_the_semcor_to_naf
wget http://lit.csci.unt.edu/~rada/downloads/semcor/semcor1.6.tar.gz
tar xzf semcor1.6.tar.gz
convert_corpus.py -i semcor1.6 -o semcor1.6_naf -wn_ver eng16
```

You will get the semcor1.6 in NAF format in the folder `semcor1.6_naf`

#Adding synset id information#

The original sense information on the SemCor corpus is just the sense number, and the lexical key. With the script add_synset_ids.py you will be able to add the synset
id information to a set of NAF files. There are three options to specify the input of this script:
* A folder, as created by the script convert_corpus.py, with the same structure
* A file containing a list of paths to NAF files
* A single NAF file

In all the cases, the modification of the files is done in place, so no new files are generated but the input files themselves. You will be to have the WordNet plain text files
for the correct version in your machine, you can download them from http://wordnet.princeton.edu/wordnet/download. Information about the inputa parameters can be found by running
the script with the -h option.
```shell
add_synset_ids.py -h
usage: add_synset_ids.py [-h] (-i INPUT_FOLDER | -l LIST_FILES | -f FILE) -wn
                         WN -wn_ver WN_VERSION

Script to add synset ids to NAF files, modifying the files in place.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FOLDER, -input_folder INPUT_FOLDER
                        Input folder
  -l LIST_FILES, -list_files LIST_FILES
                        File with paths to files
  -f FILE, -file FILE   Single NAF filename
  -wn WN                Path to WordNet plain text files
  -wn_ver WN_VERSION    Version code of the WordNet used, will be included in
                        the synset ids
```

One parameter is the input file or files, another one is the path to your local WordNet and finally you have to provide them wordnet version used, as it will be included in the synset
ids, to generate labels like `eng16-00022819-r`. Below you can find one example of how to use this script.
```shell
python add_synsets_ids.py -wn wordnet-1.6 -wn_ver eng16 -f semcor1.6_naf
```

This would modify all the files in semcor_1.6_naf/brown[12v]/*.naf and will include the synset ids, reading the WordNet information from the folder `wordnet-1.6`.

#Putting all together#

These are the steps that you should follow in order to get a clean copy of a certain version of SemCor, convert it to NAF and add the synset information. We will consider that
you are interested in the original SemCor, which has sense information annotated according WordNet 1.6.
```shell
git clone https://github.com/cltl/semcor_to_naf.git
cd semcor_to_naf
wget http://lit.csci.unt.edu/~rada/downloads/semcor/semcor1.6.tar.gz
tar xzf semcor1.6.tar.gz
wget http://wordnetcode.princeton.edu/1.6/wn16.unix.tar.gz
tar xvf wn16.unix.tar.gz
python convert_corpus.py -i semcor1.6 -o semcor1.6_naf -wn_ver eng16
python add_synset_ids.py -i semcor1.6_naf -wn wordnet-1.6 -wn_ver eng16
```

All these step will end up with the folder `semcor1.6_naf` with three subfolders (brown1,brown2 and brownv), with all files converted to NAF and with the synset identifiers included,
for instance this is how the instance of the verb say in the SemCor corpus looks like (file semcor1.6/brown1/tagfiles/br-a01) and how it is converted to NAF.
```shell
    <wf cmd=done pos=VB lemma=say wnsn=1 lexsn=2:32:00::>said</wf>
    
    ...
    
    
    <term id="t2" pos="VB" lemma="say" type="close">
      <span>
        <target id="w2"/>
      </span>
      <externalReferences>
        <externalRef confidence="1.0" reference="1" resource="WordNet-eng16" reftype="sense_number"/>
        <externalRef confidence="1.0" reference="2:32:00::" resource="WordNet-eng16" reftype="lexical_key"/>
        <externalRef confidence="1.0" resource="WordNet-eng16" reference="eng16-00682542-v" reftype="synset"/>
      </externalReferences>
    </term>
```
All these steps are grouped in the script `get_my_semcor.sh` that can be found in this repository and you can run directly or modify to your own needs, for selecting a certain version
or folder names. Keep in mind that the version of the WordNet used for the SemCor corpus selected has to match to the version of the WordNet indicated to the `add_synset_ids.py` in
order to be able to generate the correc synset identifiers.

#Documentation#
The documentation can be generated automatically by running:
```shell
epydoc --config documentation.cfg
```

This will call to the external program epydoc (http://epydoc.sourceforge.net/) with the provided configuration file, and will create the HTML documents
for the API in the folder `apidocs`. As said before the already generated documentation can be seen at http://kyoto.let.vu.nl/~izquierdo/api/semcor_to_naf

#Contact#
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl  rubensanvi@gmail.com
* http://rubenizquierdobevia.com/

