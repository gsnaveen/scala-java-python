import pandas as pd

df = pd.read_csv('./data/cluster_data', header=None, sep="\t")

pd.options.display.max_columns = 50
pd.options.display.max_rows = 999
pd.set_option('expand_frame_repr', False)
print(df.shape)
print(df.columns)
print(df.head(10))
