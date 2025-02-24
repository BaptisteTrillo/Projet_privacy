#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from datetime import datetime as dt

# In[1]:

def infer_home_work(df):

    hour = []
    df_to_array = df.values
    lendf = len(df_to_array)
    for i in range(lendf):
        data_i = df_to_array[i]
        hour.append(dt.strftime(data_i[1], "%H:%M:%S"))
    df['time_h'] = hour
    
    #Infer 'Domicile' from the hour
    
    list_stops = set(df[(df.time_h >= '02:00:00') & (df.time_h <= '05:00:00')].stops.unique())
    for item in list_stops:
        if item !=-1:
            df.loc[df.stops==item, 'stops'] = 'Domicile'
    
    
    ##Infer 'Bureau' as one of the most visisted place (the first or second)
    
    df_groupby = df.groupby('stops').count().sort_values('participant_virtual_id',  ascending=False).reset_index()
    list_stops2 = list(df_groupby.stops)
    
    for item in list_stops2:
        if (item == 'Domicile') | (item == -1):
            pass
        else:
            df.loc[df.stops==item, 'stops'] = 'Bureau'
            break
            
    df.drop(['time_h'], axis=1, inplace=True)
    
    return df

# In[2]:

def home_stops(df):
    hour = []
    df_to_array = df.values
    lendf = len(df_to_array)
    for i in range(lendf):
        data_i = df_to_array[i]
        hour.append(dt.strftime(data_i[1], "%H:%M:%S"))
    df['time_h'] = hour
    
    #Infer 'Domicile' from the hour
    
    list_stops = set(df[(df.time_h >= '02:00:00') & (df.time_h <= '05:00:00')].stops.unique())
       
    #check if the list_stops is actually 'domicile'
    
    if bool(list_stops & set(df[df.activity=='Domicile'].stops.unique())):
        if list_stops & set(df[df.activity=='Domicile'].stops.unique()) == {-1}:
            df.loc[df.activity=='Domicile', 'stops'] = 888888
        else:
            pass
    else:
        
        if len(df[df.activity=='Domicile'].stops.unique()) == 1:
            if df[df.activity=='Domicile'].stops.unique() == -1:
                df.loc[df.activity=='Domicile', 'stops'] = 888888
        
        list_stops.union(set(df[df.activity=='Domicile'].stops.unique()))
        
    if -1 in list_stops:
        list_stops.remove(-1)
    
    #print('''Stops number %s belong to 'Home' ''' % list_stops)
    for item in list_stops:
        df.loc[df.stops==item, 'stops'] = 'Domicile'
    
    
    #list_home = df[df.stops=='Domicile'].hilbert.unique()
    
    return list_stops


# In[2]:

def work_stops(df):
    
    df_groupby = df.groupby('stops').count().sort_values('participant_virtual_id',  ascending=False).reset_index()
    list_stops2 = list(df_groupby.stops)
    work = []
    
    for item in list_stops2:
        if (item == 'Domicile') | (item == -1):
            pass
        else:
            work.append(df.loc[df.stops==item, 'stops'].iloc[0])
            #df.loc[df.stops==item, 'stops'] = 'Bureau'
            break
            
    if bool(set(work) & set(df[df.activity=='Bureau'].stops.unique())):
        
        if set(work) & set(df[df.activity=='Bureau'].stops.unique()) == {-1}:
            df.loc[df.activity=='Bureau', 'stops'] = 999999
        else:       
            pass
    
    else:
        if len(df[df.activity=='Bureau'].stops.unique()) == 1:
            if bool(df[df.activity=='Bureau'].stops.unique() == -1):
                work.append(999999)
                df.loc[df.activity=='Bureau', 'stops'] = 999999
            else:
                work.append(df.loc[df.activity=='Bureau', 'stops'].iloc[0])
                
    
    work = set(work)
    if -1 in work:
        work.remove(-1)
        
    #print('''Stops number %s belong to 'Work' ''' % work)        
    for item in work:
        df.loc[df.stops==item, 'stops'] = 'Bureau'
    
    #list_work = df[df.stops=='Bureau'].hilbert.unique()
    
    return work