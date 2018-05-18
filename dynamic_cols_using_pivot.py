import pandas as pd
myData = [['myurl.com/','q1',10], ['myurl.com/','q2',15],['myurl.com/','q3',20],['myurl.com/','q3',20]]
df = pd.DataFrame(myData,columns=['URL','toPiv','value'])
df = df.drop_duplicates()
df.pivot(index='URL', columns='toPiv', values='value').reset_index()
