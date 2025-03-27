from collections import defaultdict
from pathlib import Path



def compute_ngrams(ngram_order, top_count, file):
    '''
    computes ngram counts in a given file and returns the most frequent ngrams;
    params:
    ngram_order = size of ngrams, e.g. bigram or trigram
    top_count = how many most frequent ngrams the function should return
    file = the data to compute ngrams
    '''
    ngrams = defaultdict(int)
    language_code = file.stem[:3]

    with open (file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:

            sent = line.split('\t')[1]
            for i in range(len(sent)):
                ngram = sent[i:i+ngram_order]

                if len(ngram) == ngram_order:
                    ngrams[ngram] +=1

    top = sorted(ngrams, key=ngrams.get, reverse=True)[:top_count]

    return f'Language: {language_code}, ngram order: {ngram_order}, top-{top_count} ngrams: {top}\n'

def main():
    
    files = Path('./leipzig_corpora')
    for file in files.iterdir():
        if file.is_file():
            
            print('Processing bigrams...')
            print(compute_ngrams(2, 10, file))
            
            print('Processing trigrams...')
            print(compute_ngrams(3, 10, file))

            print('Processing 4-grams...')
            print(compute_ngrams(4, 10, file))
            
            print('Processing 5-grams...')
            print(compute_ngrams(5, 10, file))

    
    print('Done.')
    
if __name__ == '__main__':
    main()

#TODO: remove punctuation?