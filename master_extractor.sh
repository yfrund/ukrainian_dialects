#!/bin/bash

PDF_EXTRACTOR='extract_text_pdf.py'
CLEAN_EXAMPLES='clean_examples.py'
OUTPUT_DIR='dialect_text'

mkdir -p $OUTPUT_DIR

echo 'Running the scripts.'

/c/Users/Yuliia/miniconda3/python $PDF_EXTRACTOR
/c/Users/Yuliia/miniconda3/python $CLEAN_EXAMPLES