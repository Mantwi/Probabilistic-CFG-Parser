import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg

### Use the following two functions to check the format of your data structures in part 3 ###
def check_table_format(table):
    """
    Return true if the backpointer table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Backpointer table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and \
          isinstance(split[0], int)  and isinstance(split[1], int):
            sys.stderr.write("Keys of the backpointer table must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of backpointer table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            bps = table[split][nt]
            if isinstance(bps, str): 
                continue 
            if not isinstance(bps, tuple):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
                return False
            if len(bps) != 2:
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
                return False
            for bp in bps: 
                if not isinstance(bp, tuple) or len(bp)!=3:
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
                    return False
                if not (isinstance(bp[0], str) and isinstance(bp[1], int) and isinstance(bp[2], int)):
                    print(bp)
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
                    return False
    return True

def check_probs_format(table):
    """
    Return true if the probability table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Probability table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write("Keys of the probability must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of probability table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            prob = table[split][nt]
            if not isinstance(prob, float):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
                return False
            if prob > 0:
                sys.stderr.write("Log probability may not be > 0.  {}\n".format(prob))
                return False
    return True



class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar): 
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def is_in_language(self,tokens):
        """
        Membership checking. Parse the input tokens and return True if 
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        # TODO, part 2
        chart = [[set() for i in range(len(tokens) + 1)] for i in range(len(tokens) + 1)]
        for i in range(len(tokens)):
            s = tokens[i]
            if (s,) in self.grammar.rhs_to_rules:
                chart[i][i + 1] = set([rule[0] for rule in self.grammar.rhs_to_rules[(s,)]])
        for l in range(2, len(tokens) + 1):
            for i in range(len(tokens) - l + 1):
                j = i + l
                for k in range(i + 1, j):
                    B_set = chart[i][k]
                    C_set = chart[k][j]
                    for B in B_set:
                        for C in C_set:
                            if (B, C) in self.grammar.rhs_to_rules:
                                chart[i][j] = chart[i][j].union(
                                    set([rule[0] for rule in self.grammar.rhs_to_rules[(B, C)]]))
        if self.grammar.startsymbol in chart[0][len(tokens)]:
            return True
        return False
       
    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
        # TODO, part 3
        table = defaultdict(dict)
        probs = defaultdict(lambda: defaultdict(int))
        for i in range(len(tokens)):
            s = tokens[i]
            if (s,) in self.grammar.rhs_to_rules:
                for rule in self.grammar.rhs_to_rules[(s,)]:
                    table[(i, i + 1)][rule[0]] = rule[1][0]
                    probs[(i, i + 1)][rule[0]] = math.log(rule[2])

        for l in range(2, len(tokens) + 1):
            for i in range(len(tokens) - l + 1):
                j = i + l
                for k in range(i + 1, j):
                    B_set = table[(i, k)]
                    C_set = table[(k, j)]
                    for B, B_rule in B_set.items():
                        for C, C_rule in C_set.items():
                            for rule in self.grammar.rhs_to_rules[(B, C)]:
                                prob = math.log(rule[2]) + probs[(i, k)][rule[1][0]] + probs[(k, j)][rule[1][1]]
                                if rule[0] not in probs[(i, j)] or prob > probs[(i, j)][rule[0]]:
                                    probs[(i, j)][rule[0]] = prob
                                    table[(i, j)][rule[0]] = ((rule[1][0], i, k), (rule[1][1], k, j))
        return table, probs


def get_tree(chart, i,j,nt): 
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    # TODO: Part 4
    if i < j and j - i == 1:
        return (nt, chart[(i, j)][nt])

    children = chart[(i, j)][nt]
    return (nt, get_tree(chart, children[0][1], children[0][2], children[0][0]),
            get_tree(chart, children[1][1], children[1][2], children[1][0]))


if __name__ == "__main__":
    
    with open('atis3.pcfg','r') as grammar_file: 
        grammar = Pcfg(grammar_file) 
        parser = CkyParser(grammar)
        toks =['flights', 'from','miami', 'to', 'cleveland','.'] 
        #print(parser.is_in_language(toks))
        #table,probs = parser.parse_with_backpointers(toks)
        #assert check_table_format(chart)
        #assert check_probs_format(probs)
        
