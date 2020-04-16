__version__ = '0.1.2'
from pprint import pprint as print
from datetime import datetime, timedelta
from datetime import date

import pandas as pd
import numpy as np
import lh3.api as lh3



def remove_practice_queues(chats_this_day):
    """remove all chats thas was from the
    Practice queues

    Arguments:
        chats_this_day {[list of dict]} -- [description]

    Returns:
        [list of dict] -- [Filtered chats]
    """
    res = [chat for chat in chats_this_day if not "practice" in chat.get("queue")]
    return res

def clean_chats_dictionnary(all_chats):
    """General cleaning

    Arguments:
        all_chats {[list of dict]} -- [description]

    Returns:
        [list of dict] -- [Filtered chats]
    """
    chats_this_day = remove_practice_queues(all_chats)
    chat_not_none = [chat for chat in chats_this_day if chat.get("accepted") != None]
    return chat_not_none

def delete_columns(df):
    """Columns to remove from the
    DataFrame

    Arguments:
        df {[DataFrame]} -- [description]

    Returns:
        [DataFrame] -- [description]
    """
    columns = ['duration', 'protocol', 'queue',
                'profile', 'reftracker_id',
                'reftracker_url', 'desktracker_id',
                'desktracker_url', 'wait', 'ip',
                'referrer', 'accepted', 'started',
                'ended']
    for col in columns:
        del df[col]
    return df

def prepare_dataframe(data):
    """creating a Dataframe from
    the list of Chats

    Arguments:
        data {[list of chats]} -- [description]

    Returns:
        [type] -- [description]
    """
    df = pd.DataFrame(data)

    df['started'] = pd.to_datetime(df['started'])
    df['ended'] = pd.to_datetime(df['ended'])
    df["started_time"] = pd.to_datetime(df['started'])
    df["ended_time"] = pd.to_datetime(df['ended'])
    df["date"] = df['started'].apply(lambda x:x.date())
    df = delete_columns(df)

    return df

def count_simul(group):
    """https://stackoverflow.com/a/61218897/2581266

    Arguments:
        group {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    n = 0
    g = []
    ranges = {}

    # For each user, start the loop with a time range covering the distant
    # past to distant future
    started_time = pd.Timestamp('1900-01-01')
    ended_time = pd.Timestamp('2099-12-31')

    for index, row in group.iterrows():
        if (row['started_time'] < ended_time) and (started_time < row['ended_time']):
            # If the current row overlaps with the time range defined by
            # `started_time` and `ended_time`, set `started_time` and
            # `ended_time` to the intersection of the two. And keep the row
            # in the current time group
            started_time = max(started_time, row['started_time'])
            ended_time = min(ended_time, row['ended_time'])
        else:
            # Otherwise, set `started_time` and `ended_time` to those of the
            # current row and assign the current row to a new time group
            started_time, ended_time = row[['started_time', 'ended_time']]
            n += 1

        # `ranges` is a dictionary mapping each group number to the time range
        ranges[n] = (started_time, ended_time)
        g.append(n)

    # Group the rows by their time group number and get the size
    freq = group.groupby(np.array(g)).size()
    freq.index = freq.index.map(ranges)
    return freq

def find_concurrent_chats(all_chats):
    """main function
    
    Arguments:
        all_chats {[list of dict]} -- [list of chats]
    
    Returns:
        [pd.DataFrame] -- [Username - total concurrent chats]
    """
    data = clean_chats_dictionnary(all_chats)
    df = prepare_dataframe(data)
    df = df.sort_values(['operator', 'started_time', 'ended_time']) \
        .groupby('operator') \
        .apply(count_simul) \
        .replace(1, np.nan).dropna()
    df = df.to_frame().reset_index()
    df = df.rename(columns={0: 'total concurrent chats', 'level_2': 'Datetime'})
    df["Datetime"] = df['Datetime'].apply(lambda x:x.date())
    del df['level_1']
    df = df.sort_values(['Datetime', 'total concurrent chats'])
    # print(df.tail(50))
    return df

if __name__ == '__main__':
    client = lh3.Client()
    chats = client.chats()
    #if I want a result for a specific day
    all_chats = chats.list_day(2019,9,9)
    all_chats = chats.list_day(2019,9,9, to="2020-04-09")
    df = concurrent_chats(all_chats)

    df.to_excel("concurrent_chats.xlsx", index=False)

    print(df.tail(50))

    #breakpoint()
