#!/usr/bin/env python
# vim: ts=4:sw=4:tw=78:nowrap
""" Demonstration using editable and activatable CellRenderers """
import pygtk
pygtk.require("2.0")
import gtk, gobject

friends = ["dave","pete"]
non_friends = ["suzy","clive"]
tasklist = {"Friends":friends,"Enemies":non_friends}

class GUI_Controller:
    """ The GUI class is the controller for our application """
    def __init__(self):
        # setup the main window
        self.root = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
        self.root.set_title("CellRenderer Example")
        self.root.connect("destroy", self.destroy_cb)
        # Get the model and attach it to the view
        self.mdl = Store.get_model()
        self.view = Display.make_view( self.mdl )
        # Add our view into the main window
        self.root.add(self.view)
        self.root.show_all()
        return
    def destroy_cb(self, *kw):
        """ Destroy callback to shutdown the app """
        gtk.main_quit()
        return
    def run(self):
        """ run is called to set off the GTK mainloop """
        gtk.main()
	return	

class InfoModel:
    """ The model class holds the information we want to display """
    def __init__(self):
        """ Sets up and populates our gtk.TreeStore """
        self.tree_store = gtk.TreeStore( gobject.TYPE_STRING,
                                         gobject.TYPE_BOOLEAN )
        # places the global people data into the list
        # we form a simple tree.
        for item in tasklist.keys():
            parent = self.tree_store.append( None, (item, None) )
            for p in tasklist[item]:
                self.tree_store.append( parent, (p,None) )
        return
    def get_model(self):
        """ Returns the model """
        if self.tree_store:
            return self.tree_store 
        else:
            return None

class DisplayModel:
    """ Displays the Info_Model model in a view """
    def make_view( self, model ):
        """ Form a view for the Tree Model """
        self.view = gtk.TreeView( model )
        # setup the text cell renderer and allows these
        # cells to be edited.
        self.renderer = gtk.CellRendererText()

        # Connect column0 of the display with column 0 in our list model
        # The renderer will then display whatever is in column 0 of
        # our model .
        self.column0 = gtk.TreeViewColumn("Buddies", self.renderer, text=0)

        self.view.append_column( self.column0 )
        return self.view
    def col1_toggled_cb( self, cell, path, model ):
        """
        Sets the toggled state on the toggle button to true or false.
        """
        model[path][1] = not model[path][1]
        print "Toggle '%s' to: %s" % (model[path][0], model[path][1],)
        return

if __name__ == '__main__':
    Store = InfoModel()	
    Display = DisplayModel()
    myGUI = GUI_Controller()
    myGUI.run()

