from collections import defaultdict
from pathlib import Path
from unidecode import unidecode
import pandas as pd
import string
import nltk



def compute_ngrams(ngram_order: int, top_count: int, file: Path) -> tuple:
    '''
    computes ngram counts in a given file and returns the most frequent ngrams;
    params:
    ngram_order = size of ngrams, e.g. bigram or trigram
    top_count = how many most frequent ngrams the function should return
    file = the data to compute ngrams
    '''
    ngrams = defaultdict(int)

    if '_' in file.stem: #language files
        language_code = file.stem.split('_')[0]
    else:
        language_code = unidecode(file.stem) #dialect files

    with open (file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:

            try:
                sent = line.split('\t')[1].translate(str.maketrans('', '', string.punctuation)).strip()
                for i in range(len(sent)):
                    ngram = sent[i:i+ngram_order]

                    if len(ngram) == ngram_order:
                        ngrams[ngram] +=1
            except IndexError:

                for i in range(len(line)):
                    ngram = line.translate(str.maketrans('', '', string.punctuation)).strip()[i:i+ngram_order]

                    if len(ngram) == ngram_order:
                        ngrams[ngram] += 1

    top = sorted(ngrams, key=ngrams.get, reverse=True)[:top_count]

    #return f'Language: {language_code}, ngram order: {ngram_order}, top-{top_count} ngrams: {top}\n'
    return language_code, ngram_order, top

def main():


    ngram_orders = [2,3,4,5]   
    
    files_languages = Path('./leipzig_corpora')
    files_dialects = Path('./dialect_text')


    data_ngrams = []


    for ngram in ngram_orders:
        for file in files_languages.iterdir():
            if file.is_file():

                print(f'\nProcessing {ngram}-grams in {file}')
                #print(compute_ngrams(ngram, 10, file))
                data_ngrams.append(compute_ngrams(ngram, 20, file))

        for file in files_dialects.iterdir():
            if file.is_file():

                print(f'\nProcessing {ngram}-grams in {file}')
                #print(compute_ngrams(ngram, 10, file))
                data_ngrams.append(compute_ngrams(ngram, 20, file))

    
    df_ngrams = pd.DataFrame(data_ngrams, columns = ['Dialect or Language', 'N-gram order', 'Top N-grams'])

    df_ngrams.to_csv('ngrams_table.csv', index=False, encoding='utf-8-sig') #utf-8-sig ensures Windows apps like Excel correctly recognize the encoding
    


    print('Done.')
    
if __name__ == '__main__':
    main()
