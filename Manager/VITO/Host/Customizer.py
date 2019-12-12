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
from Models.Host import Host
from Models.Interface import Interface
from Host.Executor import Executor
import os

class Customizer:

    def execute_command(self,host,command,*argument):
        #os.system("ssh root@$(sudo virsh net-dhcp-leases default | grep %s | cut -d ' ' -f16 | cut -d '/' -f 1) %s"%(host.virbr_mac,command))
        if host.ip is None:
            print("ssh root@%s virsh net-dhcp-leases vito | grep %s | cut -d ' ' -f16"%(self.hostname,host.virbr_mac))
            ip = os.popen("ssh root@%s virsh net-dhcp-leases vito | grep %s"%(self.hostname,host.virbr_mac)).read().strip()
            for part in ip.split(" "):
                if "172.12" in part:
                    host.ip = part.split("/")[0]
        if host.manager_ip is None:
            print("ssh root@%s virsh net-dhcp-leases vito | grep %s | cut -d ' ' -f16"%(self.hostname,'manager'))
            ip = os.popen("ssh root@%s virsh net-dhcp-leases vito | grep %s | cut -d ' ' -f16"%(self.hostname,'manager')).read().strip()
            for part in ip.split(" "):
                if "172.12" in part:
                    host.manager_ip = part.split("/")[0]
        if not host.vito_client:
            print("scp /VITO/Client/vito_client.py root@%s:/usr/local/bin/vito_client "%(host.ip))
            os.system("scp /VITO/Client/vito_client.py root@%s:/usr/local/bin/vito_client "%(host.ip))
            print("ssh root@%s chmod +x /usr/local/bin/vito_client"%(host.ip))
            os.system("ssh root@%s chmod +x /usr/local/bin/vito_client"%(host.ip))
            host.vito_client = True
        print("ssh root@%s vito_client %s %s"%(host.ip,command,' '.join(map(lambda x : str(x),argument))))
        os.system("ssh root@%s vito_client %s %s"%(host.ip,command,' '.join(map(lambda x : str(x),argument))))

    def __init__(self,hostname):
        self.hostname = hostname

    def setup_host(self,host):
        print("Setting up %s"%(host.name.replace("_",'')))
        self.execute_command(host,"hostname",host.name.replace("_",""))
        self.execute_command(host,"firewall")
        #NFS Mount problematic with docker
        #self.execute_command(host,"mount",host.manager_ip)
        for interface in host.interfaces:
            self.execute_command(host,"interface_name",interface.mac,interface.name)
            self.execute_command(host,"interface_properties",interface.name,interface.mtu,interface.bandwidth,interface.delay,interface.jitter,interface.loss)
            self.execute_command(host,'address',interface.name, interface.ip)
            for dest,via in interface.routes.items():
                print("Route to %s via %s at interface %s"%(dest,via,interface.name))
                self.execute_command(host,"add_route",interface.name,dest,via)


    def finish_host(self,host):
        self.execute_command(host,"finish")
        print("scp root@%s:/mnt/host.tar.bz2 /mnt/vito/%s.tar.bz2 "%(host.ip,host.name))
        os.system("scp root@%s:/mnt/host.tar.bz2 /mnt/vito/%s.tar.bz2 "%(host.ip,host.name))

