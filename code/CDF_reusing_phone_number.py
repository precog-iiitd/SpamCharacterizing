
from datetime import datetime;
import pymongo
import time; 
import pickle
import numpy as np
connection = pymongo.MongoClient(
        'mongodb://srishti:phdsucks@192.168.1.246/', connect=False)
    
db = connection.PhoneBlacklist#techsupport;
legit = 'tech_legit'
spam = 'tech_spam'

def extract_phone_number(ph_no):
    final_phone_number = ''.join([i for i in ph_no if i.isdigit() == True])
    return final_phone_number

def get_date(s):
    s = str(s)
    ts=s
    # ts = time.strftime('%Y-%m-%d', time.strptime(s,'%Y-%m-%d %H:%M:%S'))
    do = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S');
    print do
    return do;

def create_phone_dict(name):
    phone_date_dict = dict()
    tweets = db[name].find();
    print tweets.count()
    count = 0;
    d2016 = datetime(2016,01,01)
    for t in tweets:
        tweet = t['tweet']
        if('phone_no' in tweet):
            phone_no = tweet['phone_no'];
            phone_no = extract_phone_number(phone_no);
            created_at = None;
            if('created_at' in tweet):
                created_at = tweet['created_at'];
                created_at = get_date(created_at)
            if(phone_no not in phone_date_dict):
                phone_date_dict[phone_no] = [];
            phone_date_dict[phone_no].append(created_at)
        
        else:
            print '--------------ERROR-------------'    
    for phone_no in phone_date_dict:
        phone_date_dict[phone_no].sort()        
    print ' total numbers found ',len(phone_date_dict)
    print phone_date_dict;
    with open(name+'_reusing_phone_number_dict.pickle', 'wb') as fp:
        pickle.dump(phone_date_dict, fp)

# create_phone_dict(legit)
# create_phone_dict(spam)

with open('tech_legit_reusing_phone_number_dict.pickle', 'rb') as f:
        legit_phone_dict = pickle.load(f)

with open('tech_spam_reusing_phone_number_dict.pickle', 'rb') as f:
        spam_phone_dict = pickle.load(f)

def date_diff(date_list):
    diff=[]
    # print "";
    # print "len(dates):",len(date_list)
    count=0
    for i in range(0,len(date_list)-1):
        j=i+1;
        d1 = date_list[i];
        d2 = date_list[j];
        c=d2-d1;
        
        if(c.days==0 and c.seconds==0):
            count+=1
            # print d1,d2
        x = c.days*24*60;
        y = c.seconds//60
        diff.append(c.days);
    return diff 

def get_diff(phone_dict):
    lifetime = []
    for phone_no in phone_dict:
        date_list = phone_dict[phone_no];
        diff = date_diff(date_list);
        for d in diff:
            lifetime.append(d);
    print lifetime.count(0),lifetime.count(1)       
    sortedtime = np.sort(lifetime)
    p = 1. * np.arange(len(lifetime))/(len(lifetime) - 1)
    return sortedtime,p;

def get_avg(phone_dict):
    print('getiing average data')
    lifetime = []
    for phone_no in phone_dict:
        date_list = phone_dict[phone_no];
        diff = date_diff(date_list);
        if(len(diff)>0):
            sum=0
            for d in diff:
                sum+=d;
            sum = float(sum/len(diff))
            lifetime.append(sum)
            
    #print lifetime.count(0),lifetime.count(1)      
    c1,c2,c3,c4,c5=0,0,0,0,0
    for l in lifetime:
        if(l<1):
            c1+=1;
        elif(1<=l<4):
            c2+=1;
        elif(4<=l<11):
            c3+=1;
        elif(11<=l<30):
            c4+=1;
        elif(l>30):
            c5+=1
    c1=float(c1*100/len(lifetime))
    c2=float(c2*100/len(lifetime))      
    c3=float(c3*100/len(lifetime))      
    c4=float(c4*100/len(lifetime))      
    c5=float(c5*100/len(lifetime))      
            
    print c1,c2,c3,c4,c5    
    sortedtime = np.sort(lifetime)
    p = 1. * np.arange(len(lifetime))/(len(lifetime) - 1)
    return sortedtime,p;

def graph(legit_phone_dict,spam_phone_dict):
    sort_legit, values_legit = get_avg(legit_phone_dict)
    sort_spam, values_spam = get_avg(spam_phone_dict);
    import matplotlib as mpl    
    mpl.use('agg')  
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)

    linestyles = ['solid', 'dashed']
    plt.xlabel('Days',fontsize=20);
    plt.ylabel('CDF',fontsize=20);
    
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.set_xlim(0,200)  
    plt.plot(sort_spam,values_spam, color='crimson', label = 'Spam', linewidth=3.0, linestyle = linestyles[1])
    plt.plot(sort_legit,values_legit, color='royalblue', label = 'Legit', linewidth=3.0,linestyle = linestyles[0]);
    plt.legend(loc='best',fontsize=20)
    plt.tight_layout()
    plt.grid()
    plt.savefig('../paper/CDF_Phone_Reusability.pdf')

graph(legit_phone_dict,spam_phone_dict);
