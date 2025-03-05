import json
from extract_text_pdf import normalize
from bs4 import BeautifulSoup



def clean_save():
    
    with open('examples.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for dialect in data:
            with open(f'dialect_text/{dialect}.txt', 'a', encoding='utf-8') as f:

                for example in data[dialect]['examples']:

                    try:
                        
                        soup = BeautifulSoup(example, 'html.parser')
                        clean = soup.get_text(separator=' ', strip=True).replace('\\', '')

                        normalized = normalize(clean)

                        if normalized:
                            f.write(normalized+'\n')
                            
                            

                    except AttributeError as e:
                        print(f'Exception: {e}\n')

def main():
    print('Start processing examples...')
    clean_save()
    print('Finished \u2713')


if __name__ == '__main__':
    main()
    
