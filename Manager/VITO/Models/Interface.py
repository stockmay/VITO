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

class Interface:

    def __init__(self,name,bridge,mac,mtu,ip,bandwidth,delay,jitter,loss,tcpdump,routes):
        self.name = name
        self.bridge = bridge
        self.mac = mac
        self.mtu = mtu
        self.ip = ip
        self.bandwidth = bandwidth
        self.delay = delay
        self.jitter = jitter
        self.loss = loss
        self.tcpdump = tcpdump
        self.routes = routes

    def __str__(self):
        val = "%s connected to %s\n"%(self.name,self.bridge)
        val += "Mac: %s, IP: %s, MTU: %s\n"%(self.mac,self.ip,self.mtu)
        val += "Bandwidth: %s, Delay: %s, Jitter: %s, Loss: %s\n"%(self.bandwidth,self.delay,self.jitter,self.loss)
        val += "Tcpdump? %s"%(self.tcpdump)
        for dest,via in self.routes.items():
            val += "\nRoute to %s via %s"%(dest,via)
        return val