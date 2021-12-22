from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words,stopwords
from nltk.util import everygrams,ngrams
import re

wordList = words.words()
stop_words = set(stopwords.words('english'))

baseWord = 'hourstofollowupexcludeweekends'
listBaseWord = list(baseWord)
lengthOfWord = len(listBaseWord)
validWords = []
for wordin in everygrams(listBaseWord):
    worlinLen = len(wordin)
    word =  ''.join(wordin)
    # > 1 len and exclude stop keywords
    if worlinLen > 1 and word not in stop_words:
         if ''.join(word) in wordList :
              validWords.append(word)
         else:
              pass


print(validWords)
validWordsTwo = []
for index,vwords in enumerate(validWords):
    found = False
    for val in validWords[index +1:]:
         if re.search(vwords,val):
              break
    else:
         if not found:
              validWordsTwo.append(vwords)


 print(validWordsTwo)
