#!/bin/bash
export PATH=/home/user/whoer_i2p
cd $PATH
# Запуск сценария для обновления базы данных и анализа IP-адресов
/usr/bin/python3 updateNetDb.py
/usr/bin/python3 netDb/reader.py tmp/netDb/
/usr/bin/python3 IPsParser.py tmp/netDb/
/usr/bin/python3 leaseSets/leaseSetsGrabber.py;/usr/bin/python3 update_leasesets.py
/usr/bin/python3 draw.py; 

/usr/bin/scp -P 25 ip_port_database.db user@192.168.0.194:/home/user/whoer_i2p;/usr/bin/scp -P 25 static/world_map.png user@192.168.0.194:/home/user/whoer_i2p/static
