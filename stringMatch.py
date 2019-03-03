from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
import jellyfish
import dedupe
# pip install fuzzywuzzy[speedup]
# python-Levenshtein
# import fuzzy
import pandas as pd
""" input example file
str counts
IN  2
BEARING 3
ROMAN   4
ROM    2
"""

fileName = "stringMatch"
df = pd.read_csv("./data/" + fileName +".txt",sep='\t',header=0)
df["strlen"] = df["str"].str.len()
df = df[df["strlen"] > 1]
dftopList = df[df["counts"] > 4] # If you don't have a count of the words then you can comment this line
dftopListWords = dftopList["str"].tolist()
words = df["str"].tolist()
i = 0
matchAnalysis = []
for word in dftopListWords:
    for matchWord,matchval in process.extract(word, words,limit=20):
        if word != matchWord:
            levnDist = jellyfish.levenshtein_distance(word, matchWord)
            seqMatch = round(SequenceMatcher(None, word, matchWord).ratio() * 100)
            # fuzz.token_sort_ratio
            matchAnalysis.append([word,matchWord, matchval,levnDist,seqMatch,len(word)])

    # if i == 2:
    #     break
    # else:
    #     i += 1
else:
    dfMatch = pd.DataFrame.from_records(matchAnalysis,
                                         columns=["word", "matchedWord", "matched", "levnDist", "seqMatch","strLen"])

    dfMatch.to_csv("./data/" + fileName + "out.txt",header=True,sep='\t',index=False)
# print(df.columns)
# print(df.dtypes)
# print(df.head(10))
