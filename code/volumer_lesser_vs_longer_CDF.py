#volumer_lesser_vs_longer_CDF.py

from datetime import datetime;
import pymongo
import time; 
import numpy as np;


connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)

db = connection.PhoneBlacklist
legit = 'tech_legit'
spam = 'tech_spam'

start = datetime(2016,03,01);

def get_date(s):
    s = str(s)
    try:
        ts = time.strftime('%Y-%m-%d', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
        do = datetime.strptime(ts,'%Y-%m-%d');
    except:
        print 'date error'
        do = get_date2(s)
    if( (do-start).days<=0):
        return -1;
    else:
        return 1;

def get_date2(s):
    s = str(s)
    ts = time.strftime('%Y-%m-%d', time.strptime(s,'%a %b %d %H:%M:%S +0000 %Y'))
    do = datetime.strptime(ts,'%Y-%m-%d');
    return do

def get_data(tweets):
    total =0
    user_dict_longer = dict()
    user_dict_lesser = dict()
    for t in tweets:
        total+=1;
        tweet = t['tweet']
        if('user' in tweet):
            user = tweet['user'];
            user_id = None;
            created_at = None;
            if('id' in user):
                user_id = user['id'];
                if(user_id in user_dict_longer):
                    user_dict_longer[user_id]+=1;
                elif(user_id in user_dict_lesser):
                    user_dict_lesser[user_id]+=1;
                # not in both the list, lets check for created at
                else:
                    # get date of account creation
                    if('created_at' in tweet):
                        created_at = tweet['user']['created_at'];
                        print created_at
                        created_at = get_date(created_at)
                    else:
                       print '------created at error----------' 
                    if(created_at==-1):
                        # add to longer dict
                        user_dict_longer[user_id] =1
                    else:
                        user_dict_lesser[user_id] =1;

    l1 = []
    l2 = []
    for user in user_dict_longer:
        l1.append(user_dict_longer[user]);

    for user in user_dict_lesser:
        l2.append(user_dict_lesser[user]);
    
    sortedtime_longer = np.sort(l1)
    p_longer = 1. * np.arange(len(l1))/(len(l1) - 1)
    
    sortedtime_lesser = np.sort(l2)
    p_lesser = 1. * np.arange(len(l2))/(len(l2) - 1)
    
    return sortedtime_longer,p_longer,sortedtime_lesser,p_lesser
     

def plot_data():
    spam_tweets = db[spam].find();

    print "----------------Spam------------------------"
    sortedtime_longer,p_longer,sortedtime_lesser,p_lesser = get_data(spam_tweets);
    colours = ['red', 'blue']
    linestyles = ['solid', 'dashed']

    import matplotlib as mpl    
    mpl.use('agg')  
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    plt.ylabel('CDF',fontsize=20)
    plt.xlabel('Posts',fontsize=20)
    labels = ['0', '', '500', '', '1000', '', '1500', '', '2000', ]
    ax.set_xticklabels(labels)
    
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.set_xlim(0, 2000)  
    #ax.set_ylim(0,1);
    plt.plot(sortedtime_longer,p_longer, color='crimson', label = 'Longer', linewidth=3.0,linestyle = linestyles[1]);
    plt.plot(sortedtime_lesser,p_lesser, color='royalblue', label = 'Lesser', linewidth=3.0,linestyle = linestyles[0]);
    plt.legend(loc='best',fontsize=20)
    plt.tight_layout()
    plt.grid()
    plt.savefig("../paper/volumer_lesser_vs_longer_CDF.pdf");


plot_data()
        