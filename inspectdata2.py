# import pandas as pd

# df = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/abstracts_data_missing_2.csv', )

# round5 = df[df['Link_to_img'].notnull()]

# missing  = df[df['Link_to_img'].isnull()]

# round5.to_csv('/Users/stevensu/Desktop/SciSketch-Newest/round8.csv', index=False)
# missing.to_csv('/Users/stevensu/Desktop/SciSketch-Newest/abstracts_data_missing_2.csv', index=False)

import pandas as pd

df1 = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/round1234567.csv')
df2 = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/round8.csv')

df = pd.concat([df1, df2])

df.to_csv('/Users/stevensu/Desktop/SciSketch-Newest/round12345678.csv', index=False)