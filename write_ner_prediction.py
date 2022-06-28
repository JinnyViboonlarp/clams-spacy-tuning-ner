import sys
import spacy
from spacy.tokens import Doc

def write_ner_prediction(model_path, infile_path, outfile_path):

    nlp = spacy.load(model_path)
    infile = open(infile_path, 'r')
    lines = infile.readlines()
    infile.close()
    
    # parse the input file
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

    # append the prediction to the end of each token
    # also create a confusion dict (which, like a confusion matrix, store the frequency of (correct_label,predict_label) pairs
    confusion_dict = {}
    for i_sentence, sentence in enumerate(doc):
        sentence_text = [token[0].lower() for token in sentence]
        text = Doc(nlp.vocab, sentence_text)
        predicted_sentence = nlp(text)
        for i_token, token in enumerate(predicted_sentence):
            iob_type = token.ent_iob_ if token.ent_iob_=='O' else (token.ent_iob_+'-'+token.ent_type_)
            doc[i_sentence][i_token].append(iob_type)
            # add to confusion dict, the key is the tuple (correct_label,predict_label) without the IOB prefixation
            correct_label = sentence[i_token][3].split('-')[-1] # 'O' if no type i.e. token_ent_type_ is an empty string
            predict_label = iob_type.split('-')[-1] 
            confusion_dict[(correct_label,predict_label)] = confusion_dict.get((correct_label,predict_label),0) + 1
        if(((i_sentence+1)%100)==0):
            print((i_sentence+1),"sentences predicted from",len(doc))
    print("finish predicting all sentences")

    # write that to a text file
    outfile = open(outfile_path,'w')
    for sentence in doc:
        for token in sentence:
            outfile.write(" ".join(token)+"\n")
        outfile.write("\n")
    outfile.close()

    # also write confusion dict to a text file
    outfile = open('model_confusion.txt','w')
    outfile.write("input file = "+infile_path+"\n")
    outfile.write("model = "+model_path+"\n\n")
    sorted_keys = sorted(confusion_dict,key=confusion_dict.get,reverse=True)
    for (correct_label,predict_label) in sorted_keys:
        outfile.write(correct_label+' -> '+predict_label+': '+str(confusion_dict[(correct_label,predict_label)])+"\n")
    outfile.close()   

if __name__ == '__main__':
    model_path = "trained_models/model-best-uncased-sm"
    infile_path = "conll/test/conll_test_uncased.txt"
    outfile_path = infile_path[:-4]+"_with_prediction.txt"

    write_ner_prediction(model_path, infile_path, outfile_path)
    
    
