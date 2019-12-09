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
import threading
import time

class Executor:

    def __init__(self,ip):
        self.ip = ip
        self.commands = []

    def add_command_to_queue(self,command,time,background=True,repeat=False):
        self.commands.append(Command_Container(self.ip,command,time,background,repeat))

    def start_experiment(self):
        x = threading.Thread(target=executor,args=(self.commands,))
        x.start()
        return x





def executor(commands):
    executed_commands = dict()
    start_time = time.time()
    while len(commands) > 0:
        actual_time = time.time()-start_time
        for com in commands:
            val = com.execute(actual_time)
            if val != None:
                executed_commands[com] = val
                if actual_time  > com.repeat:
                    commands.remove(com)
        time.sleep(1)
        print("Commands pending: %s"%(commands))
    print(executed_commands)



class Command_Container:

    def __init__ (self,ip,command,time,background,repeat):
        self.ip = ip
        self.command = command
        self.time = int(time)
        self.background = background
        self.repeat = int(repeat)

    def execute(self,actual_time):
        if (self.time <= actual_time and self.repeat == 0) or (self.time > 0 and actual_time % self.time == 0 and actual_time > 0):
            if self.background:
                print("ssh root@%s %s"%(self.ip,self.command))
                os.system("ssh root@%s %s"%(self.ip,self.command))
                return "done"
            else:
                print("ssh root@%s bash -c \'%s\'"%(self.ip,self.command))
                result = os.popen("ssh root@%s \'%s\'"%(self.ip,self.command)).read().strip()
                return result
        return None

    def __repr__(self):
        return "(%s,%s,%s)"%(self.command,self.time,self.repeat)