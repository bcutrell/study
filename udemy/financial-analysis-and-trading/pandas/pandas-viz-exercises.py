import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df3 = pd.read_csv('df3')


# Scatter plot

# Create a histogram of the 'a' column.

# These plots are okay, but they don't look very polished. Use style sheets to set the style to 'ggplot' 
# and redo the histogram from above. Also figure out how to add more bins to it.*

# Create a boxplot comparing the a and b columns.

# Create a kde plot of the 'd' column

# Figure out how to increase the linewidth and make the linestyle dashed. (Note: You would usually not dash a kde plot line)

# Create an area plot of all the columns for just the rows up to 30. (hint: use .ix).

# BONUS: Can you figure out how to display the legend outside of the plot as shown below?


exit()

# Notes
import seaborn as sns # improves styles
df = pd.read_csv('df1', index_col=0)
df['A'].hist(bins=30)

df.plot.bar() # uses index as category stacked=True
df['A'].plot.hist(bins=50)
df.plot.line(x=df.index, y='B', figsize=(12,3), lw=1)

df.plot.scatter(x='A',y='B',c='C',cmap='cwarm') # colormap
# s=df['C']*100 # sets size of markers

df.plot.box()
df.plot.hexbin(x='a', y='b', gridsize=25, cmap='coolwarm')

df.plot.kde() # density

# Time Series
df = pd.read_csv(parse_dates=True, index_col='Date',)
df.plot(xlim=[start_date, end_date], ylim=[start, end])
df.loc['start_date':'end_date'][column]

fig, ax = plt.subplots()
fig.autofmt_xdate() # fix overlap
ax.plot_date(idx, array, '-')

ax.yaxis.grid(True)
ax.xaxis.grid(True)

plt.tight_layout()

ax.xaxis.set_major_locator(dates.MonthLocator()) # set tick for every month
ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n\n%b-%Y')) # set tick format use \n to add space

ax.xaxis.set_minor_locator(dates.WeekdayLocator(byweekday=0)) # byweekday=0 Monday
ax.xaxis.set_minor_formatter(dates.DateFormatter('%a'))

%matplotlib notebook # adds zooming tool
