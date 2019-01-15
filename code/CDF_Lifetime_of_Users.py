
from datetime import datetime;
import pymongo
import time; 
import numpy as np;
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'


def get_date(s):
	s = str(s)
	try:
		ts = time.strftime('%Y-%m-%d', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
	 	do = datetime.strptime(ts,'%Y-%m-%d');
 		return do;
 	except:
 		print 'date error'
 		return get_date2(s)

def get_date2(s):
	s = str(s)
	ts = time.strftime('%Y-%m-%d', time.strptime(s,'%a %b %d %H:%M:%S +0000 %Y'))
 	do = datetime.strptime(ts,'%Y-%m-%d');
 	return do;

class User:
	def __init__(self,user_id,created_at):
		self.user_id = user_id;
		self.created_at = created_at

def get_data(tweets):
	dic={}
	lifetime = []

	count = 0;
	x = set()
	for t in tweets:
		tweet = t['tweet']
		if('user' in tweet):
			user = tweet['user']
			user_id = None;
			created_at = None;
			if('id' in user):
				user_id = user['id'];
			if('created_at' in tweet):
				created_at = tweet['user']['created_at'];
				print created_at
				created_at = get_date(created_at)
			else:
			   print '------created at error----------'	
			if(user_id not in dic):
				count = count+1;
				obj = User(user_id,created_at);
				dic[user_id] = obj;
			
		else:
			print '--------------ERROR-------------'	

	print count;
	start = datetime(2016,03,01);
	for d in dic:
		diff = (dic[d].created_at-start).days
		lifetime.append(diff);

	# makes data ready for CDF
	print lifetime;
	sortedtime = np.sort(lifetime)
	p = 1. * np.arange(len(lifetime))/(len(lifetime) - 1)
   	return sortedtime,p;

def plot_graph():
	legit_tweets = db[legit].find();
	spam_tweets = db[spam].find();
	
	# get data for CDF
	sort_legit,values_legit = get_data(legit_tweets);
	sort_spam,values_spam = get_data(spam_tweets);

	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xlabel('Days',fontsize=20);
	plt.ylabel('CDF',fontsize=20);
	labels = ['','', '-3000', '', '-2000', '', '-1000', '', '0', '500' ]
	ax.set_xticklabels(labels)
	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)

	linestyles = ['solid', 'dashed']
  	plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);   
  	plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
  	plt.grid()
	plt.legend(loc = 4,fontsize=20)
	plt.tight_layout()	
	plt.savefig('../paper/CDF_Lifetime_of_Users.pdf')

plot_graph()















