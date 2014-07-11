#!/usr/bin/env python

'''

vucli.py
==========

Desc: vultr cli 


Author: Kevin Yi<yikaus @ gmail>

License  : BSD 

'''

import requests
import sys
import os
import argparse
#import simplejson as json
import readline

API_BASE_URL = "https://api.vultr.com/v1/"
REGIONS_AVAILABILITY_URL = ""
PLANS_LIST_URL = "plans/list"
REGIONS_LIST_URL = "regions/list"
OS_LIST_URL = "os/list"
SNAPSHOT_LIST_URL = "snapshot/list?api_key="
SERVER_LIST_URL = "server/list?api_key="
SERVER_REBOOT_URL = "server/reboot?api_key="
SERVER_HALT_URL="server/halt?api_key="
SERVER_START_URL="server/start?api_key="
SERVER_DESTROY_URL="server/destroy?api_key="
SERVER_CREATE_URL="server/create?api_key="
SERVER_REINSTALL_URL="server/reinstall?api_key="

userkey = ""
interactive_mode = False
cmds=['planlist', 'regionlist','oslist','snapshotlist','serverlist','reboot','halt','start','destroy','reinstall','create','changekey','quit','help']

'''
def printjson(obj): 
    res = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    print res
'''
	
def jsontotable(obj): 

	table =[]
	header = True
	for k,v in obj.iteritems():
		line = []
		headerline = []
		for key, value in v.iteritems():
			if header :
				headerline.append(str(key))
			line.append(str(value))
		if header :
			table.append(headerline)
		table.append(line)
		header = False
	return table

def serverjsontotable(obj): 

	table =[]
	headerline = ["SUBID","os","ram","vcpu","disk","ip","location","DCID","VPSPLANID","Cost","status"]
	table.append(headerline)
	for k,v in obj.iteritems():
		line =[v["SUBID"],v["os"],v["ram"],v["vcpu_count"],v["disk"],v["main_ip"],v["location"],v["DCID"],v["VPSPLANID"],v["cost_per_month"],v["power_status"]]	
		table.append(line)
	return table

# there is minor issue with oslist api OSID is null , so this is little ugly tweak for it 
def osjsontotable(obj): 
	table =[]
	headerline = ["OSID","arch","name","family"]
	table.append(headerline)
	for k,v in obj.iteritems():
		line =[k,v["arch"],v["name"],v["family"]]	
		table.append(line)
	return table
	
#locale.setlocale(locale.LC_NUMERIC, "")
def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    #try:
    #    inum = int(num)
    #    return locale.format("%.*f", (0, inum), True)

    #except (ValueError, TypeError):
    return str(num)
	
def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    return max([len(format_num(row[index])) for row in table])

def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """
    col_paddings = []
	
	
    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out		
	
	
def login():
	global userkey
	if not userkey:
		userkey = raw_input ("please enter your user key :") 

def changekey():
	global userkey 
	userkey = raw_input ("please enter your new user key :")
		
def rest_server_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key
	payload = {'SUBID': int(args[0])}
	response = requests.post(url,data=payload)
	if response.status_code == 200 :
		print "Operation Successful!"
	else :
		print "Operation Failed! with HTTP %s Error!" % response.status_code

def rest_server_create_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key
	payload = {'DCID': int(args[0]),'VPSPLANID': int(args[1]),'OSID': int(args[2])}
	response = requests.post(url,data=payload)
	try :
		response.json()
		print "Server Created with SUBID "
		printjson(response.json())
	except Exception :
		#not json ,something wrong
		print response.text
		return
		
def rest_list_api(operation,key=""):
	url = API_BASE_URL + operation + key
	response = requests.get(url)
	try :
		response.json()
	except Exception :
		#not json ,something wrong
		print response.text
		return
	
	if not response.json():
		#result is empty
		print "Result is None!"
		return
	out = sys.stdout
	if operation == SERVER_LIST_URL:
		pprint_table(out,serverjsontotable(response.json()))
	elif operation == OS_LIST_URL:
		pprint_table(out,osjsontotable(response.json()))
	else:
		pprint_table(out,jsontotable(response.json()))
	
		
def plans_list():
	rest_list_api(PLANS_LIST_URL)
	
def regions_list():
	rest_list_api(REGIONS_LIST_URL)

def os_list():
	rest_list_api(OS_LIST_URL)

def snapshot_list():
	login()
	rest_list_api(SNAPSHOT_LIST_URL,userkey)

def server_list():
	login()
	rest_list_api(SERVER_LIST_URL,userkey)

def server_reboot(args):
	login()
	rest_server_api(SERVER_REBOOT_URL,userkey,args)
	
def server_halt(args):
	login()
	rest_server_api(SERVER_HALT_URL,userkey,args)

def server_start(args):
	login()
	rest_server_api(SERVER_START_URL,userkey,args)	

def server_destroy(args):
	login()
	rest_server_api(SERVER_DESTROY_URL,userkey,args)

def server_reinstall(args):
	login()
	rest_server_api(SERVER_REINSTALL_URL,userkey,args)	

def server_create(args):
	login()
	rest_server_create_api(SERVER_CREATE_URL,userkey,args)	
	
def interactive():
    global interactive_mode
    interactive_mode =True
    print ""
    print "##########################"
    print "#     Vultr Cloud CLI    #"
    print "#                        #"
    print "#            v1          #"
    print "#                        #"
    print "##########################"
    print ""
    print "Type help to load help page ."
    print ""
	
    command =''
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
	
    while True :
		i_input = raw_input ('vultr_cli>>')
		if not i_input : continue
		command = i_input.split()[0]
		args=i_input.split()[1:]
		runcmd(command,args)
    print "Bye"


	
def complete(text, state):
    for cmd in cmds:
		if cmd.startswith(text):
		    if not state:
			return cmd
		    else:
			state -= 1
			
def runcmd(command,args):
	
	cmddict={'planlist':plans_list,
		'regionlist':regions_list,
		'oslist':os_list,
		'snapshotlist':snapshot_list,
		'serverlist':server_list,
		'reboot':server_reboot,
		'halt':server_halt,
		'start':server_start,
		'create':server_create,
		'reinstall':server_reinstall,
		'destroy':server_destroy,
		'changekey':changekey,
		'help':help,
		'quit':sys.exit
	}
	if command not in cmds:
		print 'Invilad command! Press Tab key or use help command list all avaiable command.'
		print ''
	elif command in ['reboot','halt','start','destroy','reinstall'] and not args:
		print 'This command need argument!'
		print ''
	elif command in ['create'] and len(args)<3:
		print 'missing arguments : create <DCID> <PLANID> <OSID>'
		print ''
	else:
		if not args :
			cmddict[command]()
		else:
			cmddict[command](args)
		
class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise Exception(message)
		
def main():
	#print "----"
	args = None
	try:
		parser = MyArgumentParser(prog='vucli',add_help=False)
		parser.add_argument('-h', action='store_true', dest='help')
		parser.add_argument('command', nargs='?', choices=cmds,)
		parser.add_argument('-k', '--key', dest = 'userkey' ,required=False)
		parser.add_argument('-id', '--subid', dest = 'subid',required=False)
		parser.add_argument('-d', '--dc', dest = 'dcid',required=False)
		parser.add_argument('-p', '--plan', dest = 'planid',required=False)
		parser.add_argument('-os', '--os', dest = 'osid',required=False)

		args = parser.parse_args()


	except SystemExit:
		pass
	except  Exception ,e:
		help()
		'''
		parser.print_help()

		print
		print "Arguments Error"
		print "---------------"
		print e
		print
		'''
		sys.exit()

	if args.help:
		help()
		sys.exit()
	if not args :  
		# interactive mode
		interactive()
		
	if args.userkey :
		global userkey 
		userkey = args.userkey
	elif args.command in ['snapshotlist','serverlist','reboot','halt','start','destroy','reinstall','create']:
		print
		print "please provide apikey with -k option"
		print
		sys.exit()
		
	if args.command :
	
		
		if args.command in ['planlist', 'regionlist','oslist','snapshotlist','serverlist']:
			runcmd(args.command,[])
		elif args.command in ['reboot','halt','start','destroy','reinstall']:
			if not args.subid :
				print
				print "please provide subid with -id option"
				print
				sys.exit()
			runcmd(args.command,[args.subid])
		elif args.command in ['create']:
			if not args.dcid and not args.osid and not args.planid : 
				print
				print "To create server , please also provide dcid with -d option , planid with -p option and osid with -os option"
				print
				sys.exit()
			runcmd(args.command,[args.dcid,args.planid,args.osid])
	else:
		interactive()


def help():
#'planlist', 'regionlist','oslist','snapshotlist','serverlist','reboot','halt','start','destroy','reinstall','create','changekey','quit'
	print
	print "Interactive Usage : vucli"
	print
	print "Usage: vucli <command> [options] "
	print 
	print "Commands:"
	print "     planlist          list all VPS plans"
	print "     regionlist        list all available regions"
	print "     oslist            list all operating system images"
	print "     snapshotlist      list all snapshots"
	print "     serverlist        list all servers"
	print "     reboot            restart server by server id"
	print "     halt              hard stop server by server id"
	print "     start             start server by server id"
	print "     destroy           destroy server by server id"
	print "     reinstall         reinstall server by server id"
	print "     create            create new server "
	print "     changekey         reset API key (only worked in interactive mode)"
	print "     quit              quit interactive mode (only worked in interactive mode)"
	
	if not interactive_mode :
		print "Options:"
		print "     -k  <APIKEY>      provide API key"
		print "     -id <SUBID>       provide server id"
		print "     -d  <DCID>        provide datacenter DCID"
		print "     -p  <PLANID>      provide PLANID"
		print "     -os <OSID>        provide OS image ID"
		print
	

if __name__ == "__main__":
	try :
		main()
	except (KeyboardInterrupt,EOFError) as e:
		print
		sys.exit(0)

