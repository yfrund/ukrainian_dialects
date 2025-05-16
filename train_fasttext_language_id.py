import fasttext
from collections import defaultdict
from pathlib import Path
from detect_language import evaluate_predict



def train(train_set: str, test_set: str, save: str, logs: str, lr: list, epochs: list, wordNgrams: list, dims: int, pretrainedVectors: str = None):
    '''
    performs hyperparameter tuning and saves the model with the highest f-score
    params:
        train_set, test_set, save, logs, pretrainedVectors: paths
            save: to save the model

        lr, epochs, wordNgrams, dims: lists
            lr: learning rate
            wordNgrams: ngram size to include as additional information, typically 1-4
            dims: vector dimensionality; equals vector dimensionality of pretrainedVectors if pretrainedVectors != None

        pretrainedVectors: path to the .vec file
        
    '''

    
    max_fscore = 0
    

    for rate in lr:
        for epoch_num in epochs:

            for ngram_val in wordNgrams:

                if pretrainedVectors:

                    model = fasttext.train_supervised(input=train_set, lr=rate, epoch=epoch_num, wordNgrams=ngram_val, pretrainedVectors=pretrainedVectors, dim=dims)

                    
                    result = model.test(test_set)
                    precision, recall =  result[1], result[2]
                    f_score = 2*(precision*recall/(precision+recall))

                    if f_score > max_fscore:
                        max_fscore = f_score

                        message = f'Saving best model with f-score {f_score}, trained for {epoch_num} epochs with LR {rate}, {dims} vector dimensions and {ngram_val}-grams.\n'
                        print(message)
                        with open(logs, 'a', encoding='utf-8') as f:
                            f.write(message)
                        model.save_model(save)


                else:

                    model = fasttext.train_supervised(input=train_set, lr=rate, epoch=epoch_num, wordNgrams=ngram_val, dim=dims)

                    
                    result = model.test(test_set)
                    precision, recall =  result[1], result[2]
                    f_score = 2*(precision*recall/(precision+recall))

                    if f_score > max_fscore:
                        max_fscore = f_score

                        message = f'Saving best model with f-score {f_score}, trained for {epoch_num} epochs with LR {rate}, {dims} vector dimensions and {ngram_val}-grams.\n'
                        print(message)
                        with open(logs, 'a', encoding='utf-8') as f:
                            f.write(message)
                        model.save_model(save)

            



def main():

    print('Start training models...')
   


    print('Finished.')

if __name__ == '__main__':
    main()