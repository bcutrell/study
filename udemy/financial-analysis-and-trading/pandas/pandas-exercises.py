# Import pandas and read in the banklist.csv file into a dataframe called banks.
import pandas as pd
# import code code.interact(local=locals())

df = pd.read_csv('../data/banklist.csv')

# Show the head of the dataframe
df.head()


# What are the column names?
print(df.columns)

# How many States (ST) are represented in this data set?
df['ST'].nunique()

# Get a list or array of all the states in the data set.
df['ST'].unique()
 
# What are the top 5 states with the most failed banks?
df['ST'].value_counts().head(5)
df.groupby('ST').count()['Closing Date'].sort_values(ascending=False).head(5)

# What are the top 5 acquiring institutions?
df['Acquiring Institution'].value_counts().head(5)
 
# How many banks has the State Bank of Texas acquired? 
df[df['Acquiring Institution'] == 'State Bank of Texas']

# How many of them were actually in Texas?
df[df['Acquiring Institution'] == 'State Bank of Texas'][df['ST'] == 'TX']]
 
# What is the most common city in California for a bank to fail in?
df[df['ST'] == 'CA']['City'].value_counts().head(1)
 
# How many failed banks don't have the word "Bank" in their name?
df[df['Bank Name'].apply(lambda x: 'Bank' not in x)]
 
# How many bank names start with the letter 's' ?
df[df['Bank Name'].apply(lambda x: x[0].lower() == 's')]

# How many CERT values are above 20000 ?
df[df['CERT'] > 20000].count()
 
# How many bank names consist of just two words? (e.g. "First Bank" , "Bank Georgia" )
df[df['Bank Name'].apply(lambda x: len(x.split()) == 2)]
 
# Bonus: How many banks closed in the year 2008?
df[df['Closing Date'].apply(lambda x: x[-2:] == '08')]

sum(pd.to_datetime(df['Closing Date']).apply(lambda date: date.year == 2008))

# Notes
# - use inplace=True to mutate df
# - Remove column -> df.drop(column)
# - rows are the 0 axis
# - columns are the 1 axis
# - df.loc[index] to grab row by index name
# - df.iloc[index_n] to grab row by index number
# - df.loc['B', 'Y'] to grab row B column Y
# - df.set_index(list)
# - df.reset_index -> moves index to column and sets index to 0..n
# - df.xs(indexn, level=indexName) -> cross section
# - df[col].apply(function) apply custom function to each value
#   - df[col].apply(lamba x: x*2)
# - df.pivot_table(values='', index='', columns=[cols])
# - pd.to_csv('name', index=False) improves formatting
# - pd.read_html(url) # uses table table
