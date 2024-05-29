import pandas as pd

round123 = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/round123.csv')
round4 = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/round4.csv')

round1234 = pd.concat([round123, round4], ignore_index=True)

print(round1234)

round1234.to_csv('/Users/stevensu/Desktop/SciSketch-Newest/round1234.csv', index=False)