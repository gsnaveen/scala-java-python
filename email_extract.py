import re
from collections import defaultdict
"""
input is a text file output of email
"""

file = 'email1'
outset = defaultdict(int)
with open('./data/email/' + file +'.txt') as f:
    data = f.readlines()
    for row in data:
        for word in row.lower().split(' '):
            if re.search('@',word) and re.search('\.org|\.net|\.com|\..{2}.*',word):
                 # outset.add(re.sub('<|>|\'|`|;|,|\n','',word))
                email = re.sub('<|>|\'|`|;|,|\n', '', word)
                outset[email] += 1


print('Total email address : ',len(outset))
outsetSorted = {}
for key in  sorted(outset, key=outset.get, reverse=True):
    outsetSorted[key]= outset[key]
print(outsetSorted)
print('+++++++++++++++++++++')
for email in outsetSorted:
    print(email)
