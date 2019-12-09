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
from Auxilliary.Parser import Parser
from Models.Host import Host
from Models.Command import Command
from Models.Interface import Interface
from Models.Testbed import Testbed
from Host.Physical_Host import Physical_Host
import os


###Docker Container bauen
print("Start")

for f in os.listdir("/experiments"):
    if ".qcow2" in f:
        os.system("rsync /experiments/%s root@172.12.0.1:/usr/testbed/%s"%(f,f))
        os.system("rm /experiments/%s"%(f))
        ####
        hostname = f.split(".")[0]
        os.system("cat /VITO/templateconfig.xml")
        os.system("sed -i 's/TEMPLATE/%s/g' /VITO/templateconfig.xml"%(hostname))
        ####
        os.system("rsync /VITO/templateconfig.xml root@172.12.0.1:/tmp/definition.xml")
        os.system("ssh root@172.12.0.1 virsh define /tmp/definition.xml")
for f in os.listdir("/experiments"):
    if ".json" in f and not ".done" in f:
        parser = Parser("/experiments/%s"%(f))
        testbed = parser.get_testbed_config()
        p = Physical_Host("172.12.0.1")
        p.check_host()
        p.execute_experiment(testbed)
        os.system("mv /experiments/%s /experiments/%s.done"%(f,f))
    