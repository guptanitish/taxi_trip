
#this is potentially very interesting dataset. It has taxi trips in NYC for around a year. Let see it!
#does some exploratory analysis of the data; outputs two graphs in pwd

#get the input
taxi_data_path = "/home/nitish/fellowship/taxi_data/trip_data_12.csv"
import numpy as np
import pandas as pd
taxi_df = pd.read_csv(taxi_data_path)

#ahh, the columns names have leading spaces, not nice.
cols =taxi_df.columns.values
for i in range(0,len(cols)):
    cols[i] = cols[i].strip()

# In[27]:

taxi_df.columns = cols

#need this class since the for parsing timestamp.
class timestamp():
    def __init__(self,date):
        self.day = date.split(' ')[0]
        self.time = date.split(' ')[1]
        self.mm = int(self.day.split('-')[1])
        self.hh = int(self.time.split(':')[0])
        self.dd = int(self.day.split('-')[2])


import sys
hour=[]
day = []
print 'Procesing the input'
l = len(taxi_df)
for i in range(0,l):
    if i%300000 ==0:
        sys.stdout.write('.')
        sys.stdout.flush()
    t = timestamp(taxi_df.dropoff_datetime[i])
    hh = t.hh
    dd = t.dd
    hour.append(hh)
    day.append(dd)

taxi_df['hh']=hour
taxi_df['dd']=day


#ok, so i can predict the taxi demand
#include can do this according to location, or time of day, etc. +
#where you get most fares/tips
#or even fare/time analysis
# or on 4th of july
#to prove that this is viable, we look at cabs around times sq last 10
#days of Decmeber

new_df = taxi_df[(taxi_df.dropoff_longitude<= -73.0) & (taxi_df.dropoff_longitude>= -74.0) &(taxi_df.dd >=22) &(taxi_df.dd <29)]

relevant_df = new_df[['dd','hh','trip_time_in_secs']]
grp1 = relevant_df.groupby('dd').count()

# In[99]:

grp2 =  relevant_df.groupby(['dd','hh']).count()
grp3 =  relevant_df.groupby(['hh']).mean()
counts = np.zeros(168)
i = 0
for val in grp2.trip_time_in_secs:
    counts[i]=val
    i+=1

counts = counts.reshape(24,7)

np.argmax(counts,axis=0)


# In[189]:

import matplotlib.pyplot as plt
christmas, = plt.plot(counts[:5,3],label='25 Dec')
monday,=plt.plot(counts[:5,6],label='28 Dec')
plt.ylabel('Number of cabs arriving near Times square')
plt.xlabel('Time of day (midnight to 5 am)')
plt.title('Cab arriving near times square on Christmas day vs other day at night')
plt.legend(handles=[christmas,monday])

plt.savefig('number_cabs.png')


# In[176]:

import matplotlib.pyplot as plt
plt.plot(grp3.trip_time_in_secs)
plt.ylabel('Mean trip distances ')
plt.xlabel('Time of day, starting from midnight')
plt.title('Mean trip distances during various times of day')
plt.savefig('trip_dist.png')


# In[ ]:



