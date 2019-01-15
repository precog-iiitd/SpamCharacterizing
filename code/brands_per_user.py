

from __future__ import division
import pymongo
import pickle
import re;
from datetime import datetime;
import numpy as np;
import time;
brands = ['safari','xbox','outlook', 'google', 'apple', 'office', 'youtube', 'canon', 'dell', 'skype', 'internet explorer', 'gmail', 'instagram', 'incredimail', 'chrome', 'OTHER_BRANDS',  'norton', 'quicken',  'iphone', 'hotmail',  'msoffice', 'hp', 'yahoo', 'facebook', 'icloud', 'Epson', 'whatsapp', 'ipad', 'mac', 'ms office',  'windows',  'brother', 'itunes', 'kindle', 'microsoft', 'quickbook']

#brand_dict = dict();

# for brand in brands:
# 	brand_dict[brand] = 0;
main_brands = ['quickbook', 'google', 'incredimail', 'apple', 'hp', 'canon', 'brother', 'dell', 'OTHER_BRANDS', 'hotmail', 'facebook', 'yahoo', 'kindle' , 'norton','quicken' ,'microsoft']
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'


def get_brand(text):
      try:	
	final_brand = None
	for brand in brands:
		if(bool(re.search(brand,text.lower()))):
			final_brand =  brand;
	#print final_brand
	
	if(final_brand  in ['instagram', 'whatsapp']): 
		return 'facebook'
		
	if(final_brand in ['xbox','windows','outlook','internet explorer','ms office','msn','msoffice','skype','office','lINKEDIN']):
		return 'microsoft'

	if(final_brand in ['gmail','chrome','youtube']):
		return 'google'

	if(final_brand in ['safari','mac','icloud','iphone','ipad','itunes']):
		return 'apple'

	if(final_brand == None):
		if(bool(re.search('fb ',text.lower()))):
				return 'facebook'
		return 'OTHER_BRANDS';	
	return final_brand

      except UnicodeEncodeError:
 	pass;

def get_data(tweets):
    
    user_dict={}
    for t in tweets:
        tweet = t['tweet']
        if('user' in tweet):
            brand = get_brand(tweet['text'])
            user = tweet['user'];
            user_id = None;
            user_id = user['id'];
            user_id_str = user['id_str']
            if(type(user_id) == float):
                user_id = str(user_id_str);
            else:
                user_id = str(user_id)
            
            if(user_id not in user_dict):   
           	    user_dict[user_id] = set();
            user_dict[user_id].add(brand);

    print " total users in :",len(user_dict);           
    lifetime=[]

    for user_id in user_dict:
        lifetime.append(len(user_dict[user_id]));
   
    print lifetime    
  
    sortedtime = np.sort(lifetime)
    p = 1. * np.arange(len(lifetime))/(len(lifetime) - 1)
    return sortedtime,p;

def plot_graph():

    legit_tweets = db[legit].find();
    spam_tweets = db[spam].find();

    print "---------------Legit---------------------"
    sort_legit,values_legit = get_data(legit_tweets);
    print "----------------Spam------------------------"
    sort_spam,values_spam = get_data(spam_tweets);
    colours = ['red', 'blue']
    linestyles = ['solid', 'dashed']

    import matplotlib as mpl    
    mpl.use('agg')  
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    plt.ylabel('CDF',fontsize=20)
    plt.xlabel('Brands',fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.set_xlim(0, 16)  
    ax.set_ylim(0,1);
    plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
    plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
    plt.legend(loc='best',fontsize=20)
    plt.tight_layout()
    plt.grid()
    plt.savefig("../paper/brands_per_user.pdf");

plot_graph()