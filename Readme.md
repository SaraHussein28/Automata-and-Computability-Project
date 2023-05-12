# CFG to PDA Converter
A context free grammar to pushdown automaton converter that operates with Context Free Grammars input.

## Use
Run main.py to enter grammar.


Grammar Input structure:
- Start state MUST be S
- All terminals and non terminals have to be of length 1
- Enter productions in format: `A->aBC|aBB`. There can be extra spaces in the input
