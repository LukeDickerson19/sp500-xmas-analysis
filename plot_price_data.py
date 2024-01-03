import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read in data
filename = "sp500_daily_price_data_from_1928-01-01_to_2024-01-01.csv"
df = pd.read_csv(filename, sep='\t')
df = df.iloc[::-1].reset_index(drop=True) # reverse order, since csv orders dates latest to earliest

# plot data
fig, ax = plt.subplots()
line, = ax.plot(df.index, df['Close*'])
start_date, end_date = df.at[0, 'Date'], df.at[df.shape[0] - 1, 'Date']
ax.set_title(f"SP500 Daily Price from {start_date} to {end_date}")
ax.set_ylabel('Price (in USD)')
ax.set_xlabel('Date')
margin = 0.20
plt.subplots_adjust(
    left = 0.1,
    right = 0.9,
    top = 0.9,
    bottom = 0.2) # remove default margin
ax.set_xlim(left=0, right=df.shape[0] - 1)
ax.set_ylim(bottom=0)

# update x-axis ticks w/ zoom
num_ticks = 5
def update_xticks(event):
    xlim = ax.get_xlim()
    tick_positions = np.linspace(xlim[0], xlim[1], num_ticks, dtype=int)
    ax.set_xticks(
        tick_positions,
        df['Date'].iloc[tick_positions],
        rotation=45,
        ha='right')
fig.canvas.mpl_connect('draw_event', update_xticks)
ax.callbacks.connect('xlim_changed', update_xticks)

# display price and date in top right corner
def format_coord(x, y):
    if int(x) > df.shape[0] - 1 or int(x) < 0: return ''
    d = df['Date'].iloc[int(x)]
    p = df['Close*'].iloc[int(x)]
    return f'Price=${p}   Date={d}'
ax.format_coord = format_coord

plt.show()
