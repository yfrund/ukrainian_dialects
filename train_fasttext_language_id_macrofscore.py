import fasttext
import numpy as np
from sklearn.metrics import classification_report
from sklearn.exceptions import UndefinedMetricWarning
from collections import defaultdict
from pathlib import Path
from detect_language import evaluate_predict_mixed


def train(train_set: str, test_set: str, save: str, logs: str, lr: list, epochs: list, wordNgrams: list, dims: int, pretrainedVectors: str = None, minn: int = None, maxn: int = None):
    '''
    performs hyperparameter tuning and saves the model with the highest f-score
    params:
        train_set, test_set, save, logs, pretrainedVectors: paths
            save: to save the model

        lr, epochs, wordNgrams, dims: lists
            lr: learning rate
            wordNgrams: ngram size to include as additional information, typically 1-4
            dims: vector dimensionality; equals vector dimensionality of pretrainedVectors if pretrainedVectors != None

        minn: minimum sizes of character n-grams
        maxn: maximum sizes of character n-grams

        pretrainedVectors: path to the .vec file
        
    '''

    
    max_macro_f1 = 0
    

    for rate in lr:
        for epoch_num in epochs:

            for ngram_val in wordNgrams:

                if pretrainedVectors:

                    if minn and maxn:

                        model = fasttext.train_supervised(input=train_set,
                                                            lr=rate, 
                                                            epoch=epoch_num, 
                                                            wordNgrams=ngram_val, 
                                                            pretrainedVectors=pretrainedVectors, 
                                                            dim=dims,
                                                            minn=minn,
                                                            maxn=maxn
                                                            )

                    else:
                        model = fasttext.train_supervised(input=train_set,
                                                            lr=rate, 
                                                            epoch=epoch_num, 
                                                            wordNgrams=ngram_val, 
                                                            pretrainedVectors=pretrainedVectors, 
                                                            dim=dims,
                                                            ) 
                   
                   
                   
                    y_true, y_pred = [], []
                    with open(test_set, 'r', encoding='utf-8') as f:
                        for line in f:
                            label = line.split('\t')[0]
                            text = line.split('\t')[1]
                            y_true.append(label)

                            
                            y_pred.append(model.predict(text.strip('\n'))[0][0])
                            

                    
                    report = classification_report(y_true, y_pred, output_dict=True, zero_division=np.nan)
                   
                    for label, metrics in report.items():
                        if label in ['accuracy', 'macro avg', 'weighted avg']: #to skip non-class entries
                            continue
                        if np.isnan(metrics['precision']):
                            print(f'Label {label} has 0 predictions.')
                        elif np.isnan(metrics['recall']):
                            print(f'Label {label} exists in test set but had no true positives')

                    macro_f1 = report['macro avg']['f1-score']



                    if macro_f1 > max_macro_f1:
                        max_macro_f1 = macro_f1

                        message = f'Saving best model with macro F-score {macro_f1}, trained for {epoch_num} epochs with LR {rate}, {dims} vector dimensions, {minn} minn, {maxn} maxn and {ngram_val}-wordGrams.\n'
                        print(message)
                        with open(logs, 'a', encoding='utf-8') as f:
                            f.write(message)
                        model.save_model(save)


                else:

                    if minn and maxn:
                        model = fasttext.train_supervised(input=train_set, 
                                                            lr=rate, 
                                                            epoch=epoch_num, 
                                                            wordNgrams=ngram_val, 
                                                            dim=dims,
                                                            minn=minn,
                                                            maxn=maxn)
                        
                    else:
                        model = fasttext.train_supervised(input=train_set,
                                                          lr=rate,
                                                          epoch=epoch_num,
                                                          wordNgrams=ngram_val,
                                                          dim=dims)

                    
                    y_true, y_pred = [], []
                    with open(test_set, 'r', encoding='utf-8') as f:
                        for line in f:
                            label = line.split('\t')[0]
                            text = line.split('\t')[1]
                            y_true.append(label)
                            y_pred.append(model.predict(text.strip('\n'))[0][0])

                    report = classification_report(y_true, y_pred, output_dict=True, zero_division=np.nan)

                    for label, metrics in report.items():
                        if label in ['accuracy', 'macro avg', 'weighted avg']: #to skip non-class entries
                            continue
                        if np.isnan(metrics['precision']):
                            print(f'Label {label} has 0 predictions.')
                        elif np.isnan(metrics['recall']):
                            print(f'Label {label} exists in test set but had no true positives')

                    macro_f1 = report['macro avg']['f1-score']



                    if macro_f1 > max_macro_f1:
                        max_macro_f1 = macro_f1

                        message = f'Saving best model with macro F-score {macro_f1}, trained for {epoch_num} epochs with LR {rate}, {dims} vector dimensions, {minn} minn, {maxn} maxn and {ngram_val}-wordGrams.\n'
                        print(message)
                        with open(logs, 'a', encoding='utf-8') as f:
                            f.write(message)
                        model.save_model(save)
            



def main():

    print('Start training models...')

    #perform hyperparameter tuning and save the model with the highest macro F-score

    dims = []
    lr = []
    epochs = []
    wordNgrams = []
    minns = []
    maxns = []
    pretrainedVectors = './fasttext_model/pretrained_vectors.vec'

    

    print('Training models without pretrained vectors...')

    for dim in dims:
        
        train_set = f'./path/to/train/set'
        test_set = f'./path/to/test/set'
        

        for min_n in minns:
            for max_n in maxns:

                logs = f'./path/to/save/logs/logs_{dim}dims_{min_n}minn_{max_n}maxn.txt'
                save = f'./path/to/save/model/dialect_model_{dim}dims_{min_n}minn_{max_n}maxn.bin'


                train(train_set=train_set, test_set=test_set, save=save, logs=logs, lr=lr, epochs=epochs, wordNgrams=wordNgrams, dims=dim, minn=min_n, maxn=max_n)

    print('Training models with pretrained vectors...')

    
    train_set = f'./path/to/train/set'
    test_set = f'./path/to/test/set'
    

    for min_n in minns:
        for max_n in maxns:

            logs = f'./path/to/save/logs/logs_16dims_{min_n}minn_{max_n}maxn_pretrained_v2.txt'
            save = f'./path/to/save/model/test/dialect_model_16dims_{min_n}minn_{max_n}maxn_pretrained_v2.bin'


            train(train_set=train_set, test_set=test_set, save=save, logs=logs, lr=lr, epochs=epochs, wordNgrams=wordNgrams, dims=16, pretrainedVectors=pretrainedVectors, minn=min_n, maxn=max_n)


    print('Finished.')

if __name__ == '__main__':
    main()