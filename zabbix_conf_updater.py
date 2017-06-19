#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import mysql.connector
import argparse

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('-h', '--hostname', help='hostname to push config (local)', required=True)
parser.add_argument('-u', '--user', help='user (local)', required=True)
parser.add_argument('-p','--password', help='password (local)', required=True)
parser.add_argument('-d','--database', help='db name (local)', required=False,default='zabbix')
parser.add_argument('-rh', '--remotehostname', help='hostname to pull config (remote)', required=True)
parser.add_argument('-ru', '--remoteuser', help='user (remote)', required=True)
parser.add_argument('-rp','--remotepassword', help='password (remote)', required=True)
parser.add_argument('-rd','--remotedatabase', help='db name (remote)', required=False,default='zabbix')
args = parser.parse_args()

conn = mysql.connector.connect(user=args.user, password=args.password, host=args.hostname, database=args.database, charset='utf8')
cur = conn.cursor()

MYSQL_CONN = "-h " + args.hostname + " -u" + args.user + " -p" + args.password + " " + args.database
MYSQL_REMOTE_CONN = "-h " + args.remotehostname + " -u" + args.remoteuser + " -p" + args.remotepassword + " " + args.remotedatabase

date = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')

DUMPFILE = "/opt/zabbixdb_dumps/zabbixdb_dump_" + date + ".sql"
BACKUPFILE = "/opt/zabbixdb_dumps/zabbixdb_backup_" + date + ".sql"

tables = 'actions,application_discovery,application_prototype,application_template,applications,autoreg_host,conditions,config,corr_condition,corr_condition_group,corr_condition_tag,corr_condition_tagpair,corr_condition_tagvalue,corr_operation,correlation,dbversion,dchecks,dhosts,drules,dservices,escalations,event_recovery,event_tag,expressions,functions,globalmacro,globalvars,graph_discovery,graph_theme,graphs,graphs_items,group_discovery,group_prototype,groups,host_discovery,host_inventory,hostmacro,hosts,hosts_groups,hosts_templates,housekeeper,httpstep,httpstepitem,httptest,httptestitem,icon_map,icon_mapping,ids,images,interface,interface_discovery,item_application_prototype,item_condition,item_discovery,items,items_applications,maintenances,maintenances_groups,maintenances_hosts,maintenances_windows,mappings,media,media_type,opcommand,opcommand_grp,opcommand_hst,opconditions,operations,opgroup,opinventory,opmessage,opmessage_grp,opmessage_usr,optemplate,problem,problem_tag,profiles,proxy_autoreg_host,proxy_dhistory,proxy_history,regexps,rights,screen_user,screen_usrgrp,screens,screens_items,scripts,services,services_links,services_times,sessions,slides,slideshow_user,slideshow_usrgrp,slideshows,sysmap_element_url,sysmap_url,sysmap_user,sysmap_usrgrp,sysmaps,sysmaps_elements,sysmaps_link_triggers,sysmaps_links,task,task_close_problem,timeperiods,trigger_depends,trigger_discovery,trigger_tag,triggers,users,users_groups,usrgrp,valuemaps'

dumpcmd = 'mysqldump --routines --opt --single-transaction --skip-lock-tables --extended-insert=FALSE ' + MYSQL_REMOTE_CONN + ' --tables ' + tables.replace(',', ' ') + ' >> ' + DUMPFILE
backcmd = 'mysqldump --routines --opt --single-transaction --skip-lock-tables --extended-insert=FALSE ' + MYSQL_CONN + ' --tables ' + tables.replace(',', ' ') + ' >> ' + BACKUPFILE

os.system(dumpcmd)
os.system(backcmd)

cur.execute('set foreign_key_checks=0;')
cur.execute('drop table if exists ' + tables + ' cascade;')
os.system('mysql ' + MYSQL_CONN + ' < ' + DUMPFILE)
cur.execute('update media_type set status=1;')
cur.execute('set foreign_key_checks=1;')

os.system('gzip ' + DUMPFILE)
os.system('gzip ' + BACKUPFILE)

os.system('find /opt/zabbixdb_dumps/ -name "*.sql.gz" -type f -mtime +60 -delete')
