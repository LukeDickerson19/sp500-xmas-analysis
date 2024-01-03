import pandas as pd
pd.set_option('display.max_rows', None)
from datetime import datetime, timedelta



# read in data
filename = "sp500_daily_price_data_from_1928-01-01_to_2024-01-01.csv"
df = pd.read_csv(filename, sep='\t')
df = df.iloc[::-1].reset_index(drop=True) # reverse order, since csv orders dates latest to earliest
df['Date'] = pd.to_datetime(df['Date'])

# for each year, calculate percent changes for Grinch, next January, and next year
def find_workdays_around_christmas(year):
    christmas_date = datetime(year, 12, 25)

    # Find three workdays before Christmas
    before_christmas = []
    delta = timedelta(days=1)
    while len(before_christmas) < 3:
        christmas_date -= delta
        if christmas_date.weekday() < 5:  # Monday to Friday are considered workdays
            before_christmas.append(christmas_date)

    # Reset to the original Christmas date
    christmas_date = datetime(year, 12, 25)

    # Find three workdays after Christmas
    after_christmas = []
    while len(after_christmas) < 3:
        christmas_date += delta
        if christmas_date.weekday() < 5:
            after_christmas.append(christmas_date)

    return before_christmas[::-1], after_christmas
start_year = df.at[0, 'Date'].year
end_year = df.at[df.shape[0] - 1, 'Date'].year
df2 = pd.DataFrame(columns=[
    'year',
    'grinch_pct_chng',
    'next_jan_pct_chng',
    'next_year_pct_chng',
    'next_year'
])
for year in range(start_year, end_year):
    
    # get grinch's percent change
    before_christmas, after_christmas = find_workdays_around_christmas(year)
    if year in [1972]:
        # IndexError: single positional indexer is out-of-bounds
        continue
    grinch_start_price = df[df['Date'] == before_christmas[0]]['Close*'].iloc[0]
    grinch_end_price   = df[df['Date'] == after_christmas[-1]]['Close*'].iloc[0]
    grinch_pct_chng = (grinch_end_price - grinch_start_price) / grinch_start_price

    # get next year's january percent change
    next_year = year + 1
    next_jan_data = df[(df['Date'].dt.year == next_year) & (df['Date'].dt.month == 1)]
    next_jan_data.reset_index(inplace=True, drop=True)
    next_jan_start_price = next_jan_data.at[0, 'Close*']
    next_jan_end_price   = next_jan_data.at[next_jan_data.shape[0] - 1, 'Close*']
    next_jan_pct_chng    = (next_jan_end_price - next_jan_start_price) / next_jan_start_price

    # get next year's total percent change
    next_year_data = df[df['Date'].dt.year == next_year]
    next_year_data.reset_index(inplace=True, drop=True)
    next_year_start_price = next_year_data.at[0, 'Close*']
    next_year_end_price   = next_year_data.at[next_year_data.shape[0] - 1, 'Close*']
    next_year_pct_chng    = (next_year_end_price - next_year_start_price) / next_year_start_price

    if True: #next_year_pct_chng > 0: #grinch_pct_chng < 0:
        df2 = pd.concat([df2, pd.DataFrame({
            'year' : [year],
            'grinch_pct_chng' : ['%.2f %%' % (100 * grinch_pct_chng)],
            'next_jan_pct_chng' : ['%.2f %%' % (100 * next_jan_pct_chng)],
            'next_year_pct_chng' : ['%.2f %%' % (100 * next_year_pct_chng)],
            'next_year' : [next_year],
        }, index=[0])])

df2.reset_index(inplace=True, drop=True)
print('\nResults:')
print(df2)


