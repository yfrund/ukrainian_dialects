import sacrebleu
from pathlib import Path
from evaluate import load, EvaluationModule

def evaluate_bleu(candidate: Path, reference: Path):
    '''
    computes the BLEU score
    '''
    with open(candidate, 'r', encoding='utf-8') as c:
        with open(reference, 'r', encoding='utf-8') as r:
            candidate_lines = c.readlines()
            reference_lines = r.readlines()

            score = sacrebleu.corpus_bleu(candidate_lines, reference_lines, lowercase=True)

            return score
            #print(reference.stem)
            #print(score)

def evaluate_comet(source: Path, candidate: Path, reference: Path, metric: EvaluationModule):
    '''
    computes the COMET score.
    returns the mean score.
    '''

    with open(source, 'r', encoding='utf-8') as s:
        with open(candidate, 'r', encoding='utf-8') as c:
            with open(reference, 'r', encoding='utf-8') as r:
                

                results = metric.compute(predictions=c.readlines(), references=r.readlines(), sources=s.readlines())
                
    
    return results['mean_score']


if __name__ == '__main__':

    
    models = []
    comet_metric = load('comet')

    #per class

    with open('evaluation_results_model_name.txt', 'w', encoding='utf-8') as eval:

        for model in models:
            print(f'Model: {model}\n')
            candidate_lines_all = []
            reference_lines_all = []
            source_lines_all = []

            #provide directories not files
            dir_candidate = Path(f'./patho/to/translations/{model}')
            dir_reference = './path/to/references'
            dir_source = './path/to/sources'

            for file in dir_candidate.iterdir():
                ref = Path(f'{dir_reference}/{file.name}')
                source = Path(f'{dir_source}/{file.name}')

                eval.write(f'Evaluation of {model}\n')
                eval.write(f'Dialect: {file.stem}\n')
                
                    
                bleu = evaluate_bleu(file, ref)
                comet = evaluate_comet(source=source, candidate=file, reference=ref, metric=comet_metric)

                eval.write(f'{bleu}\n')
                eval.write(f'Comet mean: {comet}\n')
                

            #total - concatenate all files and evaluate them
            
            candidate_files = sorted(dir_candidate.glob('*.txt')) #to ensure that the order is consistent
            reference_files = sorted(Path(dir_reference).glob('*.txt'))
            source_files = sorted(Path(dir_source).glob('*.txt'))

            for candidate in candidate_files:
                with candidate.open('r', newline='') as infile:
                    candidate_lines_all.extend(infile.readlines())

            for reference in reference_files:
                with reference.open('r', newline='') as reffile:
                    reference_lines_all.extend(reffile.readlines())

            for source in source_files:
                with source.open('r', newline='') as sourcefile:
                    source_lines_all.extend(sourcefile.readlines())

            eval.write(f'Total system evaluation\n')

            print('\n\nTotal BLEU\n\n')
            score = sacrebleu.corpus_bleu(candidate_lines_all, reference_lines_all, lowercase=True)
            eval.write(f'{score}\n')
            print(score)
            print('\n\nTotal Comet\n\n')
            
            
            results = comet_metric.compute(sources=source_lines_all, predictions=candidate_lines_all, references=reference_lines_all)
        
            eval.write(f'Total Comet mean: {results['mean_score']}\n')
            eval.flush()
            print(results['scores'])