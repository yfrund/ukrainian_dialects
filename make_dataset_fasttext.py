import os
from unidecode import unidecode
from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue
import random
from pathlib import Path


def make_dataset(file: str):
    '''prepare all sentences in the same format: 
                                                __label__label    sentence
                                                '''

    with open(file, 'r', encoding='utf-8') as i:
        sents = i.readlines()
        with open(f'./labelled_fasttext/no_dialects/{unidecode(os.path.splitext(os.path.basename(file))[0]).lower()}.txt', 'a', encoding='utf-8') as o:
            for sentence in sents:
                #dialect code = 5 first letters of the transliterated dialect name
                dialect_code = unidecode(os.path.splitext(os.path.basename(file))[0]).lower()[:5]
                
                try:
                    sent = sentence.split('\t')[1]
                    label = Lang(os.path.splitext(os.path.basename(file))[0].split('_')[0]).pt1 #convert ISO 639-3 to 639-1
                    
                    o.write(f'__label__{label}\t{sent}') 
                except (IndexError, InvalidLanguageValue):
                    #o.write(f'__label__uk_{dialect_code}\t{sentence}')
                    o.write(f'__label__uk\t{sentence}')
                     

def downsample_split_upsample(directory: Path, samples: int, temp: list, test_portion=0.2,  min_test=10) -> list:
    '''
    params:
    directory = folder with files per dialect or language
    samples = number of samples per class
    test_portion = the proportion of data that should be allocated to the test set; default = 20%
    min_test = minimal number of datapoints to be allocated to the test set; default = 10 datapoints
    '''
    
    train, test = [], []
    temp.append(test_portion)
    test_samples = int(samples * test_portion) # number of datapoints in the test set per class
    train_samples = int(samples * (1-test_portion))

    
    for file in directory.iterdir():
        if file.is_file():
            with open(file, 'r', encoding = 'utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]

                if len(lines) > test_samples:
                    sample_test = random.sample(lines, test_samples)
                    test = test + sample_test


                    remainder = [sent for sent in lines if sent not in sample_test]

                    if len(remainder) > train_samples:

                        sample_train = random.sample(remainder, train_samples)
                        train = train + sample_train


                    else:
                        
                        #upsample
                        multiply = int(train_samples / len(remainder)) + 1 #always round upwards
                        
                        train = train + remainder*multiply

                        

                else:
                    sample = random.sample(lines, min_test)
                    test = test + sample


                    remainder = [sent for sent in lines if sent not in sample_test]

                    if len(remainder) > train_samples:

                        sample_train = random.sample(remainder, train_samples)
                        train = train + sample_train

                    else:
                        
                        #upsample
                        multiply = round(train_samples / len(remainder))
                        
                        train = train + remainder*multiply
                       

    
    if not balanced_proportions(train, test, test_portion=temp[0]):
        train, test = downsample_split_upsample(directory, samples, temp, test_portion=test_portion+0.01)

    random.shuffle(train)
    random.shuffle(test)
    temp = []
    return train, test

def balanced_proportions(train, test, test_portion):
    '''
    checks if the proportions of the train / test split are respected
    '''

    test_part = len(test)/(len(train)+len(test))
    print(f'test part: {test_part}, test portion: {test_portion}')

    if test_part < test_portion:
        return False
    
    return True




def main():

    ...


if __name__ == '__main__':
    main()