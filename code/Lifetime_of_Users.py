
from datetime import datetime;
import pymongo
import time; 

connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist
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
			user = tweet['user'];
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

	# for i in lifetime:
	# 	print lifetime[i];

	print lifetime;
	days={}
		# keys = number of days 
		# values  =  number of phone numbers with key as lifetime
	for i in lifetime:
			if(i in days):
				days[i]=days[i]+1
			else:
				days[i]=1;	
		
	lists = sorted(days.items()) # sorted by key, return a list of tuples
	x, y = zip(*lists) # unpack a list of pairs into two tuples
	return x,y

def plot_graph():
	legit_tweets = db[legit].find();
	spam_tweets = db[spam].find();
	sort_legit,values_legit = get_data(legit_tweets);
	sort_spam,values_spam = get_data(spam_tweets);

	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('Lifetime of Users');
	plt.xlabel('Number of Days');
	plt.ylabel('Number of Users')	
	plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0);
	plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,alpha=.2);
	plt.legend(loc='best')
	plt.tight_layout()
	plt.savefig('Lifetime_of_Users5.pdf')



plot_graph()













