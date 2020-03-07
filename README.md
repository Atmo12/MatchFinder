# MatchFinder

### Custom Library for finding matches inside String or list of Strings

## Task

Building custom library to ease the task of comparing strings and finding strings inside text that may be a partial or a complete match to your goal string.

## Summary of requiements and technologies

Code developed on Python 3.7.
Makes use of the following libraries:
* re: (["Source Code"](https://github.com/python/cpython/blob/3.8/Lib/re.py "difflib Github Page"), ["docs"](https://docs.python.org/3/library/re.html "difflib docs Page"))
* difflib (["Source Code"](https://github.com/python/cpython/blob/3.8/Lib/difflib.py "difflib Github Page"), ["docs"](https://docs.python.org/3/library/difflib.html "re docs Page"))
  
## Functionality

Library allows to:
* Check for similarity between strings by a customizable ratio.
* Compare two strings and retrieve indexes for the differences between them.
* Compare multiple strings to a goal string and retrieve differences.
* Find partial/complete matches for a goal string, into other strings or a list of strings.
* Multiple find functions.
   
  
## Basic functions

* **areSimilar(String1, String2)**: Returns if the two strings are similar and the ratio of similarity. Does not take into account capitals,  spaces, accents or other special characters.
* **areSimilarAbsolute(String1, String2)**: Returns if the two strings are similar and the ratio of similarity for the strings as they are.
* **compare(String1, String2)**: Compares the given strings and returns the string with the indexes of the characters that are different.<br>
i.e: compare('Hello World', Hello Earth') --> ['Hello World',[6,7,8,9,10], 'Hello Earth', [6,7,8,9,10] (Hello *World*, Hello *Earth*).<br>
* **compareListToString(StringList, String1)**: Compares multiple Strings to a single string.<br>
i.e: compareListToString(['Hellow', 'Hallo', 'Helo'], 'Hello') --> [['Hellow', [5], 'Hello', []], ['Hallo', [1], 'Hello', [1]], ['Helo', [], 'Hello', [3]]].
