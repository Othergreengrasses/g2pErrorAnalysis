"""Error Analysis tool for G2P.

This script assumes 2 input files. a) Covering Grammer b) Test output. 
CG file  : Each line contain graphime and their corresponding pronunciation seperated by a tab
Test File: contains three attributes in each line seperated by a tab. The attributes are - orthography, expected pronunciation, and hypothesized pronunciation."""

__author__ = "Arundhati Sengupta"

from pynini import *
import argparse

def main(args: argparse.Namespace):
    bn_fst = string_file(args.cg_path).closure()
    f = open(args.test_path,'r')
    lines = f.readlines()
    rulematch_predMatch = 0
    rulematch_predNotMatch = 0
    notRulematch_predMatch = 0
    notRulematch_predNotMatch = 0
    for line in lines:
        parts = line.split('\t')
        ben = parts[0].strip()
        act = parts[1].replace(' ','').replace('.','').strip()
        predPron = parts[2].replace(' ','').replace('.','').strip()
         
        lattice = (ben @ bn_fst @ predPron).project(True)
        
        if lattice.start() == NO_STATE_ID:
            if (act == predPron):
                notRulematch_predMatch += 1
                
            else:
                notRulematch_predNotMatch += 1            
            
        else:
            if (act == predPron):
                rulematch_predMatch += 1
            else:
                rulematch_predNotMatch += 1

    total_records = len(lines)
    f.close()
    
    print ('Total Number of Records', total_records)

    printtable(round(rulematch_predNotMatch / total_records, 4),round(rulematch_predMatch / total_records, 4),
        round (notRulematch_predMatch / total_records, 4),round(notRulematch_predNotMatch / total_records, 4))


def printtable(ruleMpredNM, ruleMpredM,ruleNMpredM,ruleNMpredNM):
    ruleMpredNM = '{:.4f}'.format(ruleMpredNM)
    ruleMpredM = '{:.4f}'.format(ruleMpredM)
    ruleNMpredM = '{:.4f}'.format(ruleNMpredM)
    ruleNMpredNM = '{:.4f}'.format(ruleNMpredNM)

    print('                                            ')
    print('               | CG Match  |   CG Not Match |')
    print('---------------|-----------+----------------|')
    print('Pron Match     | ',ruleMpredM,'  |     ',ruleNMpredM,'   |')
    print('Pron Not Match | ',ruleMpredNM,'  |     ',ruleNMpredNM,'   |')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cg_path", required=True, help="path to file of covering grammar which is a tsv file. Each line contain graphime and their corresponding pronunciation seperated by a tab"
    )
    parser.add_argument(
        "--test_path", required=True, help="path to test tsv file which contains three attributes in each line seperated by a tab. The attributes are - orthography, expected pronunciation, and hypothesized pronunciation."
    )
    main(parser.parse_args())