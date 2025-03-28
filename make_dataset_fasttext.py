import os
from unidecode import unidecode


def make_dataset(file):
    '''prepare all sentences in the same format: landialect_label \tab sentence'''

    with open(file, 'r', encoding='utf-8') as i:
        sents = i.readlines()
        with open(f'./dialect_text/labelled_fasttext/{unidecode(os.path.splitext(os.path.basename(file))[0]).lower()}.txt', 'a', encoding='utf-8') as o:
            for sentence in sents:
                #dialect code = 5 first letters of the transliterated dialect name
                #dialect_code = unidecode(os.path.splitext(os.path.basename(file))[0]).lower()
                

                o.write(f'__label__uk\t{sentence}')


def main():

    for file in os.listdir('./dialect_text'):
        filepath = os.path.join('./dialect_text', file)
        if os.path.isfile(filepath):
            make_dataset(filepath)


if __name__ == '__main__':
    main()