from datetime import datetime;
import pymongo
import time; 
import pandas as pd
# function for processing the opno to standard form
def extract_phone_number(ph_no):
    final_phone_number = ''.join([i for i in ph_no if i.isdigit() == True])
    return final_phone_number

# extract date from the [CREATED_AT]
def get_date(s):
	s  = str(s)
	ts = time.strftime('%Y-%m', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
 	do = datetime.strptime(ts,'%Y-%m');
 	return do;

connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
    
db = connection.PhoneBlacklist
legit = 'tech_legit'
spam  = 'tech_spam'

def get_data(tweets):
	print tweets.count()
	start_date = '2016-03-01'
	end_date   = '2018-02-01'
	# create pointers for all months
	index = pd.date_range(start_date,end_date,freq="MS");
	# stores count of new OPNOs seen very month
	monthly_count = {}
	for i in index:
		monthly_count[i]=0;

	# numbers that I have already seen before
	seen_numbers = set();
	for t in tweets:
		tweet = t['tweet']
		if('phone_no' in tweet):

			opno = tweet['phone_no'];
			opno = extract_phone_number(opno);
			if(opno not in seen_numbers):
				print 'new opno'
				seen_numbers.add(opno);
				if('created_at' in tweet):
					created_at = tweet['created_at'];
					print created_at
					date = get_date(created_at);
					if(date>datetime(2016,02,27)):
						#print 'increase monthly count'
						c = monthly_count[date];
						c=c+1;
						monthly_count[date]=c;

	print monthly_count
	sorted_dates = sorted(monthly_count);
	values=[]
	for s in sorted_dates:
			values.append(monthly_count[s]);
	return sorted_dates, values;

def plot_graph():
	legit_tweets = db[legit].find();
	spam_tweets = db[spam].find();

	sort_legit,values_legit = get_data(legit_tweets);
	sort_spam,values_spam = get_data(spam_tweets);
	linestyles = ['solid', 'dashed']
	import matplotlib as mpl    
	mpl.use('agg')  
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)

	plt.xlabel('Month',fontsize=20);
	plt.ylabel('Phone Numbers',fontsize=20);
	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)

	plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
	plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
	labels = ['Mar16', '', 'Sep16', '', 'Mar17', '', 'Sep17', '', 'Mar18', '']
	ax.set_xticklabels(labels)

	plt.legend(loc='best',fontsize=20)
	plt.tight_layout()
	plt.tight_layout()
	plt.grid()

	plt.savefig('../paper/New_Phone_Number_Per_Month.pdf')

plot_graph()
