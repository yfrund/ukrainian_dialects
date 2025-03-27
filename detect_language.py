#from langdetect import detect, lang_detect_exception
import os
import fasttext
import subprocess
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


from collections import defaultdict
from pathlib import Path
import json

def detect_lang(file, model, results_folder):

    results = defaultdict(lambda: defaultdict(int))
    dialect = Path(file).stem
    

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        results[dialect]['total'] = len(lines)

        for line in lines:
        

            try:

                label, _ = model.predict(line.strip('\n'))
                label = label[0].replace('__label__', '')
                results[dialect][label] += 1

            except lang_detect_exception.LangDetectException as e:
                print(f'Exception: {e}\nLine: {line}')
                results[dialect]['undetected'] += 1
            
    with open(f'{results_folder}/{dialect}.json', 'w', encoding='utf-8') as o:
        json.dump(results, o, ensure_ascii=False, indent=4)



def evaluate_predict(model, test_file, predictions, save):


    dialect = test_file.stem
    result_eval = model.test(str(test_file))
    f_score = 2*(result_eval[1]*result_eval[2] / (result_eval[1] + result_eval[2]))

    #print(f'\nEvaluated dialect: {dialect}.\nNumber of datapoints: {result_eval[0]}\n\tPrecision: {result_eval[1]}\n\tRecall: {result_eval[2]}\n\tF-score: {f_score}.')
    
    
    #with open (save, 'a', encoding='utf-8') as o:
    #    o.write(f'\nEvaluated dialect: {dialect}.\nNumber of datapoints: {result_eval[0]}\n\tPrecision: {result_eval[1]}\n\tRecall: {result_eval[2]}\n\tF-score: {f_score}.')

    with open(test_file, 'r', encoding='utf-8') as f:
        
        predictions[dialect]['total'] = result_eval[0]

        for line in f.readlines():

            try: 

                label, _ = model.predict(line.strip('\n'))
                label = label[0].replace('__label__', '')
                predictions[dialect][label] +=1
            except Exception as e:
                print(f'Encountered an exception while processing {dialect} dialect. Exception: {e}')


def main():
    folder = Path(r'/mnt/c/Users/Administrator/Desktop/Bachelor/dialect_text/labelled_fasttext')
    #model_path = hf_hub_download(repo_id='facebook/fasttext-language-identification', filename='model.bin')
    model = fasttext.load_model('./fasttext_model/lid.176.bin')
    predictions = defaultdict(lambda: defaultdict(int))
    for file in folder.iterdir():
        if file.is_file():

            #detect_lang(file, model, r'/mnt/c/Users/Administrator/Desktop/Bachelor/language_id/fasttext')
            evaluate_predict(model, file, predictions, 'language_id/fasttext.txt')
    
    #make sure no label is missed in hardcoded predicted_labels
    preds = set()
    for dial in predictions:
        for pred in predictions[dial]:
            if pred != 'total':
                preds.add(pred)
    true_labels = sorted(predictions.keys())
    #predicted_labels = set(label for counts in predictions.values() for label in counts if label != 'total')
    predicted_labels = ['uk', 
                        'ru', 'be', 'rue', 
                        'bg', 'mk', 'sr', 'sh', 
                        'tt', 'sah', 'ky', 'uz', 'kk', 'ba', 'krc', 'az', 'cv',
                        'mhr', 'mrj', 
                        'mt', 
                        'ce', 'lez',
                        'tg', 
                        'mn', 
                        'lv', 
                        'pl', 
                        'ko', 
                        'de']

    if set(predicted_labels) == preds:
    
    
        confusion_matrix = np.zeros((len(predicted_labels), len(true_labels)), dtype=int)

        dialect_to_idx = {dialect: i for i, dialect in enumerate(true_labels)}
        pred_label_to_idx = {label: i for i, label in enumerate(predicted_labels)}

        for true_label, counts in predictions.items():
            true_idx = dialect_to_idx[true_label]

            for pred_label, count in counts.items():
                if pred_label != 'total':
                    pred_idx = pred_label_to_idx[pred_label]
                    confusion_matrix[pred_idx, true_idx] = count

        df_conf_matr = pd.DataFrame(confusion_matrix, index=predicted_labels, columns=true_labels)
    
        #heatmap with all dialects
        plt.figure(figsize=(10,8))
        sns.heatmap(df_conf_matr, annot=True, fmt='d', cmap='Blues', xticklabels=true_labels, yticklabels=predicted_labels)
        plt.xlabel('True Labels - Dialects')
        plt.ylabel('Predicted Labels - Languages')
        plt.savefig('visualisations/lang_id_heatmap2.png', dpi=300, bbox_inches='tight')
        plt.clf() #clear the figure
        plt.close() #close it
    else:
        print(f'predicted_labels != actual predictions!')
        
if __name__ == '__main__':
    main()
      
