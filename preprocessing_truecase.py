import sys
import random

def preprocessing_input(filename):
    infile = open(filename+'_cased.txt', 'r')
    lines = infile.readlines()
    infile.close()

    # parse the (cased) input file
    doc = []
    sentence = []
    for line in lines:
        linesplit = line.strip().split()
        if(len(linesplit)>=4): # line with data
            sentence.append(linesplit)
        else: # empty line; end of sentence
            doc.append(sentence)
            sentence = []
    if(len(sentence)>0):
        doc.append(sentence)

    # create a text file to be truecased (one sentence per line)
    filename2 = (('/').join(filename.split('/')[:-1]))+'/truecaser/'+filename.split('/')[-1]
    # for example, if filename is 'conll/train/conll_train' then filename2 is 'conll/train/truecaser/conll_train'
    outfile = open(filename2+'_truecase_input.txt','w')
    for sentence in doc:
        outfile.write(" ".join([token[0].lower() for token in sentence])+"\n")
    outfile.close()

    # truecase that file. This takes time
    os.system("allennlp predict wiki-truecaser-model.tar.gz "+filename2+"_truecase_input.txt --output-file "+filename2+"_truecase_output.txt \
    --include-package mylib --use-dataset-reader --predictor truecaser-predictor --silent")

    # replace the token[0] (i.e. the word) in each token with the truecased word
    infile = open(filename2+'_truecase_output.txt', 'r')
    lines = infile.readlines()
    infile.close()
    for i_line, line in enumerate(lines):
        linesplit = line.strip().split(" ")
        for i_word, word in enumerate(linesplit):
            if(word.lower()!='-docstart-'):
                doc[i_line][i_word][0] = word # this line is replacing the word with the truecased version
            else:
                doc[i_line][i_word][0] ='-DOCSTART-'

    # write that to a text file
    outfile = open(filename+'_truecased.txt','w')
    for sentence in doc:
        for token in sentence:
            outfile.write(" ".join(token)+"\n")
        outfile.write("\n")
    outfile.close()

if __name__ == '__main__':

    for suffix in ['train','dev','test']:
        preprocessing_input('conll/'+suffix+'/conll_'+suffix) # for example, 'conll/train/conll_train'
    
    
