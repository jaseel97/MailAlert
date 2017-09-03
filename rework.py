#!/usr/bin/env python

import os
import imaplib
import socket
import getpass

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

	login_count = 4
	login_func(connection_object,login_count)

def login_func(connection_object,login_count):
	username = raw_input("Enter E-Mail ID : ")
	password = getpass.getpass()

	try:
		connection_object.login(username,password)
		print 'Logged In Successfully!'
		connection_object.logout()		
	except imaplib.IMAP4_SSL.error:
		login_count = login_count - 1
		print 'Invalid Credentials! Login Attempts Left:',login_count
		print 'Enter login details again!'
		login_func(connection_object,login_count)



if __name__ == '__main__':
	main()