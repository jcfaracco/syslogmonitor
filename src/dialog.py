#!/usr/bin/python

import gtk


class ReloadingDialog(gtk.Window): 
        def __init__(self):
                super(ReloadingDialog, self).__init__()

		self.text = "Reading log 0 of 0."

                self.set_size_request(300, 150)
                self.set_position(gtk.WIN_POS_CENTER)
                self.connect("destroy", gtk.main_quit)
                self.set_title("Reloading ...")
                
        	vbox = gtk.VBox(False, 2)        
        	vbox.set_border_width(9)
        
                self.label = gtk.Label(self.text)
                
        	self.bar = gtk.ProgressBar()
        
        	vbox.pack_start(self.label, False, False, 0)
        	vbox.pack_start(self.bar, False, False, 0)
           
                self.add(vbox)
		self.set_keep_above(True)


        def read_line(self, line, size):
                self.text = "Reading log %d of %d." % (line, size)
                self.label.set_label(self.text)
		self.bar.set_fraction(line/size)
