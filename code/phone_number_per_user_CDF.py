
from datetime import datetime;
import pymongo
import time; 
import numpy as np;
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'

def get_data(tweets):
    
    user_dict={}
    for t in tweets:
        tweet = t['tweet']
        if('user' in tweet):
            phone_no = tweet['phone_no']
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
            user_dict[user_id].add(phone_no);

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
    spam_tweets =  db[spam].find();

    sort_legit,values_legit = get_data(legit_tweets);
    sort_spam,values_spam = get_data(spam_tweets);
    colours    =    ['red','blue']
    linestyles =    ['solid', 'dashed']

    import matplotlib as mpl    
    mpl.use('agg')  
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax  =  fig.add_subplot(111)
    
    plt.ylabel('CDF ', fontsize = 20)
    plt.xlabel('Phone numbers per user', fontsize = 20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.set_xlim(0, 20)  
    ax.set_ylim(0.7,1);
    plt.plot(sort_spam,values_spam, color='crimson',label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
    plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
    labels = ['0', '', '5', '', '10', '', '15', '', '20']                                                                                             
    ax.set_xticklabels(labels)

    plt.legend(loc='best',fontsize=20)
    plt.tight_layout()
    plt.grid()
    plt.savefig("../paper/phone_number_per_user_CDF.pdf");

plot_graph()