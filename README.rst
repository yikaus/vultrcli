vucli 0.0.2 (Vultr cloud server CLI tool)
======================

vucli is a CLI tool to manage Vultr VPS 
vucli invoked Vultr public REST service , see details https://www.vultr.com/api/

.. contents::

Changes
-------

**0.0.1**: Initial drop

**0.0.2**: Add start script & snapshot management ,  create server with startscript or snapshot ,showing current_charge in serverlist

Requirements
-------------

1. Python 2.6 +
2. python requests and argparse package if you want to directly run


Direct RUN
-------------
git clone https://github.com/yikaus/vultrcli
cd vultrcli/vucli
chmod +x vucli.py
./vucli.py


Installation (all dependency will be installed)
------------

$sudo pip install vucli

$vucli

To Use
------------

Interactive mode
------------

vucli

OR

./vucli.py

##########################
#     Vultr Cloud CLI    #
#                        #
#            v1          #
#                        #
##########################

Type help to load help page .

vultr_cli>>help

Interactive Usage : vucli

Usage: vucli <command> [options]

Commands:
     planlist          list all VPS plans
     regionlist        list all available regions
     oslist            list all operating system images
     snapshotlist      list all snapshots
     newsnapshot       create a snapshot with subid
     snapshotdestroy   delete a snapshot
     serverlist        list all servers
     reboot            restart server by server id
     halt              hard stop server by server id
     start             start server by server id
     destroy           destroy server by server id
     reinstall         reinstall server by server id
     create            create new server
     scriptlist        list all start script
     scriptdestroy     delete particular start script
     newscript         create new server
     create            create start script
     changekey         reset API key (only worked in interactive mode)
     quit              quit interactive mode (only worked in interactive mode)
	 
vultr_cli>>
vultr_cli>>regionlist
country    state   DCID          name       continent
FR                   24        France          Europe
JP                   25         Tokyo            Asia
AU                   19     Australia       Australia
US            NJ      1    New Jersey   North America
US            TX      3        Dallas   North America
...
...

vultr_cli>>oslist
OSID    arch                      name     family
151     i386   Debian 6 i386 (squeeze)     debian
147     i386             CentOS 6 i386     centos
138      x64    Debian 6 x64 (squeeze)     debian
140      x64            FreeBSD 10 x64    freebsd
...
...

vultr_cli>>serverlist
please enter your user key :xxxxxxxxxxxxxxxxx
SUBID                    os      ram   vcpu            disk              ip      location   DCID   VPSPLANID   Cost    status
1371543    Ubuntu 12.04 x64   768 MB      1   Virtual 15 GB   xxx.xx.xx.xxx   Los Angeles      5          29   5.00   running

vultr_cli>>halt 1371543
Operation Successful!
vultr_cli>>serverlist
SUBID                    os      ram   vcpu            disk              ip      location   DCID   VPSPLANID   Cost    status
1371543    Ubuntu 12.04 x64   768 MB      1   Virtual 15 GB   xxx.xx.xx.xxx   Los Angeles      5          29   5.00   stopped
vultr_cli>>start 1371543
Operation Successful!
vultr_cli>>serverlist
SUBID                    os      ram   vcpu            disk              ip      location   DCID   VPSPLANID   Cost    status
1371543    Ubuntu 12.04 x64   768 MB      1   Virtual 15 GB   xxx.xx.xx.xxx   Los Angeles      5          29   5.00   running

Command mode
------------

./vucli.py -h

Interactive Usage : vucli

Usage: vucli <command> [options]

Commands:
     planlist          list all VPS plans
     regionlist        list all available regions
     oslist            list all operating system images
     snapshotlist      list all snapshots
     newsnapshot       create a snapshot with subid
     snapshotdestroy   delete a snapshot
     serverlist        list all servers
     reboot            restart server by server id
     halt              hard stop server by server id
     start             start server by server id
     destroy           destroy server by server id
     reinstall         reinstall server by server id
     create            create new server
     scriptlist        list all start script
     scriptdestroy     delete particular start script
     newscript         create new server
     create            create start script
     changekey         reset API key (only worked in interactive mode)
     quit              quit interactive mode (only worked in interactive mode)
Options:
     -k  <APIKEY>      provide API key
     -id <SUBID>       provide server id
     -d  <DCID>        provide datacenter DCID
     -p  <PLANID>      provide PLANID
     -os <OSID>        provide OS image ID
     -f <SCRIPTPATH>   provide script file path
     -st <SCRIPTID>    provide script id
     -sn <SCRIPTNAME>  provide script name
     -ss <SUBID>       provide server id to create a snapshot
     -sd <SNAPDESC>    provide snapshot description

Examples:
  create instance with OSID 128 at DCID 5 and planid 29 ,script id 245
      vucli create -k <yourkey> -d 5 -p 29 -os 128 -st 245

  create instance with SNAPSHOTID 53bdd6e0d6414 at DCID 5 and planid 29
      vucli create -k <yourkey> -d 5 -p 29 -ss 53bdd6e0d6414
      provide OS image ID


Usage example:	  
	 
./vucli.py oslist

OSID    arch                      name     family
151     i386   Debian 6 i386 (squeeze)     debian
147     i386             CentOS 6 i386     centos
138      x64    Debian 6 x64 (squeeze)     debian
.....

./vucli.py create -k <yourkey> -d 5 -os 128 -p 29
Server Created with SUBID
{"SUBID":"1371543"}

./vucli.py serverlist -k <yourkey>
SUBID                    os      ram   vcpu            disk              ip      location   DCID   VPSPLANID   Cost    status
1371543    Ubuntu 12.04 x64   768 MB      1   Virtual 15 GB   xxx.xx.xx.xxx   Los Angeles      5          29   5.00   running

./vucli.py reboot -k <yourkey> -id 1371543
Operation Successful!
