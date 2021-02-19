#!/usr/bin/env python

"""Makes test file.

Takes the gold data and the model output, and creates a three-column TSV where
each line has a word, its gold pronunciation, and the predicted pronunciation.
"""

import argparse
import logging


def main(args: argparse.Namespace) -> None:
	# If necessary, apply default output file name
	if not args.out:
		base = args.gold[:args.gold.rfind('.')]
		ext = args.gold[args.gold.rfind('.'):]
		args.out = base + "_test" + ext
	with open(args.gold, 'r') as gf:
		with open(args.pred, 'r') as pf:
			with open(args.out, 'w') as wf:
				# Loop over lines in the files containing the gold data and 
				# the predictions. Gather each word, its actual pronunciation,
				# and its predicted pronunciation, and write them to the
				# outfile.
				for i, (g_line, p_line) in enumerate(zip(gf, pf)):
					try:
						# Separate lines into [word, pron] lists
						g_line = g_line.split('\t')
						p_line = p_line.split('\t')
						# Make sure that gold data and predictions have the
						# same words
						assert g_line[0] == p_line[0]
						word = g_line[0]
						# Note that we use `strip` to remove the newline
						g_pron = g_line[1].strip()
						p_pron = p_line[1].strip()
						line = '\t'.join([word,g_pron,p_pron]) + '\n'
						wf.write(line)
					except AssertionError:
						logging.warning(f"Gold data and predictions do not match: {g_line[0]} != {p_line[0]} (line {i})")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("gold", help="TSV with words and correct pronunciations")
	parser.add_argument("pred", help="TSV with words and predicted pronunciations")
	parser.add_argument("-o", "--out", help="file to write to")
	main(parser.parse_args())