# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk, os, sys
from oauth import oauth
import gwitter.oauthtwitter as twitt 

from gwitter.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('gwitter')



#AUTH_FILE_PATH = "%s/data/auth_token" % PROJECT_ROOT_DIRECTORY

class AuthDialog(gtk.Dialog):
    __gtype_name__ = "AuthDialog"

    PROJECT_ROOT_DIRECTORY = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))
    AUTH_FILE_PATH = "%s/data/auth_token" % PROJECT_ROOT_DIRECTORY

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated AuthDialog object.
        """
        builder = get_builder('AuthDialog')
        new_object = builder.get_object('auth_dialog')
        new_object.finish_initializing(builder)

        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a AuthDialog object with it in order to
        finish initializing the start of the new AuthDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    def set_oauth_details(self, consumer_key, consumer_secret):
        #set up twit auth values
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.twitter = twitt.OAuthApi(self.consumer_key, self.consumer_secret)
        self.tmp_cred = self.twitter.getRequestToken()
        self.auth_url = self.twitter.getAuthorizationURL(self.tmp_cred)        
        #Get link to authorise and set button to link up.
        self.builder.get_object("linkbutton1").set_uri(self.auth_url)        

    def ok(self, widget, data=None):
        """The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        pin = self.builder.get_object("txt_pin_entry").get_text()
        access_token = self.twitter.getAccessToken(self.tmp_cred, pin)
        auth_file = None

        try:
            auth_file = open(self.AUTH_FILE_PATH, "w")
            auth_file.write("token:%s\n" % access_token['oauth_token'])
            auth_file.write("secret:%s\n" % access_token['oauth_token_secret'])
            auth_file.close()
        except IOError as (errno, strerror):
            print "I/O error in AuthDialog ({0}): {1}".format(errno, strerror)
        finally:
            if (auth_file != None):
                try:                
                    auth_file.close()
                    auth_file = None
                except Exception:
                    pass

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass


if __name__ == "__main__":
    dialog = AuthDialog()
    dialog.show()
    gtk.main()
