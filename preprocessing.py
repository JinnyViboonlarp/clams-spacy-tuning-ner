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

    # create an uncased output
    outfile = open(filename+'_uncased.txt','w')
    for sentence in doc:
        for token in sentence:
            if(token[0]!='-DOCSTART-'):
                outfile.write(" ".join([token[0].lower(),token[1],token[2],token[3]])+"\n")
            else:
                outfile.write(" ".join(token)+"\n")
        outfile.write("\n")
    outfile.close()

    # create a CU (cased concat with uncased) output
    infile = open(filename+'_cased.txt', 'r')
    lines = infile.readlines()
    infile.close()
    outfile = open(filename+'_CU.txt','w')
    outfile.writelines(lines)
    outfile.write("\n")

    infile = open(filename+'_uncased.txt', 'r')
    lines = infile.readlines()
    infile.close()
    outfile.writelines(lines)
    outfile.close()

    # create a half-mixed output
    # first, create a list of index of "sentence" that is not really a sentence (i.e. the one with -DOCSTART-')
    docstart_list = [i for i in range(len(doc)) if doc[i][0][0] == '-DOCSTART-']
    n_sentences = len(doc)-len(docstart_list)
    if('train' in filename):
        print("number of sentences in training data: ",n_sentences) # 14041 sentences
    elif('dev' in filename):
        print("number of sentences in validation data: ",n_sentences) # 3250 sentences
    elif('test' in filename):
        print("number of sentences in testing data: ",n_sentences) # 3453 sentences
    random.seed(1)
    # randomly choosing half of the indices of the sentences, the rest would be uncased
    index_list = list(range(len(doc)))
    index_list = [index for index in index_list if index not in docstart_list]
    index_list = random.sample(index_list, int(n_sentences/2))
    outfile = open(filename+'_halfmixed.txt','w')
    for i, sentence in enumerate(doc):
        if(i in index_list or i in docstart_list):
            for token in sentence:
                outfile.write(" ".join(token)+"\n")
        else:
            for token in sentence:
                outfile.write(" ".join([token[0].lower(),token[1],token[2],token[3]])+"\n")
        outfile.write("\n")
    outfile.close()

if __name__ == '__main__':

    for suffix in ['train','dev','test']:
        preprocessing_input('conll/'+suffix+'/conll_'+suffix) # for example, 'conll/train/conll_train'
    
    
