# wordle-calculator
Script to identify sets of 5 wordle words that have unique characters, totalling 25 unique characters in five 5-letter words. Uses the wordle dictionary CSW 19.

## Running
Just clone the repo and run with

```
python wordle.py
```

## Output
Ran for several hours on my computer and below are all such 5-word combinations that have only unique letters.

```
Number of groupings tried:  169439287
['bemix', 'clunk', 'grypt', 'vozhd', 'waqfs']   20687
['bling', 'jumpy', 'treck', 'vozhd', 'waqfs']   20934
['blunk', 'cimex', 'grypt', 'vozhd', 'waqfs']   21889
['brick', 'glent', 'jumpy', 'vozhd', 'waqfs']   21341
['brung', 'cylix', 'kempt', 'vozhd', 'waqfs']   20516
['brung', 'kempt', 'vozhd', 'waqfs', 'xylic']   19667
['chunk', 'fjord', 'gymps', 'vibex', 'waltz']   20933
['clipt', 'jumby', 'kreng', 'vozhd', 'waqfs']   20808
['fjord', 'gucks', 'nymph', 'vibex', 'waltz']   20528
['glent', 'jumby', 'prick', 'vozhd', 'waqfs']   21116
['jumby', 'pling', 'treck', 'vozhd', 'waqfs']   20709
```

## Code optimizations and approach
As this problem is NP-complete, we have to do some shortcuts as to not evaluate all roughly `3e18` possible combinations of 5-letter words in the dictionary.

Because we're looking for 5-letter words that have solely unique letters, we can start by removing all words from the dictionary that have repeated letters, reducing the size of the dictionary to the 8k range.

We consider all remaining words in alphabetical order for the first word in the set. For a given first word (say, `bundt`), we consider all possible second words in the set that have no shared letters with `bundt` and occur later in alphabetical order than `bundt` in the dictionary. For the third word, we consider words that share no letters with the first two words and occur after the second word in alphabetical order, and so on. This brings us down to only 1.6e8 samples to try.

If we're not interested in completeness, we can also consider removing all words that have at least two vowels. This lowers the size of the dictionary to around 2k words, allowing the script to spit out solutions in only a few minutes, working on the assumption that if we consider words that have too many vowels, then there will be no vowels left for the later words. Admittedly, this dictionary contains words like `crwth` that have no vowels, so this methodology isn't perfect and should only be used if we're not interested in getting all allowed 5-word combinations.
