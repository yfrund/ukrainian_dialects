from pathlib import Path
import requests
import os


def lm_generate(api: str, model: str, dialect_name: str, instruction: str, sent: str,  api_key:str=None):
    '''
    Generates translations. Suitable to use with a local server (e.g., LM Studio) and OpenAI API.
    '''
        
    max_tokens = len(sent)*3 #set max length of output
    
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': instruction},
            {'role': 'user', 'content': sent.strip()}
        ],
        #'max_tokens': max_tokens,
        'temperature': 0
    }

    if 'eurollm' in model: #add a model if it enters an infinite generation loop
        payload['max_tokens'] = max_tokens

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    } if 'gpt' in model else None

    try:

        response = session.post(api, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        translation = data['choices'][0]['message']['content'].replace('\n', '') #remove new lines if the model generates them - crucial for alignment
        with open(f'path/to/save/translations/{model}/{dialect_name}.txt', 'a', encoding='utf-8') as f: 
            f.write(f'{translation}\n')
            f.flush() #save to disk straight away
    
    except Exception as e:
        print(f'Failed to translate ***{sent.strip()}***: {e}')




if __name__ == '__main__':


    #example api for completion
    API_URL = 'http://192.168.178.31:1234/v1/chat/completions'  
    OPENAI_API = 'https://api.openai.com/v1/chat/completions'
    
    #get token - need to set an environment variable first
    openai_key = os.getenv('OPENAI_API_KEY')

    
    #example model names
    llama = 'meta-llama-3.1-8b-instruct'
    mistral = 'mistral-7b-instruct-v0.1'
    eurollm = 'eurollm-9b-instruct'
    gpt3_5_turbo = 'gpt-3.5-turbo'

    instruction_en = 'Your instruction goes here.'
    session = requests.Session()

    dir = Path('./dialect_text/source')
    
    for file in dir.iterdir():
        if file.is_file():

            with open(file, 'r', encoding='utf-8') as f:
                dialect_name = file.stem
            
                for sent in f.readlines():
                    
                    #use this when running a local server
                    lm_generate(API_URL, model_name, dialect_name, instruction_en, sent)

                    #use this when using openai api
                    lm_generate(OPENAI_API, gpt3_5_turbo, dialect_name, instruction_en, sent, api_key=openai_key)

