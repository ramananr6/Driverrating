#!/usr/bin/env python
# coding: utf-8

# In[58]:


def ratingdrv(data):
    
    import pandas as pd
    import numpy as np
    data = pd.read_csv("/home/ramanan/Documents/Work/26dec/Day26trips/date26trip4.csv")
    data = data[~(data['speed'] <= 5)] 
    speed = data['speed']
    speed = speed.dropna()
    maxspeed = max(speed)
    harsh = speed.diff()
    harsh = harsh.dropna()
    harshaccleration = max(harsh)
    harshbrake = min(harsh)
    Averagespeed = speed.mean()
    gyroy = data[['speed','gyroscope-y']]  
    gyroy = gyroy.dropna()
    newy = gyroy[['gyroscope-y']].diff(periods=1)
    newy = newy.rename(columns={'gyroscope-y': 'gyroscope-y-diff'})
    gyroy['gyroscope-y-diff'] = newy
    gyroy = gyroy.drop(['gyroscope-y'], axis=1)
    harshturn = gyroy[(gyroy > 50).any(1)]
    turnspeed = harshturn['speed']
    if len(turnspeed.index) == 0 :
        harshturnspeed = 0
        Avgturnspeed = 0 
    else:
        harshturnspeed = round(max(turnspeed))
        Avgturnspeed = round(turnspeed.mean())
    current = data[['sensor current']]  
    current[current < 0] = 0
    currentapplied = (current != 0).any(axis=1)
    new_currentapplied = current.loc[currentapplied]
    maximumcurrent = int(new_currentapplied.max())
    avgcurrent = int(new_currentapplied.mean())
    conditions = [
    (maximumcurrent <= 99),
    (maximumcurrent > 100) & (maximumcurrent <= 149),
    (maximumcurrent > 150) & (maximumcurrent <= 200),
    (maximumcurrent > 200)
    ]
    ranges = ['good', 'average', 'belowavg', 'poor']
    fixrange = np.select(conditions, ranges)
    
    if (fixrange == 'good'):
        currentproduced = 1
    elif (fixrange == 'average'):
        currentproduced = 0.75
    elif (fixrange == 'belowavg'):
        currentproduced = 0.50
    else :
        currentproduced = -1
    
    if (avgcurrent > 100):
        currentproduced = currentproduced - 0.25
    else:
        currentproduced = currentproduced + 0.25
    
    if (harshaccleration > 15):
        scoreharshaccleration = 0.50
    else:
        scoreharshaccleration = 0.25
    if (harshbrake > -18):
        scoreharshbrake = 1.5
    else:
        scoreharshbrake = 0.75
    if (Averagespeed > 24):
        scoreAveragespeed = 1.5
    else:
        scoreAveragespeed = 0.75
    if (maxspeed > 37):
        scoremaxspeed = -3
    else:
        scoremaxspeed = 2
    if (harshturnspeed > 27):
        scoreharshturnspeed = 0.75
    else:
        scoreharshturnspeed = 1.5
    if (Avgturnspeed > 21):
        scoreAvgturnspeed = 0.75 
    else:
        scoreAvgturnspeed = 1.5
    
    
    print(maxspeed)
    print(Averagespeed)
    print(harshaccleration)
    print(harshbrake)
    print(harshturnspeed)
    print(Avgturnspeed)
    print(currentproduced)
    print(maximumcurrent)
    print(avgcurrent)
    
    ratings = scoreharshaccleration + scoreharshbrake + scoreAveragespeed + scoremaxspeed + scoreharshturnspeed + scoreAvgturnspeed + currentproduced
    ratings = ratings/2
    ratings = round(ratings, 2)
    
    if (ratings < 0.49):
        ratings = 0.5
    
    return ratings


# In[59]:


ratingdrv(data)


# In[11]:




