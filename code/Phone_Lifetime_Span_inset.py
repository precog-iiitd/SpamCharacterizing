
from datetime import datetime;
import pymongo
import time; 
import pandas as pd
import numpy as np
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
    
db = connection.PhoneBlacklist#techsupport;
#legit = 'tech_legit'
spam = 'tech_spam'




def extract_phone_number(ph_no):
    final_phone_number = ''.join([i for i in ph_no if i.isdigit() == True])
    return final_phone_number

def get_date(s):
	s = str(s)
	ts = time.strftime('%Y-%m-%d', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
 	do = datetime.strptime(ts,'%Y-%m-%d');
 	return do;

class Opno:
	def __init__(self,no):
		self.opno = no;
		self.first_seen = datetime.now();
		self.last_seen = datetime(2000,01,01);

	def update_seen(self,new_date):
		
		if(new_date<self.first_seen):
			#print 'updating dates--first seen'
			self.first_seen = new_date;
		if(new_date> self.last_seen):
			#print 'updating dates -- last seen'
			self.last_seen = new_date;

def get_data(tweets):
	dic={}
	lifetime = []

	count=0
	for t in tweets:
		tweet = t['tweet']
		if("phone_no" in tweet):
			opno = tweet["phone_no"];
			opno = extract_phone_number(opno);
			created_at = None;
			if('created_at' in tweet):
				created_at = get_date(tweet['created_at']);
			else:
				print '------created at error----------'	
			if(opno not in dic):
				count = count+1;
				#print 'creating new object:',count;
				obj = Opno(opno);
				dic[opno] = obj;
			dic[opno].update_seen(created_at);
		else:
			print '--------------ERROR-------------'	

	print 'unique numbers :',count
	print 'dictionary count:', len(dic)
	for d in dic:
		#print dic[d].opno,' ', dic[d].last_seen,' ',dic[d].first_seen
		diff = (dic[d].last_seen-dic[d].first_seen).days
		#print diff;
		lifetime.append(diff+1);

	print lifetime;

	days={}
	# keys = number of days 
	# values  =  number of phone numbers with key as lifetime
	for i in lifetime:
		if(i in days):
			days[i]=days[i]+1
		else:
			days[i]=1;	
	print days;
	return days

def graph1():
	spam_tweets = db[spam].find();
	days = get_data(spam_tweets)

	lists = sorted(days.items()) # sorted by key, return a list of tuples
	x, y = zip(*lists)

	#import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt
	overview_data_x = x;
	overview_data_y = y;
	fig, ax = plt.subplots() # create a new figure with a default 111 subplot
	ax.plot(overview_data_x, overview_data_y)
	ax.set_title('Phone Lifetime');
	plt.xlabel(' No. of Days Phone Number is Active');
	plt.ylabel('Count of Phone Numbers')
	from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

	# magnification of the image = 2 SIZE OF THE  IMAGE
	axins = zoomed_inset_axes(ax, 2, loc=9) # zoom-factor: 2.5, location: upper-left
	axins.plot(overview_data_x, overview_data_y)

	x1, x2, y1, y2 = -3, 100, 0, 12 # specify the limits
	axins.set_xlim(x1, x2) # apply the x-limitsr 
	axins.set_ylim(y1, y2) # apply the y-limits
	#plt.yticks(visible=False)
	#plt.xticks(visible=False)	
	from mpl_toolkits.axes_grid1.inset_locator import mark_inset
	mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
	#lt.show()
	plt.savefig('Phone_Lifetime_Span_inset.png')

graph1()

def graph2():

	#legit_tweets = db[legit].find()
	spam_tweets = db[spam].find();
	
	#legit_days = get_data(legit_tweets)
	spam_days = get_data(spam_tweets)
	
	#legit_lists = sorted(legit_days.items()) # sorted by key, return a list of tuples
	#sort_legit, values_legit = zip(*legit_lists) # unpack a list of pairs into two tuples 	
	
	spam_lists = sorted(spam_days.items()) # sorted by key, return a list of tuples
	sort_spam, values_spam = zip(*spam_lists) # unpack a list of pairs into two tuples 	
	
	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('Lifetime of Phone Numbers');
	plt.xlabel('Number of Days');
	plt.ylabel('Number of Phone Numbers');
	#plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0);
	plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0);
	plt.legend(loc='best')
	plt.tight_layout()
	plt.savefig('_Lifetime_of_phone_numbers.png')

#graph2()





