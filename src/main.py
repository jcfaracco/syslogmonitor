#!/usr/bin/python

import gtk
from log import File

class PyApp(gtk.Window): 
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_size_request(800, 450)
        self.set_position(gtk.WIN_POS_CENTER)
        
        self.connect("destroy", gtk.main_quit)
        self.set_title("System Log Monitor")

	self.fmessages = File()
	self.fmessages.read()

        vbox = gtk.VBox(False, 3)

	refresh = gtk.Button("Refresh", stock=gtk.STOCK_REFRESH)
	filterBy = gtk.Button("Filter by ...")

	buttonBar = gtk.HBox(False, 3)
        buttonBar.pack_start(refresh, False, False, 0)
        buttonBar.pack_start(filterBy, False, False, 0)

	hp = gtk.HPaned()

	notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_BOTTOM)
    
        sw11 = gtk.ScrolledWindow()
	sw11.set_size_request(300, 390)
        sw11.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw11.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        sw12 = gtk.ScrolledWindow()
	sw12.set_size_request(300, 390)
        sw12.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw12.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        notebook.append_page(sw11, gtk.Label("Process"))
        notebook.append_page(sw12, gtk.Label("PID"))

        sw2 = gtk.ScrolledWindow()
        sw2.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

	hp.add1(notebook)
	hp.add2(sw2)
        
        vbox.pack_start(buttonBar, False, False, 0)
        vbox.pack_start(hp, True, True, 0)

	self.create_secondary_process_info_model()
	self.create_secondary_pid_info_model()
        self.create_main_info_model()

        sectreeView = gtk.TreeView(self.secondarystore)
        sectreeView.connect("row-activated", self.on_activated_process_filter)
        sectreeView.set_rules_hint(True)
        sw11.add(sectreeView)

        pidtreeView = gtk.TreeView(self.pidstore)
        pidtreeView.connect("row-activated", self.on_activated_pid_filter)
        pidtreeView.set_rules_hint(True)
        sw12.add(pidtreeView)

        maintreeView = gtk.TreeView(self.mainstore)
        maintreeView.connect("row-activated", self.on_activated)
        maintreeView.set_rules_hint(True)
        sw2.add(maintreeView)

        self.create_secondary_columns(sectreeView)
        self.create_pid_columns(pidtreeView)
        self.create_main_columns(maintreeView)

        self.statusbar = gtk.Statusbar()

        vbox.pack_start(self.statusbar, False, False, 0)

        self.add(vbox)
        self.show_all()

    def create_secondary_process_info_model(self):
        self.secondarystore = gtk.ListStore(str)

        if (len(self.fmessages.secarray) > 0):
                self.secondarystore.append(["--All--"])
        for row in sorted(self.fmessages.secarray):
                self.secondarystore.append([row])


    def create_secondary_pid_info_model(self):
        self.pidstore = gtk.ListStore(str)

        for row in sorted(self.fmessages.pid):
                self.pidstore.append([row])


    def create_main_info_model(self):
        self.mainstore = gtk.ListStore(str, str, str, str, str)

        for row in self.fmessages.array:
                self.mainstore.append(row[2])


    def create_secondary_columns(self, treeView):
    
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Process", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)

    def create_pid_columns(self, treeView):
    
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("PID", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)


    def create_main_columns(self, treeView):
    
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Day", rendererText, text=1)
        column.set_sort_column_id(1)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Time", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Month", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Hostname", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Message", rendererText, text=4)
        column.set_sort_column_id(4)
        treeView.append_column(column)


    def on_activated(self, widget, row, col):
        
        print "clicked"
        model = widget.get_model()
        text = model[row][0] + ", " + model[row][1] + ", " + model[row][2]
        self.statusbar.push(0, text)


    def on_activated_process_filter(self, widget, row, col):
        
        print "clicked"
        model = widget.get_model()
        text = model[row][0]
        self.mainstore.clear()

	for row in self.fmessages.array:
                if text in row[0]: 
                        self.mainstore.append(row[2])
		elif text in "--All--":
			self.mainstore.append(row[2])

    def on_activated_pid_filter(self, widget, row, col):
        
        print "clicked"
        model = widget.get_model()
        text = model[row][0]
        self.mainstore.clear()

	for row in self.fmessages.array:
                if text in row[1]: 
                        self.mainstore.append(row[2])


PyApp()
gtk.main()
