# Probabilistic-CFG-Parser

## Overview
The Probabilistic-CFG-Parser repository contains a Python implementation of the Cocke-Kasami-Younger (CKY) algorithm, tailored for parsing sentences using a Probabilistic Context-Free Grammar (PCFG). This implementation supports not only parsing and checking membership of strings in the defined language but also evaluates parser performance using the PARSEVAL metric against a test set.

## Features
- **Grammar Loading:** Load PCFG rules from a file.
- **Parsing:** Utilize the CKY algorithm to parse sentences into their probable tree structures.
- **Evaluation:** Evaluate parsing accuracy using precision, recall, and F-score metrics.
- **Utilities:** Includes additional scripts for tokenizing sentences and extracting tree constituents.

## Structure
- `cky.py`: The main module that contains the CKY parser class, function for in-language checking, and parse tree recovery with backpointers.
- `evaluate_parser.py`: A script to evaluate the parser's performance using a test treebank file.
- `grammar.py`: A module to load and handle the PCFG rules.
  
## Setup
To use this repository, clone it to your local machine and ensure you have Python installed.

```bash
git clone https://github.com/your-username/Probabilistic-CFG-Parser.git
cd Probabilistic-CFG-Parser

```

##Usage
1. Prepare your grammar and test files:
   Ensure your grammar file is in the proper format as expected by Pcfg class in grammar.py. Your test file should contain annotated parse trees.
2. Run the parser evaluation:
   ```bash
   python evaluate_parser.py path/to/your/grammar_file path/to/your/test_file

   ```
3. Save the README content to a file.
path = "/mnt/data/Probabilistic-CFG-Parser_README.md" with open(path, "w") as file: file.write(readme_content)


