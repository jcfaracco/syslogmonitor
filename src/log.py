#!/usr/bin/python

import subprocess
from dialog import ReloadingDialog

class File:

       def __init__(self, bar=None):
               self.bar = bar
               self.log_file = "/var/log/messages"
               self.fdialog = ReloadingDialog()
               self.array = []
               self.secarray = []
               self.pid = []

       def read(self):
               progress = 0
 
               self.fdialog.show_all()
               with open(self.log_file) as f:
                       size = sum(1 for _ in f)
               f.close()

               fobj = open(self.log_file)
               for line in fobj:
                       row = self.parse_line(line.rstrip())
                       if not any(row[0] in s for s in self.secarray):
                               self.secarray.append(row[0])
                       if not any(row[1] in s for s in self.pid):
                               self.pid.append(row[1])
                       self.array.append(row)
                       progress += 1
                       self.fdialog.read_line(progress, size)
               fobj.close()

               self.fdialog.hide_all()


       def parse_line(self, line):
               array = []
               array_sw = []
               arrayinfo = line.split( );
               arraymessage = line.split(arrayinfo[4])
               
               array_sw.append(arrayinfo[0])
               array_sw.append(arrayinfo[1])
               array_sw.append(arrayinfo[2])
               array_sw.append(arrayinfo[3])
               array_sw.append(arraymessage[-1][1:])
               array.append(arrayinfo[4][:-1].split("[")[0])
               if (len(arrayinfo[4][:-1].split("[")) < 2):
                       array.append("None")
               else:
                       array.append(arrayinfo[4][:-1].split("[")[1][:-1])
               array.append(array_sw)

               return array
