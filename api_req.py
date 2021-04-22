import requests
import json
from datetime import datetime
import db
import re

ACCESS_KEY='ebb19de7a76fbf9ff6b6575a6a62c629&'
BASE='EUR'
API_LINK=f'http://api.exchangeratesapi.io/latest?access_key={ACCESS_KEY}'


def chek_last_time():
    """chek if taken at last 10 min"""
    time=db.fetch_time()
    if  (datetime.timestamp(datetime.now())-time<600):
        return True
    else:
        return False

def make_str(rates):
    """make str from retes list"""
    return_str=''
    rates=dict(rates)
    for item in rates:
        rates[item]=round(rates[item],2)
        return_str+=str(item)+': '+str(rates[item])+'\n'
    return return_str

def get_lates():
    """get lates rates"""
    if chek_last_time():
        try:
            req=requests.get(API_LINK)
            req=json.loads(req.content)
            time=req['timestamp']
            rates=req['rates']

            db.inset_values(time,rates)
        except:
            time=db.fetch_time()
            rates=db.fetch_val()
    else:
        time=db.fetch_time()
        rates=db.fetch_val()

    return time,rates

def get_lates_list():
    """func to get list of rates"""
    time,rates=get_lates()
       
    return_str=make_str(rates)
    return return_str

def parse_message(message):
    """parsing str to get amoun, base und symbols"""
    message=re.sub('/exchange','',message).split('to')
    message[0]=list(re.findall("(\d+)\W*(\w+)",message[0])[0])
    amount, base=message[0][0],message[0][1]
    symbols=re.findall("(\w+)",message[1])[0]
    return amount, base, symbols


def exchange(message):
    """function to exchanching some val"""
    amount,base,symbols=parse_message(message)
    payload={'base':str(base),'symbols':symbols}
    try:
        req=json.loads(requests.get(API_LINK,params=payload).content)
        if req['success']!='false':
            course=req['rates'][symbols]
            return_amount=float(amount)*float(course)
            return str(return_amount)+" "+str(symbols)
        else:
            return "Sorry, haven`t access to this function"
    except Exception as e:
        return "Smt went wrong!"
        raise e
# "/exchange 10 EUR to UAH"
