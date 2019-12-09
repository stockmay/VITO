#!/usr/bin/python3
#
# Copyright (c) 2019 Andreas Stockmayer.
#
# This file is part of VITO 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys

def change_hostname(name):
    os.system("hostname %s"%(name))

def change_interface_name(mac,name):
    old_name = os.popen("ip -o link | awk '$2 != \"lo:\" {print $2, $(NF-2)}' | grep %s | cut -d \":\" -f1"%(mac)).read().strip()
    os.system("ip l s %s down"%(old_name))
    os.system("ip l s dev %s name %s"%(old_name,name))
    os.system("ip l s dev %s up"%(name))

def change_interface_properties(name,mtu,bandwidth,delay=1,jitter=0,loss=0):
    if float(delay) < 0:
        delay = 1
    if float(jitter) < 0:
        jitter = 0
    if float(loss) < 0:
        loss = 0
    os.system("ip l s %s down"%(name))
    os.system("ip l s dev %s mtu %s"%(name,mtu))
    os.system("tc qdisc del dev %s root"%(name))
    os.system("tc qdisc add dev %s handle 1: root netem delay %sms %sms loss %s"%(name,delay,jitter,float(loss)/100.0))
    os.system("tc qdisc add dev %s parent 1: handle 2: tbf rate %skbit buffer 10000 limit 10000"%(name,float(bandwidth)*1000.0))

def add_route(interface,route,via):
    os.system("ip r add %s via %s dev %s"%(route,via,interface))

def mount_nfs(manager):
    os.system("mount -t nfs -o soft %s:/mnt/vito /mnt"%(manager))

def add_address(name,ip):
    os.system("ip a a %s dev %s"%(ip,name))

def finish():
    os.system("tar cvjf /mnt/host.tar.bz2 /root/*")

def firewall():
    os.system("iptables -i eth0 -I INPUT -s 172.12.0.0/23 -j ACCEPT")
    os.system("iptables -i eth0 -I OUTPUT -d 172.12.0.0/23 -j ACCEPT")
    os.system("iptables -i eth0 -P INPUT -j DROP")
    os.system("iptables -i eth0 -P OUTPUT -j DRWOP")    

def main():
    function = sys.argv[1]
    if function == 'hostname':
        change_hostname(sys.argv[2])
    elif function == 'interface_name':
        change_interface_name(sys.argv[2],sys.argv[3])
    elif function == 'interface_properties':
        change_interface_properties(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    elif function == 'add_route':
        add_route(sys.argv[2],sys.argv[3],sys.argv[4])
    elif function == 'mount':
        mount_nfs(sys.argv[2])
    elif function == 'address':
        add_address(sys.argv[2],sys.argv[3])
    elif function == 'finish':
        finish()
    elif function == 'firewall':
        firewall()
        
if __name__ == "__main__":
    main()
