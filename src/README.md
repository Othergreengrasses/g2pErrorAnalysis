Miscellaneous scripts
=====================

[`make_test_file.py`](make_test_file.py) creates a test file to use as input
for [`../erroranalysis.py`](../erroranalysis.py). It takes as input two 
two-column TSVs, `gold` and `pred`, both of which have a word in the first 
column and its pronunciation in the second column. It creates a three-column
TSV with the word in the first column, the pronunciation from `gold` in the
second column, and the pronunciation from `pred` in the third column. It
assumes that `gold` and `pred` have the same words in the same order (i.e.,
that their first column is the same). You can run it as follows:

`./make_test_file.py <your-gold-data> <your-predictions> -o <output-file>`