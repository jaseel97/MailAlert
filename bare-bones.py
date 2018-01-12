#!/usr/bin/env python
import imaplib
import pyglet
import getpass
from email.parser import HeaderParser
import os
import socket
import time
import pickle

def check_for_new_mail():

	new_status = open('lastmail.txt','r')
	stat = new_status.read()
	new_status.close()

	inbox = conn.select('Inbox')
	data = conn.fetch(int(inbox[1][0]),'(BODY[HEADER])')
	raw_header = data[1][0][1]
	parser = HeaderParser()
	header = parser.parsestr(raw_header)

	if stat == '':
		update_new_stat = open('lastmail.txt','w')
		pickle.dump(header['From'],update_new_stat)		                             #Sender's name and mail-id
		pickle.dump(header['Subject'],update_new_stat)			      #Subject of mail
		pickle.dump(header['Received'].split()[7:10],update_new_stat) #Received Date ['day','month','year']
		pickle.dump(header['Received'].split()[10],update_new_stat)   #Received Time
		update_new_stat.close()
		last_sender = header['From']
		last_subject = header['Subject']
		last_date = header['Received'].split()[7:10]
		last_time = header['Received'].split()[10]
	else :
		last_mail = open('lastmail.txt','r')

		last_sender = pickle.load(last_mail)
		last_subject = pickle.load(last_mail)
		last_date = pickle.load(last_mail)
		last_time = pickle.load(last_mail)

	current_sender = header['From']
	current_subject = header['Subject']
	current_date = header['Received'].split()[7:10]
	current_time = header['Received'].split()[10]
	val1 = current_sender == last_sender
	val2 = current_subject == last_subject
	val3 = current_date == last_date
	val4 = current_time == last_time

	if current_sender == last_sender :
		if current_subject == last_subject:
			if current_date ==last_date:
				if current_time == last_time:
					pass
				else:
					preamp(header)
			else:
				preamp(header)
		else:
			preamp(header)
	else :
		preamp(header)

def preamp(header):
	update_new_stat = open('lastmail.txt','w')
	pickle.dump(header['From'],update_new_stat)				#Sender's name and mail-id
	pickle.dump(header['Subject'],update_new_stat)			      	#Subject of mail
	pickle.dump(header['Received'].split()[7:10],update_new_stat) 		#Received Date ['day','month','year']
	pickle.dump(header['Received'].split()[10],update_new_stat)   		#Received Time
	update_new_stat.close()
	soundjob1(header['From'],header['Subject'],header['Received'].split()[7:10],header['Received'].split()[10])

def soundjob1(key1,key2,date,time):
	p1_file = open('priority1.txt','r')
	p2_file = open('priority2.txt','r')
	p3_file = open('priority3.txt','r')
	p4_file = open('priority4.txt','r')
	p5_file = open('priority5.txt','r')
	keys={'p1':p1_file.read().split(),'p2':p2_file.read().split(),'p3':p3_file.read().split(),'p4':p4_file.read().split(),'p5':p5_file.read().split()}
	flag = 0
	for ele in keys['p1']:
		if ele in key1 or ele in key2:
			flag =1
			#print 'calling p1 soundjob()'
			soundjob2('priority1.wav')
			print "You have a priority1 message"
			print "Sender :",key1
			print "Subject:",key2
			print "Date   :",'%s-%s-%s'%(date[0],date[1],date[2])
			print "Time   :",time
			print "______________________________________________"
			break
	if flag != 1:
		for ele in keys['p2']:
			if ele in key1 or ele in key2:
				soundjob2('priority2.wav')
				print "You have a priority2 message"
				print "Sender :",key1
				print "Subject:",key2
				print "Date   :",'%s-%s-%s'%(date[0],date[1],date[2])
				print "Time   :",time
				print "______________________________________________"
				break
	if flag != 1:
		for ele in keys['p3']:
			if ele in key1 or ele in key2:
				soundjob2('priority3.wav')
				print "You have a priority3 message"
				print "Sender :",key1
				print "Subject:",key2
				print "Date   :",'%s-%s-%s'%(date[0],date[1],date[2])
				print "Time   :",time
				print "______________________________________________"
				break
	if flag != 1:
		for ele in keys['p4']:
			if ele in key1 or ele in key2:
				soundjob2('priority4.wav')
				print "You have a priority4 message"
				print "Sender :",key1
				print "Subject:",key2
				print "Date   :",'%s-%s-%s'%(date[0],date[1],date[2])
				print "Time   :",time
				print "______________________________________________"
				break
	if flag != 1:
		for ele in keys['p5']:
			if ele in key1 or ele in key2:
				soundjob2('priority5.wav')
				print "You have a priority5 message"
				print "Sender :",key1
				print "Subject:",key2
				print "Date   :",'%s-%s-%s'%(date[0],date[1],date[2])
				print "Time   :",time
				print "______________________________________________"
				break

def soundjob2(path):
	sound = pyglet.media.load(path)
	dumpster = sound.play()

	pyglet.clock.schedule_once(exiter,sound.duration)
	pyglet.app.run()

def exiter(dt):
	pyglet.app.exit()


print 'Welcome to Prioritised Mail Alert!'

print 'Estabilishing connection with the gmail server...'
try:
	conn = imaplib.IMAP4_SSL('imap.gmail.com')
except socket.gaierror:
	print "Make sure you are connected to the internet and please try again!"
	exit()

def check_for_logout():
	stat_file= open('logout.txt','r')
	stat = stat_file.read()
	stat_file.close()
	if 'LOGOUT' in stat or 'logout' in stat or 'Logout' in stat:
		conn.logout()
		cleaner = open('logout.txt','w')
		cleaner.close()
		print "Successfully Signed Out!"
		exit()

def login_process():
	username = raw_input("Enter username:")
	password = getpass.getpass()
	try:
		conn.login(username,password)
	except imaplib.IMAP4_SSL.error:
		print "Wrong Credentials!\nPlease enter USERNAME AND PASSWORD again."
		login_process()

login_process()

os.system('clear')
while True:
	check_for_new_mail()
	#print "looping"
	time.sleep(5) #ten second gap between each execution of check_for_new_mail()
	check_for_logout()
