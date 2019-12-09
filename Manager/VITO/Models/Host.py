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

class Host:

    def __init__(self,name,template,memory,cpu):
        self.ip = None
        self.manager_ip = "172.12.0.10"
        self.name = name
        self.template = template
        self.interfaces = []
        self.commands = []
        self.virbr_mac = ""
        self.memory = memory
        self.cpu = cpu
        self.vito_client = False
        
    def add_interface(self,interface):
        self.interfaces.append(interface)
    
    def add_command(self,command):
        self.commands.append(command)

    def __str__(self):
        val = "%s (%s)\nInterfaces: \n"%(self.name,self.template)
        for interface in self.interfaces:
            val += str(interface)
            val += "\n"
        val += "Commands:\n"
        for command in self.commands:
            val += str(command)
            val += "\n"
        return val