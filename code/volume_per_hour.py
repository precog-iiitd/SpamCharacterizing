from datetime import datetime;
import pymongo
import time; 
import pandas as pd
import math;

def get_hour(s):
	s  = str(s)
	#ts = time.strftime('%Y-%m', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
 	do = datetime.strptime(s,'%Y-%m-%d %H:%M:%S');
 	if(do.hour<0 or do.hour>23):
 		print 'error:',do.hour
 	return do.hour;

connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
 
db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'

def get_values(tweets):
		#stores volume per hour
		hour_count =dict()
		for i in range(0,24):
			hour_count[i] = 0;
		for t in tweets:
			tweet = t['tweet']
			if('created_at' in tweet):
				hour = get_hour(tweet['created_at']);
				hour_count[hour] = hour_count[hour]+1;

		print hour_count

		#plotting code
		sort = sorted(hour_count)
		values=[]
		for s in sort:
			 values.append(math.log(hour_count[s]))

		print sort;
		print values;
		return sort,values;

legit_tweets = db[legit].find();
spam_tweets = db[spam].find();
sort_legit,values_legit = get_values(legit_tweets);
sort_spam,values_spam = get_values(spam_tweets);
linestyles = ['solid', 'dashed']
import matplotlib as mpl    
mpl.use('agg')  
import matplotlib.pyplot as plt
#fig = plt.figure(num=None, figsize=(7, 4.5), dpi=80, facecolor='w', edgecolor='k')
fig = plt.figure()
ax = fig.add_subplot(111)

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# plot--->semilogy
plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
ax.set_xlim(0,23)
#ax.set_ylim(0,15000)
plt.xlabel('Time of the day', fontsize=20)
plt.ylabel('Posts', fontsize=20)
plt.legend(loc=1,fontsize=20)
plt.tight_layout()
plt.rc('font', family='serif')
plt.grid()
plt.savefig('../paper/volume_per_hour.pdf')
