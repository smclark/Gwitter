# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from gwitter.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('gwitter')

class AboutGwitterDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutGwitterDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated AboutGwitterDialog object.
        """
        builder = get_builder('AboutGwitterDialog')
        new_object = builder.get_object("about_gwitter_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a AboutGwitterDialog object with it in order to
        finish initializing the start of the new AboutGwitterDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        # Code for other initialization actions should be added here.


if __name__ == "__main__":
    dialog = AboutGwitterDialog()
    dialog.show()
    gtk.main()
