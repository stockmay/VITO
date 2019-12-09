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
import json
import sys
import random
sys.path.append("..")
from Models.Host import Host
from Models.Command import Command
from Models.Interface import Interface
from Models.Testbed import Testbed

class Parser:

    def __init__(self,file_name):
        self.file_name = file_name
        with open(file_name) as f:
            self.json = json.load(f)

    def random_mac(self):
        mac = [ 0x00, 0x01, 0x00,
                random.randint(0x00, 0x7f),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def try_value(self,dictionary,key,default_val=""):
        if key in dictionary:
            return dictionary[key]
        else:
            return default_val

    def get_testbed_config(self):
        name = self.json['Name']
        hosts = self.json['Hosts']
        t = Testbed(name)
        for host in hosts:
            host_name = host['Name'].replace(" ","_")
            host_template = host['Template']
            host_memory = host['Memory']
            host_cpu = host['CPU']
            h = Host(host_name,host_template,host_memory,host_cpu)
            if 'Interfaces' in host:
                for interface in host['Interfaces']:
                    interface_name = interface['Name']
                    interface_bridge = interface['Bridge']
                    interface_mac = self.try_value(interface,'Mac',self.random_mac())
                    interface_ip = self.try_value(interface,'IP',"")
                    interface_mtu = self.try_value(interface,'MTU',1500)
                    interface_bw = self.try_value(interface,'Bandwidth',-1)
                    interface_delay = self.try_value(interface,'Delay',-1)
                    interface_jitter = self.try_value(interface,'Jitter',-1)
                    interface_loss = self.try_value(interface,'Loss',-1)
                    interface_tcpdump = self.try_value(interface,'Tcpdump','no')
                    routes = dict()
                    if 'Routes' in interface:
                        for route in interface['Routes']:
                            for destination in route.keys():
                                routes[destination] = route[destination]
                    i = Interface(interface_name,interface_bridge,interface_mac,interface_mtu,interface_ip,interface_bw,interface_delay,interface_jitter,interface_loss,interface_tcpdump,routes)
                    h.add_interface(i)
            if 'Commands' in host:
                for command in host['Commands']:
                    command_command = command['Command']
                    command_time = command['Time']
                    command_background = command['Background']
                    command_repeat = self.try_value(command,'RepeatUntil',0)
                    c = Command(command_command,command_time,command_background,command_repeat)
                    h.add_command(c)
            t.add_host(h)
        return t
 
