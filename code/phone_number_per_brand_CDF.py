import pymongo
import pickle
import re;
from datetime import datetime;
import numpy as np;
import time;
brands = ['safari','xbox','outlook', 'google', 'apple', 'office', 'youtube', 'canon', 'dell', 'skype', 'internet explorer', 'gmail', 'instagram', 'incredimail', 'chrome', 'OTHER_BRANDS',  'norton', 'quicken',  'iphone', 'hotmail',  'msoffice', 'hp', 'yahoo', 'facebook', 'icloud', 'Epson', 'whatsapp', 'ipad', 'mac', 'ms office',  'windows',  'brother', 'itunes', 'kindle', 'microsoft', 'quickbook']

main_brands = ['quickbook', 'google', 'incredimail', 'apple', 'hp', 'canon', 'brother', 'dell', 'OTHER_BRANDS', 'hotmail', 'facebook', 'yahoo', 'kindle' , 'norton','quicken' ,'microsoft']
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'


def extract_phone_number(ph_no):
    final_phone_number = ''.join([i for i in ph_no if i.isdigit() == True])
    return final_phone_number

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

    lifetime=[]
    brand_dict = dict();
    for brand in main_brands:
        brand_dict[brand] = set() # add phone numbers to this

    for t in tweets:
        tweet = t['tweet']
        
        if("phone_no" in tweet):
            opno = tweet["phone_no"];
            opno = extract_phone_number(opno);
            brand = get_brand(tweet['text'])
            brand_dict[brand].add(opno);        
    for brand in main_brands:
        print brand,len(brand_dict[brand])
        lifetime.append(len(brand_dict[brand]))
    
  
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
    plt.xlabel('Phone numbers per brand',fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
    plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
    plt.legend(loc="best",fontsize=20)
    plt.tight_layout()
    plt.grid()
    plt.savefig("../paper/phone_numbers_per_brand_CDF.pdf");

plot_graph()