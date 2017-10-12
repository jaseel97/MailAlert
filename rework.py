#!/usr/bin/env python

import os
import imaplib
import socket
import getpass
import pickle
import time
from email.parser import HeaderParser
import pyglet

def main():
	os.system('clear')

	print '\tMAIL ALERT 2'
	print 'Connecting to Gmail Server...'

	os.system('clear')
	print '\tMAIL ALERT 2'

	try:
		connection_object = imaplib.IMAP4_SSL('imap.gmail.com')
	except socket.gaierror:
		print 'Cannot connect to Gmail Server. Please check your internet connection and restart MailAlert'

	login_attempts = 0
	loginProcess(connection_object,login_attempts)

	while True:
		last_mail = getLastMail(connection_object)
		#print last_mail['From']
		redundancy_flag = redundancyCheck(last_mail)
		if redundancy_flag == 1:
			updateLastMail(last_mail)
			priority = findPriority(last_mail)
			notifyUser(last_mail,priority)
		time.sleep(0.1)
		checkLogout(connection_object)


def loginProcess(connection_object,login_attempts):
	username = raw_input("Enter E-Mail ID : ")
	password = getpass.getpass()

	try:
		connection_object.login(username,password)
		print 'Logged In Successfully!'
		
	except imaplib.IMAP4_SSL.error:
		login_attempts = login_attempts + 1
		if login_attempts < 4 :
			attempts_left = 4 - login_attempts
			print 'Invalid Credentials! Login Attempts Left:',attempts_left
			print 'Enter login details again!'
			login_func(connection_object,login_attempts)
		else :
			print "Login Failed. Action will be reported !"
			exit()

def getLastMail(connection_object):
	inbox = connection_object.select('Inbox')
	raw_mail = connection_object.fetch(int(inbox[1][0]),'(BODY[last_mail])')
	raw_last_mail = raw_mail[1][0][1]
	parser_object = HeaderParser()
	last_mail = parser_object.parsestr(raw_last_mail)
	return last_mail

def checkLogout(connection_object):
	logout_status_file = open('logout.txt','r')
	logout_status = logout_status_file.read()
	logout_status = logout_status.upper()
	logout_status_file.close()

	if 'LOGOUT' in logout_status :
		connection_object.logout()

		logout_status_file = open('logout.txt','w')
		logout_status_file.close()

		print 'Logged out of current user!'
		exit()

def redundancyCheck(last_mail):

	current_sender = last_mail['From']
	current_subject = last_mail['Subject']
	current_date = last_mail['Received'].split()[7:10]
	current_time = last_mail['Received'].split()[10]

	last_mail_file = open('lastmail.txt','r')
	check_string = last_mail_file.read()
	last_mail_file.close()
	if check_string == '':
		last_mail_file = open('lastmail.txt','w')
		pickle.dump(last_mail['From'],last_mail_file)		              #Sender's name and mail-id
		pickle.dump(last_mail['Subject'],last_mail_file)			      #Subject of mail
		pickle.dump(last_mail['Received'].split()[7:10],last_mail_file) #Received Date ['day','month','year']
		pickle.dump(last_mail['Received'].split()[10],last_mail_file)   #Received Time
		last_mail_file.close()
		
		last_sender = last_mail['From']
		last_subject = last_mail['Subject']
		last_date = last_mail['Received'].split()[7:10]
		last_time = last_mail['Received'].split()[10]
	
	else :
		last_mail_file = open('lastmail.txt','r')
		last_sender = pickle.load(last_mail_file)
		last_subject = pickle.load(last_mail_file)
		last_date = pickle.load(last_mail_file)
		last_time = pickle.load(last_mail_file)

	sender_flag = current_sender == last_sender
	subject_flag = current_subject == last_subject
	date_flag = current_date == last_date
	time_flag = current_time == last_time		

	if sender_flag and subject_flag and date_flag and time_flag:
		return 0
	else :
		return 1

def updateLastMail(last_mail):
		last_mail_file = open('lastmail.txt','w')
		pickle.dump(last_mail['From'],last_mail_file)				
		pickle.dump(last_mail['Subject'],last_mail_file)			
		pickle.dump(last_mail['Received'].split()[7:10],last_mail_file) #Date as ['day','month','year']
		pickle.dump(last_mail['Received'].split()[10],last_mail_file)   
		last_mail_file.close()

def findPriority(last_mail):
	priority1_keys_file = open('priority1.txt','r')
	priority2_keys_file = open('priority2.txt','r')
	prioriy3_keys_file = open('prioriy3.txt','r')
	priority4_key_file = open('priority4.txt','r')
	priority5_keys_file = open('priority5.txt','r')

	p1_keys = priority1_keys_file.read().split()
	p2_keys = priority2_keys_file.read().split()
	p3_keys = priority3_keys_file.read().split()
	p4_keys = priority4_keys_file.read().split()
	p5_keys = priority5_keys_file.read().split()

	current_sender = last_mail['From']
	current_subject = last_mail['Subject']

	for key in p1_keys:
		if key in current_sender or key in current_subject:
			return 1

	for key in p2_keys:
		if key in current_sender or key in current_subject:
			return 2

	for key in p3_keys:
		if key in current_sender or key in current_subject:
			return 3

	for key in p4_keys:
		if key in current_sender or key in current_subject:
			return 4

	for key in p5_keys:
		if key in current_sender or key in current_subject:
			return 5

def notifyUser(last_mail,priority):
	print "__________________________________________________________________"
	print "Priority",priority,"mail"
	print "Sender    :",last_mail['From']
	print "Subject   :",last_mail['Subject']
	date = last_mail['Received'].split()[7:10]
	time = last_mail['Received'].split()[10]
	print "Timestamp :",'%s-%s-%s %s'%(date[0],date[1],date[2],time)
	print "__________________________________________________________________"

	path = "alert"+str(priority)
	alert_tone = pyglet.media.load(path) 
	alert_object = alert_tone.play()
	pyglet.clock.schedule_once(exiter,alert_tone.duration)
	pyglet.app.run()

def exiter(dt):
	pyglet.app.exit()
	#
	#


if __name__ == '__main__':
	main()
