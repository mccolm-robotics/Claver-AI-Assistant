import sys
import gi
gi.require_version('Gtk', '3.0')
from Claver.interface.ProgramLoader import *
from Claver.assistant.avatar.renderEngine.GLCanvas import *
from Claver.interface.Settings import res_dir


class MainWindow(Gtk.Application):

    # Default Window Size
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self):
        Gtk.Application.__init__(self)
        self.is_fullscreen = False
        self.monitor_num_for_display = 0

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(res_dir['LOADER_GUI'] + 'style.css')
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_activate(self):
        window = Gtk.Window(application=self)
        window.set_title("Claver")
        window.set_default_size(self.WIDTH, self.HEIGHT)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("key-release-event", self.on_key_release)
        window.connect("key-press-event", self.on_key_press)

        # Attach a Gtk.GLArea widget to the window. GLCanvas subclasses Gtk.GLArea
        self.glCanvas = GLCanvas()
        window.add(self.glCanvas)

        if self.is_fullscreen == True:
            display = Gdk.Display.get_default()
            window.fullscreen_on_monitor(Gdk.Screen.get_default(), self.monitor_num_for_display)
            monitor = display.get_monitor(self.monitor_num_for_display)
            geometry = monitor.get_geometry()
            scale_factor = monitor.get_scale_factor()
            width = scale_factor * geometry.width
            height = scale_factor * geometry.height
            # print("Monitor resolution: {}x{}".format(width, height))

        window.show_all()

    def on_key_release(self, window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit()
        elif event.keyval == Gdk.KEY_f or event.keyval == Gdk.KEY_F:
            self.fullscreen_mode(window)
        else:
            self.glCanvas.cancelKeyPress(event.keyval)

    def on_key_press(self, window, event):
        if event.keyval != Gdk.KEY_f:
            self.glCanvas.registerKeyPress(event.keyval)

    def fullscreen_mode(self, window):
        if self.is_fullscreen == True:
            window.unfullscreen()
            self.is_fullscreen = False
        else:
            window.fullscreen()
            self.is_fullscreen = True

    def runProgramLoader(self):
        dialog = ProgramLoader(self)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return True
        elif response == Gtk.ResponseType.CANCEL:
            return False


win = MainWindow()
if win.runProgramLoader():
    exit_status = win.run(sys.argv)
    sys.exit(exit_status)
