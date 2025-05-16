import fasttext
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from unidecode import unidecode
from find_label import find_dialect


from collections import defaultdict
from pathlib import Path
import json

def evaluate_predict_single(model, test_file, predictions, save):

    '''
    evaluates a model on a single-dialect file; name of the file = true label
    '''


    
    dialect = test_file.stem
    result_eval = model.test(str(test_file))
    
    f_score = 2*(result_eval[1]*result_eval[2] / (result_eval[1] + result_eval[2]))

        
    with open (save, 'a', encoding='utf-8') as o:
        o.write(f'\nEvaluated dialect: {dialect}.\nNumber of datapoints: {result_eval[0]}\n\tPrecision: {result_eval[1]}\n\tRecall: {result_eval[2]}\n\tF-score: {f_score}.')

    with open(test_file, 'r', encoding='utf-8') as f:
        
        predictions[dialect]['total'] = result_eval[0]

        for line in f.readlines():

            try: 

                label, _ = model.predict(line.strip('\n'))
                label = label[0].replace('__label__', '')
                predictions[dialect][label] +=1
            
            except Exception as e:
                print(f'Encountered an exception while processing {dialect} dialect. Exception: {e}')

def evaluate_predict_mixed(model, test_file, predictions, save, folder):
    '''
    makes predictions based on a single test file with mixed languages; true label is extracted from every line
    '''

    result_eval = model.test(str(test_file))

    f_score = 2*(result_eval[1]*result_eval[2] / (result_eval[1] + result_eval[2]))

    with open (save, 'w', encoding='utf-8') as o:
        o.write(f'Number of datapoints: {result_eval[0]}\n\tPrecision: {result_eval[1]}\n\tRecall: {result_eval[2]}\n\tF-score: {f_score}.')

    with open(test_file, 'r', encoding='utf-8') as f:
        

        for line in f.readlines():

            try: 

                dialect = line.split('\t')[0].replace('__label__', '').lstrip('\ufeff') #extract true label

                label, _ = model.predict(line.strip('\n'))
                label = label[0].replace('__label__', '')

                #get true dialects for models trained without dialect labels
                if label == 'uk': #don't check if it's another language
                    dialect = find_dialect(line.split('\t')[1].strip(), test_file, source_dir=folder)
                #end of relevant part

                

                predictions[dialect][label] +=1
            
            except Exception as e:
                print(f'Encountered an exception while processing {dialect} dialect. Exception: {e}')


def main():

    folder = Path('./path/to/labelled/files')
    model = fasttext.load_model('./path/to/model')
    predictions = defaultdict(lambda: defaultdict(int))
    
    #run eval on multiple files in a directory
    for file in folder.iterdir():
        if file.is_file():

            evaluate_predict_single(model, file, predictions, 'path/to/save/results')
    
    #run eval on a single test file - for new or finetuned models

    evaluate_predict_mixed(model=model, 
                           test_file=Path('./path/to/test/file'), 
                           predictions=predictions, 
                           save='./path/to/save/logs',
                           folder=folder)
   
    #predictions - save the dictionary, visualize the results, etc.
        
if __name__ == '__main__':
    main()
      
