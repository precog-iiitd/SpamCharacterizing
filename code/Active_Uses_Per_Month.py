from datetime import datetime;
import pymongo
import time; 
import pandas as pd

def get_month(s):
	s  = str(s)
	ts = time.strftime('%Y-%m', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
 	do = datetime.strptime(ts,'%Y-%m');
 	return do;

connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
 
db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'


start_date = '2016-03-01'
end_date   = '2018-02-01'
# create pointers for all months
index = pd.date_range(start_date,end_date,freq="MS");

def get_data(tweets):
	# dictionary of unique users per month
	# Key = month
	# value = set that holds all unique user IDs
	monthly_user=dict();
	for i in index:
		monthly_user[i] = set() # set of unique user ids

	for t in tweets:
		tweet = t['tweet']
		if('user' in tweet):
			user_id = tweet['user']['id']
			created_at = get_month(tweet['created_at']);
			try:
			     monthly_user[created_at].add(user_id);
			except KeyError as e:
				pass;     
	mu=dict();

	for i in monthly_user:
		mu[i] = len(monthly_user[i]);

	print mu;
	sort = sorted(mu)
	values=[]
	for s in sort:
		 values.append(mu[s])

	return sort, values;

legit_tweets = db[legit].find();
spam_tweets = db[spam].find();

sort_legit,values_legit = get_data(legit_tweets);
sort_spam,values_spam = get_data(spam_tweets);
linestyles = ['solid', 'dashed']

import matplotlib as mpl    
mpl.use('agg')  
import matplotlib.pyplot as plt
fig = plt.figure(num=None, figsize=(7, 4.5), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
ax.set_title('Active Users per Month');
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.xlabel('Months', fontsize=10)
plt.ylabel('Number of Active Users', fontsize=10)

plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
plt.legend(loc="best")
plt.tight_layout()
plt.rc('font', family='serif')
plt.grid()
file_time = time.strftime("%H_%M",time.localtime())
plt.savefig('Active_Uses_Per_Month'+file_time+'.pdf')
