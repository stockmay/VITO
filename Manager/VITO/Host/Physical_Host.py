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
from Host.VM_Creator import VM_Creator
from Host.Customizer import Customizer
from Host.Executor import Executor
import threading
import time
import os

class Physical_Host:

    def __init__(self,hostname):
        self.hostname = hostname
        self.vm_creator = VM_Creator(self.hostname)
        self.customizer = Customizer(self.hostname)

    def tool_exists(self,tool,packet):
        val = os.popen("ssh root@%s which %s 2>&1"%(self.hostname,tool)).read()
        if "which:" in val or "$PATH" in val:
            print("Error %s missing on Host %s"%(packet,self.hostname))

    def check_host(self):
        self.tool_exists("qemu-img","Qemu")
        self.tool_exists("virsh","libvirt")
        self.tool_exists("virt-clone","Virt-Manager")

    def execute_experiment(self,testbed):
        print("Executing %s"%(testbed))
        for host in testbed.hosts:
            self.vm_creator.create_vm(host)
        time.sleep(10)
        for host in testbed.hosts:
            self.customizer.setup_host(host)
        threads = []
        for host in testbed.hosts:
            e = Executor(host.ip)
            for command in host.commands:
                e.add_command_to_queue(command.command,command.time,command.background)
            threads.append(e.start_experiment())
        for thread in threads:
            thread.join()
        for host in testbed.hosts:
            self.customizer.finish_host(host)
            self.vm_creator.destroy_vm(host)
        



            

