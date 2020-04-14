# Source: https://developer.gnome.org/gnome-devel-demos/stable/window.py.html.en
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys


class MyApplication(Gtk.Application):

    def do_activate(self):
        # create a Gtk Window belonging to the application itself
        window = Gtk.Window(application=self)
        # set the title
        window.set_title("McColm Robotics GTK Framework")
        # set the default size
        window.set_default_size(500, 300)
        # Set starting position of window
        window.set_position(Gtk.WindowPosition.CENTER)
        # show the window
        window.show_all()

# create and run the application, exit with the value returned by
# running the program
app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)