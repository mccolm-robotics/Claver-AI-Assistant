import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.is_fullscreen = False

    def do_activate(self):
        window = Gtk.Window(application=self)
        window.set_title("McColm Robotics GTK Framework")
        window.set_default_size(500, 300)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("key-release-event", self.on_key_release)
        window.show_all()

    def on_key_release(self, window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit()
        elif event.keyval == Gdk.KEY_f:
            self.fullscreen_mode(window)

    def fullscreen_mode(self, window):
        if self.is_fullscreen == True:
            window.unfullscreen()
            self.is_fullscreen = False
        else:
            window.fullscreen()
            self.is_fullscreen = True

    def popup_run_dialog(self):
        dialog = PopUp(self)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return True
        elif response == Gtk.ResponseType.CANCEL:
            return False

class PopUp(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self)
        self.set_title("Program Launcher")
        self.set_default_size(350, 200)

        area = self.get_content_area()
        grid = Gtk.Grid(orientation=Gtk.Orientation.HORIZONTAL)
        area.add(grid)
        area.get_style_context().add_class('orange-background')

        RUN_Button = Gtk.Button(label="Run")
        RUN_Button.connect("clicked", self.button_clicked)
        RUN_Button.get_style_context().add_class('green-background')

        QUIT_Button = Gtk.Button(label="Quit")
        QUIT_Button.connect("clicked", self.button_clicked)
        QUIT_Button.set_name("myButton_red")

        grid.add(RUN_Button)
        grid.add(QUIT_Button)
        RUN_Button.set_margin_start(120)
        grid.set_margin_top(150)

        self.show_all()

    def button_clicked(self, button):
        if button.get_label() == "Run":
            self.response(Gtk.ResponseType.OK)
        elif button.get_label() == "Quit":
            self.response(Gtk.ResponseType.CANCEL)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style-pt1.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

app = MyApplication()
if app.popup_run_dialog():
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)