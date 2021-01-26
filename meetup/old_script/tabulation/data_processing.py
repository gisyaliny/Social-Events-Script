import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import timedelta
import math


def drop_na(df):
    drop_lst = [colnam for colnam in df.columns if ('Unnamed' in colnam)]
    df.drop(drop_lst, axis=1, inplace=True)
    df = df.dropna()
    return df


def general_plot(df,outpath):
    df1 = df.replace(['Arts', 'Beliefs', 'Book Clubs', 'Career & Business', 'Dance',
           'Family', 'Fashion & Beauty', 'Film', 'Food & Drink',
           'Health & Wellness', 'Hobbies & Crafts', 'Language & Culture',
           'Learning', 'LGBTQ', 'Movements', 'Music', 'Outdoors & Adventure',
           'Pets', 'Photography', 'Sci-Fi & Games', 'Social',
           'Sports & Fitness', 'Tech', 'Writing'],['At','Bf','Bk','C&B','Dc','Fy','F&B','Fm','F&D','H&W','H&C','L&C',
                                                  'Le','LG','Mt','Mu','O&A','Pt','Py','S&C','Sl','S&F','T','Wt'])
    plt.figure(figsize=(20, 10))
    plt.bar(df1['Category'].value_counts().index,df1['Category'].value_counts())
    plt.title('Events Count\n', fontsize=20)
    plt.xlabel('Category', fontsize=18)
    plt.ylabel('Count', fontsize=18)
    plt.savefig(outpath)


def times_category_plot(df,times_outpath,category_outpath):
    events_frenqucy_lst = df['Name'].value_counts()
    events_frenqucy_lst.head()
    plt.figure(figsize=(12, 10))
    plt.bar(events_frenqucy_lst.value_counts().sort_index().index,events_frenqucy_lst.value_counts().sort_index())
    plt.title('Events happend times\n', fontsize=20)
    plt.xlabel('Times', fontsize=18)
    plt.ylabel('frequncy', fontsize=18)
    plt.savefig(times_outpath)
    df['Date'] = pd.to_datetime(df['Date'])
    start_time = df['Date'].min()
    end_time = df['Date'].max()
    date_list = [start_time + timedelta(days=x) for x in range(0, (end_time - start_time).days, 30)]
    oneTime_events = events_frenqucy_lst[events_frenqucy_lst == 1].index
    oneTime_events = list(set(oneTime_events))
    df1 = df[~df.Name.isin(oneTime_events)]
    df1['Name']
    weekly_events = []
    i = 0
    while (i < len(date_list) - 1):
        df_slice = df1[(df1.Date >= date_list[i]) & (df1.Date < date_list[i + 1])]
        i += 1
        events_frenqucy_lst2 = df_slice['Name'].value_counts()
        weekly_events2 = events_frenqucy_lst2[events_frenqucy_lst >= 2].index
        weekly_events.extend(weekly_events2)
    weekly_events = list(set(weekly_events))
    df['Types'] = 'Monthly Events'
    df.loc[df['Name'].isin(oneTime_events), 'Types'] = 'One Time events'
    df.loc[df['Name'].isin(weekly_events), 'Types'] = 'Weekly events'
    plt.figure(figsize=(12, 10))
    plt.bar(df['Types'].value_counts().index,df['Types'].value_counts())
    plt.title('Events Count\n', fontsize=20)
    plt.xlabel('Category', fontsize=18)
    plt.ylabel('Count', fontsize=18)
    plt.savefig(category_outpath)
    return df

def set_interval(x):
    x = str(x)
    if (('AM' in x) & (x.count(':00'))):
        timeRange = math.floor(int(str(x).split(':')[0]) * 2)
    if (('AM' in x) & (x.count(':00') == 0)):
        timeRange = math.floor(int(str(x).split(':')[0]) * 2) + 1
    if (('PM' in x) & (x.count(':00'))):
        timeRange = math.floor(int(str(x).split(':')[0]) * 2) + 24
    if (('PM' in x) & (x.count(':00') == 0)):
        timeRange = math.floor(int(str(x).split(':')[0]) * 2) + 25
    return timeRange

def set_time_interval(df):
    df['start_timeRange'] = df.Start_Time.map(lambda x: set_interval(x) )
    df['end_timeRange'] = df.End_Time.map(lambda x: set_interval(x))
    df['start_timeRange'] = df['start_timeRange'].replace(48,24)
    df['start_timeRange'] = df['start_timeRange'].replace(49,25)
    df['end_timeRange'] = df['end_timeRange'].replace(48,24)
    df['end_timeRange'] = df['end_timeRange'].replace(49,25)
    return df

def set_weekday(df):
    df['weekdays'] = df.Date.map(lambda x: x.weekday())
    return df


def main():
    df = pd.read_excel('../../../events.xlsx', sheet_name='Sheet1')
    df = drop_na(df)  # Drop column only contains NA

    # Save three firgures
    fig_outpath = os.path.abspath('../../../Figures/events.png')
    times_outpath = os.path.abspath('../../../Figures/times.png')
    category_outpath = os.path.abspath('../../../Figures/categories.png')
    general_plot(df, fig_outpath)
    df = times_category_plot(df, times_outpath, category_outpath)

    # Add Time interval and weekday information
    df = set_time_interval(df)
    df = set_weekday(df)

    # Save as new table
    df.to_excel('../../../Classified_events.xlsx')

if __name__ == '__main__':
    main()

