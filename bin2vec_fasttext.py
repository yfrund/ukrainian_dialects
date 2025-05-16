# adapted code based on https://github.com/facebookresearch/fastText/blob/main/python/doc/examples/bin_to_vec.py

from fasttext import load_model
import errno


def extract(model: str, save: str):
    '''
    extracts word embedding vectors from a bin model
    '''

    ft = load_model(model)

    words = ft.get_words()

    
    with open(save, 'w') as f:

        f.write(str(len(words)) + ' ' + str(ft.get_dimension()) + '\n')

        for w in words:

            v = ft.get_word_vector(w)
            vstr = ""
            for vi in v:
                vstr += " " + str(vi)
            try:
                f.write(w + vstr + '\n')
                

            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass

def main():
    model_path = './path/to/model'
    save = './path/to/save/vectors'

    extract(model_path, save)

if __name__ == '__main__':
    main()