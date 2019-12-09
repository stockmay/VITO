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
from Models.Command import Command
import os
import random 
import time

class  VM_Creator:
    def random_mac(self):
        mac = [ 0x52, 0x54, 0x00,
                random.randint(0x00, 0x7f),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def execute(self,command):
        #os.system("ssh root@%s %s"%(command))
        print("ssh root@%s %s"%(self.hostname,command))
        os.system("ssh root@%s %s"%(self.hostname,command))
        time.sleep(1)

    def __init__(self,hostname):
        self.hostname = hostname

    def create_vm(self, host):
        template = host.template
        vm_name = host.name
        print("Creating %s"%(host.name))
        new_mac = self.random_mac()
        host.virbr_mac = new_mac
        self.execute("qemu-img create -f qcow2 -b /usr/testbed/%s.qcow2 /usr/testbed/%s.qcow2"%(template,vm_name))
        self.execute("virt-clone --original %s --name %s --file=/usr/testbed/%s.qcow2 --mac=%s --preserve-data"%(template,vm_name,vm_name,new_mac))
        self.execute("virsh setvcpus %s %s --config"%(vm_name,host.cpu))
        self.execute("virsh setmaxmem %s %sG --config"%(vm_name,host.memory))
        self.execute("virsh setmem %s %sG --config"%(vm_name,host.memory))
        for interface in host.interfaces:
            self.add_interface_to_vm(vm_name,interface)
        self.execute("virsh start %s"%(vm_name))

    def add_interface_to_vm(self, vm_name,interface):
        mac = interface.mac
        bridge = interface.bridge
        self.execute("ip l add name %s type bridge"%(bridge))
        self.execute("ip l s %s up"%(bridge))
        self.execute("virsh attach-interface --domain %s --type bridge --source %s --model e1000 --mac %s --config"%(vm_name,bridge,mac))
    

    def destroy_vm(self,host):
        self.execute("virsh destroy %s"%(host.name))
        for interface in host.interfaces:
            self.execute("ip l s %s down"%(interface.bridge))
            self.execute("ip l del name %s"%(interface.bridge))
        self.execute("virsh undefine %s"%(host.name))
        self.execute("rm -f /usr/testbed/%s.qcow2"%(host.name))



