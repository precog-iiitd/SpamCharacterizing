import pymongo;

from datetime import datetime, timedelta
import pandas as pd
import datetime as dt
import time;

def get_quarter(s):
	s = str(s)
	ts = time.strftime('%Y-%m', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
 	do = datetime.strptime(ts,'%Y-%m')
 	# 3,6,9,12
 	if(do.month<=3):
 		do = do.replace(month=3);
 	elif(do.month >3 and do.month <=6):
 		do = do.replace(month=6);
 	elif(do.month>6 and do.month<=9):
 		 do = do.replace(month=9);
 	elif(do.month>9 and do.month<=12):
 		 do = do.replace(month=12);
 	else:
 		print '----------error ------------';
 	return do;

connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
 
db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'

def get_values(tweets):
	all_dates =[]
	start = '2016-01-01'
	end   = '2018-04-01'
	index = pd.date_range(start,end,freq="Q");
	quarter_count = {}

	for i in range(len(index)):
		ts = time.strftime('%Y-%m', time.strptime(str(index[i]),'%Y-%m-%d %H:%M:%S'))
		do = datetime.strptime(ts,'%Y-%m')
		quarter_count[do]=0;
	print quarter_count	
	for t in tweets:
		tweet = t['tweet']
		if('created_at' in tweet):
			if(tweet['created_at']>datetime(2016,01,01)):
				all_dates.append(get_quarter(tweet['created_at']));
		else:
			print 'no date-----------'
	for date in all_dates:
		val = quarter_count[date];
		val = val+1;
		quarter_count[date] = val;
	sort = sorted(quarter_count)
	values=[]
	for s in sort:
		 values.append(quarter_count[s])
	print quarter_count;
	return sort, values	 

legit_tweets = db[legit].find();
spam_tweets = db[spam].find();
sort_legit,values_legit = get_values(legit_tweets);
sort_spam,values_spam = get_values(spam_tweets);
linestyles = ['solid', 'dashed']

import matplotlib as mpl    
mpl.use('agg')  
import matplotlib.pyplot as plt
fig=plt.figure()
ax = fig.add_subplot(111)

plt.xticks(fontsize=20) # rotation=40
plt.yticks(fontsize=20)
plt.semilogy(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
plt.semilogy(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);

labels = ['16Q1', '', '16Q3', '', '17Q1', '', '17Q3', '', '18Q1', '']
ax.set_xticklabels(labels)
plt.xlabel('Quarter', fontsize=20)
plt.ylabel('Posts(log)', fontsize=20)
plt.legend(loc=1,fontsize=20)
plt.tight_layout()
plt.grid()
plt.savefig('../paper/Volume_per_Quarter.pdf')
