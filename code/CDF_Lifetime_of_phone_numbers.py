
from datetime import datetime;
import pymongo
import time; 
import pandas as pd
import numpy as np
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
    
db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'

# opno_list=opno_list.unique_opno;


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
	return lifetime;

def graph2():
	legit_tweets = db[legit].find();
	spam_tweets = db[spam].find();
	legit_lifetime = get_data(legit_tweets)
	spam_lifetime  = get_data(spam_tweets)
	sort_legit = np.sort(legit_lifetime)
	values_legit = 1. * np.arange(len(legit_lifetime))/(len(legit_lifetime) - 1)
   	
   	sort_spam = np.sort(spam_lifetime)
   	values_spam = 1. * np.arange(len(spam_lifetime))/(len(spam_lifetime) - 1)
   	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xlabel('Days',fontsize=20);
	plt.ylabel('CDF',fontsize=20);
	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)

	plt.axvline(x=365, linestyle='--')
	linestyles = ['solid', 'dashed']
        plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);   
        plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
        plt.grid()
	
	plt.legend(loc='best',fontsize=20)
	plt.tight_layout()
	plt.savefig('../paper/CDF_Lifetime_of_phone_numbers.pdf')

graph2()





