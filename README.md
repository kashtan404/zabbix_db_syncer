zabbix_db_syncer
=========

This script can be used copy zabbix database configuration to other zabbix database.
Beware! History and trends tables are not synced.

Requirements
------------

Zabbix 3.0 or higher

Python 3 or higher

python libs:
  - os
  - datetime
  - mysql.connector
  - argparse

Directory /opt/zabbixdb_dumps/ must exist.


Usage
------

./zabbix_conf_updater.py -h "host" -u "user" -p "pass" -d "dbname" -rh "remotehost" -ru "remoteuser" -rp "remotepass" -rd "remotedbname"


Script work-line
----------------

1) Dump master DB
2) Backup slave DB (history and trends will not saved)
3) Drop slave tables
4) Disable all media_type on slave
5) gzip dump and backup (/opt/zabbixdb_dumps/)
6) Delete all dumps and backups older than 60 days

License
-------

MIT

Author Information
------------------

Aleksey Demidov