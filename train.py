import os
import sys
import argparse

import spacy

training_text = "conll/train/conll_train_uncased.txt"
development_text = "conll/dev/conll_dev_uncased.txt"
testing_text = "conll/test/conll_test_uncased.txt"
# the names of these text files could be changed to change input types, e.g., cased, uncased, halfmixed

base_config = 'base_config/base_config_lg.cfg'
# the names of the config file could be changed to change model types, e.g., base_config_sm.cfg for model en_core_web_sm

if __name__ == '__main__':

    # converting the training/development data to the .spacy format
    # before running the following commands, must make sure that there are folders named 'train', 'dev', and 'test' in the directory spacy_files
    # and also that they must be empty folders
    for foldername in ['train','dev','test']:
        if (not(os.path.isdir('spacy_files/'+foldername))) or os.listdir('spacy_files/'+foldername):
            print("ERROR: the folder spacy_files/"+foldername+" must exists and must be an empty directory.")
            sys.exit()
    os.system("python -m spacy convert "+training_text+" spacy_files/train -c ner -n 10")
    os.system("python -m spacy convert "+development_text+" spacy_files/dev -c ner -n 10")
    os.system("python -m spacy convert "+testing_text+" spacy_files/test -c ner -n 10")

    # fill config file
    os.system("spacy init fill-config "+base_config+" config.cfg")

    # start training the model
    os.system("python -m spacy train config.cfg --output ./")

    # evaluate the model
    testing_file = "spacy_files/test/"+os.path.basename(testing_text)[:-4]+".spacy"
    os.system("python -m spacy evaluate model-best "+testing_file)
    
    
