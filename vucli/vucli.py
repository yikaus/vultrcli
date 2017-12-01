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
try:
  import readline
except ImportError:
  import pyreadline as readline

API_BASE_URL = "https://api.vultr.com/v1/"
REGIONS_AVAILABILITY_URL = ""
PLANS_LIST_URL = "plans/list"
REGIONS_LIST_URL = "regions/list"
OS_LIST_URL = "os/list"
SNAPSHOT_LIST_URL = "snapshot/list?api_key="
SNAPSHOT_CREATE_URL = "snapshot/create?api_key="
SNAPSHOT_DESTROY_URL = "snapshot/destroy?api_key="
SERVER_LIST_URL = "server/list?api_key="
SERVER_REBOOT_URL = "server/reboot?api_key="
SERVER_HALT_URL="server/halt?api_key="
SERVER_START_URL="server/start?api_key="
SERVER_DESTROY_URL="server/destroy?api_key="
SERVER_CREATE_URL="server/create?api_key="
SERVER_REINSTALL_URL="server/reinstall?api_key="
STARTUPSCRIPT_LIST_URL="startupscript/list?api_key="
STARTUPSCRIPT_DESTROY_URL="startupscript/destroy?api_key="
STARTUPSCRIPT_CREATE_URL="startupscript/create?api_key="

SNAPHOST_OS_ID = 164
CUSTOM_OS_ID = 159

ops_by_subid = [SERVER_REBOOT_URL,SERVER_HALT_URL,SERVER_START_URL,SERVER_DESTROY_URL,SERVER_REINSTALL_URL]
ops_by_snapshotid = [SNAPSHOT_DESTROY_URL]
ops_by_scriptid = [STARTUPSCRIPT_DESTROY_URL]

userkey = ""
interactive_mode = False
cmds=['planlist',
     'regionlist',
	 'oslist',
	 'snapshotlist',
	 'snapshotdestroy',
	 'newsnapshot',
	 'serverlist',
	 'reboot',
	 'halt',
	 'start',
	 'destroy',
	 'reinstall',
	 'create',
	 'scriptlist',
	 'scriptdestroy',
	 'newscript',
	 'changekey',
	 'quit',
	 'help']

cmdsneedkey=['serverlist','reboot','halt','start','destroy','reinstall','create',
			'scriptlist','scriptdestroy','newscript','snapshotlist','snapshotdestroy','newsnapshot']
	 
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
	headerline = ["SUBID","os","ram","vcpu","disk","ip","location","DCID","VPSPLANID","Cost","Charge","status"]
	table.append(headerline)
	for k,v in obj.iteritems():
		line =[v["SUBID"],v["os"],v["ram"],v["vcpu_count"],v["disk"],v["main_ip"],v["location"],v["DCID"],v["VPSPLANID"],v["cost_per_month"],v["pending_charges"],v["power_status"]]	
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

def script_print(obj):
	for k,v in obj.iteritems():
		print "%s\t%s" % (v["name"],v["date_modified"])
		print "==========Script Content=================="
		print v["script"]
		print "==========Script Content End=============="
		print 
	print "==========Script lists===================="
	for k,v in obj.iteritems():
		print "%s\t%s\t%s\t%s" % (k,v["name"],v["date_modified"],v["date_modified"])
	print
	
def login():
	global userkey
	if not userkey:
		userkey = raw_input ("please enter your user key :") 

def changekey():
	global userkey 
	userkey = raw_input ("please enter your new user key :")

	
def rest_server_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key
	if operation in ops_by_subid:
		payload = {'SUBID': int(args[0])}
	elif operation in ops_by_scriptid:
		payload = {'SCRIPTID': int(args[0])}
	elif operation in ops_by_snapshotid:
		payload = {'SNAPSHOTID': args[0]}
	response = requests.post(url,data=payload)
	if response.status_code == 200 :
		print "Operation Successful!"
	else :
		print "Operation Failed! with HTTP %s Error!" % response.status_code
		

def rest_snapshot_create_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key
	payload = {'SUBID': int(args[0]),'description':args[1]}
	response = requests.post(url,data=payload)
	try :
		response.json()
		print "Snapshot Created with SNAPSHOTID  "
		printjson(response.json())
	except Exception :
		#not json ,something wrong
		print response.text
		return	
		
		
def rest_script_create_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key
	content = ""
	fname = args[1]
	if not os.path.isfile(fname) :
		print "%s not exists" % fname
		return
	with open (fname, "r") as scriptfile:
		content=scriptfile.read()
	payload = {'name': args[0],'script':content }
	response = requests.post(url,data=payload)
	try :
		response.json()
		print "Start Script Created with SCRIPTID "
		printjson(response.json())
	except Exception :
		#not json ,something wrong
		print response.text
		return
		


def rest_server_create_api(operation,key="",args=[]):
	url = API_BASE_URL + operation + key

	if len(args) == 4 :
		try :
			payload = {'DCID': int(args[0]),'VPSPLANID': int(args[1]),'OSID': int(args[2]),'SCRIPTID':int(args[3])}
		except Exception:
			print "StartScript can not be used with snapshot , only with standard vultr os image!"
			print 
			return
	else:
		#3 args 
		try :
			payload = {'DCID': int(args[0]),'VPSPLANID': int(args[1]),'OSID': int(args[2])}
		except Exception:
			payload = {'DCID': int(args[0]),'VPSPLANID': int(args[1]),'SNAPSHOTID':args[2],'OSID':SNAPHOST_OS_ID}
	
	
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
	elif operation == STARTUPSCRIPT_LIST_URL:
	    script_print(response.json())
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

def snapshot_create(args):
	login()
	rest_snapshot_create_api(SNAPSHOT_CREATE_URL,userkey,args)
	
def snapshot_destroy(args):
	login()
	rest_server_api(SNAPSHOT_DESTROY_URL,userkey,args)
	
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
	
def script_list():
	login()
	rest_list_api(STARTUPSCRIPT_LIST_URL,userkey)	

def script_create(args):
	login()
	rest_script_create_api(STARTUPSCRIPT_CREATE_URL,userkey,args)

def script_destroy(args):
	login()
	rest_server_api(STARTUPSCRIPT_DESTROY_URL,userkey,args)
	
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
    print "Type help to load help page . Or just hit Tab"
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
		'snapshotdestroy':snapshot_destroy,
		'newsnapshot':snapshot_create,
		'serverlist':server_list,
		'reboot':server_reboot,
		'halt':server_halt,
		'start':server_start,
		'create':server_create,
		'reinstall':server_reinstall,
		'destroy':server_destroy,
		'scriptlist':script_list,
		'scriptdestroy':script_destroy,
		'newscript':script_create,
		'changekey':changekey,
		'help':help,
		'quit':sys.exit
	}
	if command not in cmds:
		print 'Invilad command! Press Tab key or use help command list all avaiable command.'
		print ''
	elif command in ['reboot','halt','start','destroy','reinstall','scriptdestroy','snapshotdestroy'] and not args:
		print 'This command need 1 argument!'
		print ''
	elif command in ['create'] and len(args) not in [3,4]:
		print 'Arguments Error: create <DCID> <PLANID> <OSID>|<SNAPSHOTID> [<STARTSCRIPTID>] '
		print '** Startscript can not be used with snapshot'
		print ''
	elif command in ['newscript'] and len(args)<2:
		print 'Arguments Error : newscript <NAME> <SCRIPTPATH>'
		print ''
	elif command in ['newsnapshot'] and len(args)<2:
		print 'Arguments Error : newsnapshot <SUBID> <DESCIRIPTION>'
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
	try :
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
			parser.add_argument('-f', '--file', dest = 'scriptfile',required=False)
			parser.add_argument('-st', '--scriptid', dest = 'scriptid',required=False)
			parser.add_argument('-sn', '--scriptname', dest = 'scriptname',required=False)
			parser.add_argument('-ss', '--snapshotid', dest = 'snapshotid',required=False)
			parser.add_argument('-sd', '--snapshotdesc', dest = 'snapshotdesc',required=False)

			args = parser.parse_args()


		except SystemExit:
			pass
		except  Exception ,e:
			help()
			print e
			
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
		elif args.command in cmdsneedkey:
			print
			print "please provide apikey with -k option"
			print
			sys.exit()
			
		if args.command :
		
			
			if args.command in ['planlist', 'regionlist','oslist','snapshotlist','serverlist','scriptlist']:
				runcmd(args.command,[])
			elif args.command in ['reboot','halt','start','destroy','reinstall']:
				if not args.subid :
					print
					print "Arguments Error , Please add -id <SUBID>"
					print
					sys.exit()
				runcmd(args.command,[args.subid])
			elif args.command in ['newsnapshot']:
				if not args.subid or not args.snapshotdesc:
					print
					print "Arguments Error ,Use vucli newsnapshot -k <USERKEY> -id <SUBID> -sd <DESCIRIPTION>"
					print
					sys.exit()
				runcmd(args.command,[args.subid,args.snapshotdesc])
			elif args.command in ['snapshotdestroy']:
				if not args.snapshotid :
					print
					print "Arguments Error ,Use vucli snapshotdestroy -k <USERKEY> -ss <SNAPSHOTID>"
					print
					sys.exit()
				runcmd(args.command,[args.snapshotid])
			elif args.command in ['newscript']:
				if not args.scriptname or not args.scriptfile:
					print
					print "Arguments Error ,Use vucli newscript -k <USERKEY> -sn <SCRIPTNAME> -f <SCRIPTPATH>"
					print
					sys.exit()
				runcmd(args.command,[args.scriptname,args.scriptfile])
			elif args.command in ['scriptdestroy']:
				if not args.scriptid :
					print
					print "Arguments Error ,Use vucli scriptdestroy -k <USERKEY> -st <SCRIPTID>"
					print
					sys.exit()
				runcmd(args.command,[args.scriptid])
			elif args.command in ['create']:
				if not args.dcid or not args.planid or not (args.osid or args.snapshotid) or (args.osid and args.snapshotid): 
					print
					print "Arguments Error ,Use vucli create -d <DCID> -p <PLANID> -os <OSID>|-ss <SNAPSHOTID> [-st <SCRIPTID>]"
					print
					print "Can only choose <OSID> or <SNAPSHOTID> at one time"
					print '** Startscript can not be used with snapshot'
					print
					sys.exit()
				createarg = []	
				if args.osid :
					createarg=[args.dcid,args.planid,args.osid]
				elif args.snapshotid:
					createarg=[args.dcid,args.planid,args.snapshotid]
				
				if args.scriptid :
					createarg.append(args.scriptid)
				
				
				runcmd(args.command,createarg)
		else:
			interactive()
	except (KeyboardInterrupt,EOFError) as e:
		print
		sys.exit(0)
	


def help():
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
	print "     newsnapshot       create a snapshot with subid"
	print "     snapshotdestroy   delete a snapshot"
	print "     serverlist        list all servers"
	print "     reboot            restart server by server id"
	print "     halt              hard stop server by server id"
	print "     start             start server by server id"
	print "     destroy           destroy server by server id"
	print "     reinstall         reinstall server by server id"
	print "     create            create new server "
	print "     scriptlist        list all start script"
	print "     scriptdestroy     delete particular start script"
	print "     newscript         create new server "
	print "     create            create start script "
	print "     changekey         reset API key (only worked in interactive mode)"
	print "     quit              quit interactive mode (only worked in interactive mode)"
	
	if not interactive_mode :
		print "Options:"
		print "     -k  <APIKEY>      provide API key"
		print "     -id <SUBID>       provide server id"
		print "     -d  <DCID>        provide datacenter DCID"
		print "     -p  <PLANID>      provide PLANID"
		print "     -os <OSID>        provide OS image ID"
		print "     -f <SCRIPTPATH>   provide script file path"
		print "     -st <SCRIPTID>    provide script id"
		print "     -sn <SCRIPTNAME>  provide script name"
		print "     -ss <SUBID>       provide server id to create a snapshot"
		print "     -sd <SNAPDESC>    provide snapshot description"
		print
		
		print "Examples:"
		
		print "  create instance with OSID 128 at DCID 5 and planid 29 ,script id 245"
		print "      vucli create -k <yourkey> -d 5 -p 29 -os 128 -st 245"
		print
		print "  create instance with SNAPSHOTID 53bdd6e0d6414 at DCID 5 and planid 29"
		print "      vucli create -k <yourkey> -d 5 -p 29 -ss 53bdd6e0d6414"
		print
	

if __name__ == "__main__":
	main()


