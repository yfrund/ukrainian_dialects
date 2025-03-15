import unicodedata
import pymupdf
import re


oblasts = ("АР Крим", 
           "Вінницька", 
           "Волинська", 
           "Дніпропетровська", 
           "Донецька", 
           "Житомирська", 
           "Закарпатська", 
           "Запорізька", 
           "Івано-Франківська", 
           "Київська", 
           "Кіровоградська", 
           "Луганська", 
           "Львівська", 
           "Миколаївська", 
           "Одеська", 
           "Полтавська",
           "Рівненська", 
           "Сумська", 
           "Тернопільська", 
           "Харківська", 
           "Херсонська", 
           "Хмельницька", 
           "Черкаська", 
           "Чернівецька", 
           "Чернігівська")

                                
def process_borshch(start_page, end_page, doc):
    '''Processes texts about borshch.
    Automatically assigns text chunks to correct dialects'''
    document = pymupdf.open(doc)

    text = ''
    dialect = None

    for page_num in range(start_page, end_page):

        for item in document[page_num].get_text('dict')['blocks']:

            try:
                for l in item['lines']:

                    for s in l['spans']:
                        flags = flags_decomposer(s['flags'])

                        if 'bold' in flags:

                            for o in oblasts:
                                if o in s['text']:
                            
                                    if dialect:

                                        with open(f'dialect_text\{dialect}.txt', 'a', encoding='utf-8') as f:
                                            

                                            for sent in text.split('//'):
                                                if sent.strip():
                                                    
                                                    f.write(sent.strip()+'\n')

                                    dialect = o
                                    text = ''

                                    break

                        elif 'italic' not in flags and 'superscript' not in flags and s['size'] != 9.0: #filtering out footnotes based on smaller size; superscript = diacritics that are also valid letters
                            

                            text = text + normalize(s['text'])

            except TypeError as e:

                #print(f'Exception due to empty page: {e}')
                continue
    #save the last chunk
  
    with open(f'dialect_text\{dialect}.txt', 'a', encoding='utf-8') as f:
        for sent in text.split('//'):
            if sent.strip():
                f.write(sent.strip()+'\n')


        

def process_text(start_page, end_page, dialect_name, doc):
    '''Processes all other texts.
    Assigns data to specified dialects'''
    document = pymupdf.open(doc)

    text = ''
   

    #speaker_pattern = r'\w+\s+\w+(?:\w+)?, \d{4} '#to exclude text that gives information about speakers - each line contains: 'Last_name First_name Parental, XXXX', where XXXX = birth year

    for page_num in range(start_page, end_page):

        
        for item in document[page_num].get_text('dict')['blocks']:

            for l in item['lines']:
                
                if any('|' in span['text'] for span in l['spans']): #make sure it's speaker's text, not metadata - speaker text is marked for stress
                    
                        
                    for s in l['spans']:
                        flags = flags_decomposer(s['flags'])
                            

                        try:
                            #if 'italic' not in flags and 'bold' not in flags and s['size'] == 13.918607711791992 and 'інформант' not in s['text'].lower():

                                #match = re.search(speaker_pattern, s['text'])
                                
                                
                                #if not match:
                                    #text = text + normalize(s['text'])
                            if 'bold' not in flags: #there is some relevant italicized text in speaker text, e.g. quotes from songs
                                text = text + normalize(s['text'])
                            


                        except TypeError: #skip empty pages
                            
                            #print(f'exception: {e}')
                            continue

    with open(f'dialect_text\{dialect_name}.txt', 'a', encoding='utf-8') as f:
        for sent in text.split('//'):
            if sent.strip():
                f.write(sent.strip()+'\n')
                
                    
def normalize(item):

    if isinstance(item, str):
        
        normalized = item.replace('˙', '')
        normalized = keep_char(normalized)
        

        normalized = ''.join(char for char in unicodedata.normalize('NFKC', normalized) if unicodedata.category(char) not in ('Mn', 'Sm', 'Sk', 'Lm', 'Pf') and char not in (':', '′', '·', '\'') and not unicodedata.combining(char)) #add 'Lm' to remove the stress marks, 'Pf' to remove softening mark, 'Po' removes colons but also slashes

        
        
        normalized = normalized.replace(' / ', ',')
        normalized = normalized.replace('\n', '')
        
        

        #remove metadata in [] and (), including unbalanced brackets
        if any(char in normalized for char in '[]()'):
            
            
            normalized = re.sub(r'\[.*?\]', '', normalized)
            normalized = re.sub(r'\(.*?\)', '', normalized)
            

            normalized = normalized.split('[')[0] if '[' in normalized else normalized
            normalized = normalized.split('(')[0] if '(' in normalized else normalized
            normalized = normalized.split(']')[1] if ']' in normalized else normalized
            normalized = normalized.split(')')[1] if ')' in normalized else normalized
          
        
        
        try:
            #filter out integers stored as strings - page numbers
            int(normalized)
            #return ''

        except ValueError:
            
                return normalized
    
def flags_decomposer(flags):

    """Make font flags human readable.
    Function from official docs at https://pymupdf.readthedocs.io/en/latest/recipes-text.html"""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)

def get_flags(item):

    for l in item['lines']:
        for s in l['spans']:
            flags = flags_decomposer(s['flags'])

    return flags

def keep_char(text):
    '''keep the й'''
    
    decomposed = unicodedata.normalize('NFKD', text)

    clean = ''
    for i in range(len(decomposed)):

        try:

            if decomposed[i].lower() == 'и' and decomposed[i+1].lower() == '\u0306': #breve
                clean = clean + decomposed[i] + decomposed[i+1]
            else:
                if unicodedata.category(decomposed[i]) not in ('Mn', 'Sm', 'Sk', 'Lm', 'Pf') and decomposed[i] not in (':'):

                    clean = clean + decomposed[i]
                   
        except IndexError:
            clean = clean + decomposed[i]
 
    return clean


def main():
    print(f'Starting the extraction...')

    process_borshch(20, 308, 'G:\My Drive\Bachelor\Словники\Тексти\Borshсh.pdf')
    print('Processed "Borshch" \u2713')

    process_text(34, 121, 'Черкаська', 'G:\My Drive\Bachelor\Словники\Тексти\Hovirky_Cherkaschyny_zbirky_dialektnyh_tekstiv.pdf')
    print('Processed Cherkasy region \u2713')

    process_text(6, 304, 'Луганська', 'G:\My Drive\Bachelor\Словники\Тексти\Hovirky_Skhidnoi_Slobozhanschyny_zbirnyk_dialektnykh_tekstiv.pdf')
    print('Processed Luhansk region \u2713')

    process_text(24, 154, 'Полтавська', 'G:\My Drive\Bachelor\Словники\Тексти\Hovirky_Zahidnoi_Poltavschyny_zbirnyk_dialektnyh_tekstiv.pdf')
    print('Processed Poltava region \u2713')

    process_text(20, 339, 'Хмельницька', 'G:\My Drive\Bachelor\Словники\Тексти\Volynski-hovirky-Khmelnychchyny-zbirnyk-dialektnykh-tekstiv.pdf')
    print('Processed Khmelnytsk region \u2713')

    print(f'Finished.')

if __name__ == '__main__':
    main()
