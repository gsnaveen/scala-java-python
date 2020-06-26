import re

"""
input is a text file output of email
"""

file = 'email1'
outset = set()
with open('./data/email/' + file +'.txt') as f:
    data = f.readlines()
    for row in data:
        for word in row.lower().split(' '):
            if re.search('@',word) and re.search('\.org|\.net|\.com|\..{2}.*',word):

                 outset.add(re.sub('<|>|\'|`|;|,|\n','',word))


print('Total email address : ',len(outset))
print('+++++++++++++++++++++')
for email in outset:
    print(email)
