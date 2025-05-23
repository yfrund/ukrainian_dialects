 # Language Technology for Ukrainian Dialects
 
 The project explores the ability of modern language technologies to process dialect text in Ukrainian. It evaluates system performance on three tasks: language identification, dialect classification, and text standardization.

 This repository provides data, model outputs, and evaluation resources for analyzing the performance of modern LLMs on Ukrainian dialect text.

 ## Repository Structure

- `dialect_text/` contains cleaned data organized by administrative region.

     - `reference/`: Manually corrected reference files for automatic evaluation. Text was generated using:

        - GPT-3.5-turbo (via OpenAI API)
        - EuroLLM-9B-Instruct
        - Meta-LLaMA-3.1-8B-Instruct
        - Mistral-7B-Instruct-v0.1

    - `source/`: Sentences sampled from the output of the four LLMs above.

  - `translations/`: Raw outputs of the LLMs and No Language Left Behind.

  - `translations_v2/`: Outputs generated using a more restrictive prompt. Evaluation using BLEU and COMET showed no major improvements.

- `labelled_fasttext/` includes clean data formatted for fastText with dialect labels.

  - `no_dialects/`: Same data with all dialects mapped to standard Ukrainian (`uk`).

The root directory contains scripts used for data processing, model evaluation, and analysis throughout the project:

- `analyze_ngrams.py`: computes top-X most common n-grams.

- `bin2vec.py`: extracts word embedding vectors from a `.bin` fastText model.

- `clean_examples.py`: parses and cleans text extracted from HTML sources.

- `detect_language.py`: performs language ID with fastText.

- `evaluate_bleu_comet.py`: evaluates text standardization using BLEU and COMET metrics.

- `extract_text_pdf.py`: parses PDF files to extract dialect text.

- `find_label.py`: a naive script to infer true labels from filenames.

- `generate_translations.py`: generates translations using selected LLMs.
