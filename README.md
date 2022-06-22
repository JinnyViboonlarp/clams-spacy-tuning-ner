# clams-spacy-tuning-ner
This repository describes how to train a spaCy NER model that is optimized for lowercase data.

The data used for training is the CoNLL 2003 English dataset. As per the method described in https://aclanthology.org/D19-1650.pdf, there are many different casing scenario for the training/validation/testing data:
  - **Cased**: The data is unmodified from the original CoNLL dataset.
  - **Uncased**: The data is lowercased.
  - **CU (cased + uncased)**: The .txt files of the cased and uncased data are concatenated.
  - **Halfmixed**: Half of the sentences are randomly selected to be lowercased.
  - **Truecased**: The data is lowercased, and then is passed through a Truecaser model from https://github.com/mayhewsw/pytorch-truecaser 

Since we want to optimize the model for the data in which no casing information is presented, only the uncased and truecased versions of the validation/testing set is used. From my experiments, the model performs best when its input data (training/validation/testing set) is all uncased, and second-best when the data is all truecased.

I have experimented with three spaCy model architectures: `en_core_web_sm`, `en_core_web_md`, and `en_core_web_lg`. Not surprisingly, the largest model (`en_core_web_lg`) achieves the highest F1-score (which is, F1=84.29 when trained with uncased data, and F1=83.61 when trained with truecased data), but it also takes the longest to train.

Two of the small models (with folder size of 13 MB) are in the folder `trained_models` of this repository
  - `model-best-uncased-sm`: trained, validated, and tested on uncased data on the `en_core_web_sm` pretrained model. F1=80.70
  - `model-best-truecased-all-sm`: trained, validated, and tested on truecased data on the `en_core_web_sm` pretrained model. F1=80.09

## Requirements

This project requires spaCy (>=3.0). It is recommended that you install spaCy by following instructions from https://spacy.io/usage . The specific model(s) that would be trained also needs to be downloaded and installed, e.g., via `python -m spacy download en_core_web_sm`

For the Truecaser model, the requirements are python (3.6), allennlp (0.8.2), and spaCy (<2.1,>=2.0). This requirement of the older version of spaCy conflicts with the requirement for this project. It is not recommended for you to download the Truecaser model to truecase the data, since the truecased data is already provided in the folder `conll`

## Training the model

To train the best-performing model (`en-core-web-lg` trained on uncased data), first make sure that all the subdirectories in the folder `spacy_files` are empty, then run `python train.py` in your terminal.

The file `train.py` could be edited to change the paths to the data and the model’s config file (which would select the model architecture, e.g. `base_config_sm.cfg` would select the model `en_core_web_sm`).

## Pre-processing

To create dataset with different casing scenarios from the original cased CoNLL data, the codes `preprocessing.py` and `preprocessing_truecase.py` are used. You do not have to run these codes since all versions of the data (e.g. cased, uncased, truecased) are provided in the folder `conll`








