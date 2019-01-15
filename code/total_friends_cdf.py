
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
    user_dict={}
    
    for t in tweets:
        tweet = t['tweet']
        if('user' in tweet):
            user = tweet['user'];
            user_id = None;
            user_id = user['id'];
            user_id_str = user['id_str']
            if(type(user_id) == float):
                user_id = str(user_id_str);
            else:
                user_id = str(user_id)
            if(user_id not in user_dict):   
                #print "adding followers count for user:",user_id,user['friends_count']
                user_dict[user_id] = int(user['friends_count'])
                #friends_count
    print " total users in :",len(user_dict);           
    lifetime=[]
    for user_id in user_dict:
        lifetime.append(user_dict[user_id]);
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
    
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    #ax.set_title('CDF of Number of Friends of Users');
    
    #plt.axhline(linewidth = 2.5, color = "black")
    #plt.axvline(linewidth = 2.5, color = "black")
    #plt.xlabel('Number of Days');
    #plt.ylabel('Number of Users');
    #plt.ylabel('Lifetime ', fontsize = 18)
    plt.ylabel('CDF ', fontsize = 10)
    plt.xlabel('# Friends of Users', weight = "bold", fontsize = 10)
    ax.set_xlim(0, 6000)  
    ax.set_ylim(0,1);
    plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0,linestyle = linestyles[1]);
    plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
    plt.legend(loc=4)
    plt.tight_layout()
    #plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid()
    file_time = time.strftime("%H_%M",time.localtime())
    plt.savefig("total_friends_cdf_"+file_time+"_linestyle"+".pdf");

plot_graph()










