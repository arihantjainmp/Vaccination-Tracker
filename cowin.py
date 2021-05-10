import requests
from datetime import date,datetime
import datetime as DT
import os
import smtplib
from time import time,ctime

email_user = 'hithere.abcxyz@gmail.com'
email_password = 'phoenixisdard'

sent_from = email_user
to = ['sakshi@getnada.com']

minutes = 1

today = date.today()
day2 = today+DT.timedelta(days=1)
day3 = today+DT.timedelta(days=2)
day4 = today+DT.timedelta(days=3)
day5 = today+DT.timedelta(days=4)
day6 = today+DT.timedelta(days=5)
day7 = today+DT.timedelta(days=6)


__district = "366" #kannur

'''
295 - Kasargod
296 - Thiruvananthapuram
298 - kollam
299 - Wayanad
300 - Pathanamthitta
302 - Malappuram
303 - thrissue
305 - Kozikode
306- idukki
307 - ernakulam
308 - palakkad
'''



d1 = today.strftime("%d/%m/%Y")
d2 = day2.strftime("%d/%m/%Y")
d3 = day3.strftime("%d/%m/%Y")
d4 = day4.strftime("%d/%m/%Y")
d5 = day5.strftime("%d/%m/%Y")
d6 = day6.strftime("%d/%m/%Y")
d7 = day7.strftime("%d/%m/%Y")

__date = str(d1).replace("/","-")
__date2 = str(d2).replace("/","-")
__date3 = str(d3).replace("/","-")
__date4 = str(d4).replace("/","-")
__date5 = str(d5).replace("/","-")
__date6 = str(d6).replace("/","-")
__date7 = str(d7).replace("/","-")

def send_email(res):
	# turn on allow less secure apps to get email
	#  https://myaccount.google.com/lesssecureapps
	# suggest to use a backup account for this to preserve security
	
	subject = 'Vaccine slot available in your area'
	body = "Following vaccines centers are found \n\n Query Time :  "+ctime(time())+"\n\n" + res

	email_text = """\
From: %s
To: %s 
Subject: %s
%s
""" % (sent_from, ", ".join(to), subject, body)
	print email_text

	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(email_user, email_password)
	    server.sendmail(sent_from, to, email_text)
	    server.close()

	    print 'Email sent!'
	except Exception as e:
	    print 'Something went wrong...'
	    print (e)
	


def parse_json(result):
	output = []
	centers = result['centers']
	for center in centers:
		sessions = center['sessions']
		for session in sessions:
			if session['available_capacity'] > 0:
				res = { 'name': center['name'], 'block_name':center['block_name'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , 'date':session['date'],'available_capacity':session['available_capacity'] }
				output.append(res)
	return output
				
	
def call_api(vardate):
    api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + __district+ "&date="+ vardate

    response = requests.get(api)

    if response.status_code == 200:
    	print('\007')
        print "API call success for " + vardate
        result = response.json()
        output = parse_json(result)
        if len(output) > 0:
            #print "Vaccines available"
            result_str = ""
            for center in output:

                '''print center['name']
                print "block:"+center['block_name']
                print "vaccine count:"+str(center['available_capacity'])
                print "vaccines type:" + center['vaccine_type']
                print center['date']
                print "age_limit:"+ str(center['age_limit'])
                print "---------------------------------------------------------" '''
                result_str = result_str + center['name'] + "\n"
                result_str = result_str + "block:"+center['block_name'] + "\n"
                result_str = result_str + "vaccine count:"+str(center['available_capacity']) + "\n"
                result_str = result_str + "vaccine type:"+ center['vaccine_type'] + "\n"
                result_str = result_str + center['date'] + "\n"
                result_str = result_str + "age_limit:"+str(center['age_limit'])+"\n"
                result_str = result_str + "-----------------------------------------------------\n"
            if(str(center['age_limit']) == '18'):
                send_email(result_str)
            else :
                print "Vaccine availiable but not for 18+"

        else:
            
            print "Vaccines not available"

t = datetime.now()

if __name__ == '__main__':
    print(ctime(time()))
    call_api(__date)
    call_api(__date2)
    call_api(__date3)
    call_api(__date4)
    call_api(__date5)
    call_api(__date6)
    call_api(__date7)
    while True:
        delta = datetime.now()-t
        if delta.seconds >= minutes * 60:
            call_api(__date)
            call_api(__date2)
            call_api(__date3)
            call_api(__date4)
            call_api(__date5)
            call_api(__date6)
            call_api(__date7)
            t = datetime.now()
