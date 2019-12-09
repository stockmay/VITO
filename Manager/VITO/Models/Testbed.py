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

class Testbed:

    def __init__(self,experiment_name):
        self.experiment_name = experiment_name
        self.hosts = []

    def add_host(self,host):
        self.hosts.append(host)

    def __str__(self):
        val = "Experiment %s \n"%(self.experiment_name)
        for host in self.hosts:
            val += str(host)
            val += "\n\n"
        return val