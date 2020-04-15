import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.is_fullscreen = False
        self.monitor_num_for_display = 0

    def do_activate(self):
        window = Gtk.Window(application=self)
        window.set_title("McColm Robotics GTK Framework")
        window.set_default_size(500, 300)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("key-release-event", self.on_key_release)
        if self.is_fullscreen == True:
            window.fullscreen_on_monitor(Gdk.Screen.get_default(), self.monitor_num_for_display)
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
        self.set_default_size(651, 397)

        area = self.get_content_area()
        grid = Gtk.Grid(column_homogeneous=False, column_spacing=10, row_spacing=10)
        area.add(grid)
        area.get_style_context().add_class('orange-background')

        RUN_Button = Gtk.Button(label="Run")
        RUN_Button.connect("clicked", self.button_clicked)
        RUN_Button.get_style_context().add_class('green-background')

        QUIT_Button = Gtk.Button(label="Quit")
        QUIT_Button.connect("clicked", self.button_clicked)
        QUIT_Button.set_name("myButton_red")

        vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_list.get_style_context().add_class('grid_list')
        vbox_list.set_hexpand(True)
        vbox_list.set_vexpand(True)
        vbox_list.set_valign(Gtk.Align.END)

        group = Gtk.RadioButton.new(None)

        display = Gdk.Display.get_default()
        num_of_monitors = display.get_n_monitors()

        for i in range(num_of_monitors):
            monitor = display.get_monitor(i)
            geometry = monitor.get_geometry()
            scale_factor = monitor.get_scale_factor()
            width = scale_factor * geometry.width
            height = scale_factor * geometry.height

            if monitor.is_primary():
                label = "Monitor #" + repr(i) + " - " + repr(width) + " X " + repr(height) + " (PRIMARY)"

                button = Gtk.RadioButton.new_with_label_from_widget(group, label)
                button.get_style_context().add_class('blue-text')
                button.connect("toggled", self.on_button_toggled, i, parent)
                button.set_active(True)
            else:
                label = "Monitor #" + repr(i) + " - " + repr(width) + " X " + repr(height)

                button = Gtk.RadioButton.new_with_label_from_widget(group, label)
                button.get_style_context().add_class('blue-text')
                button.connect("toggled", self.on_button_toggled, i, parent)

            vbox_list.add(button)

        checkbutton = Gtk.CheckButton.new_with_label("Fullscreen Window")
        checkbutton.get_style_context().add_class('blue-text')
        checkbutton.connect("toggled", self.on_fullscreen_toggled, "fullscreen", parent)
        checkbutton.set_active(True)
        vbox_list.add(checkbutton)

        grid.attach(vbox_list, 1, 2, 1, 1)
        grid.attach(RUN_Button, 2, 0, 1, 1)
        grid.attach(QUIT_Button, 2, 1, 1, 1)

        self.show_all()

    def on_button_toggled(self, button, name, parent):
        if button.get_active():
            parent.monitor_num_for_display = name

    def on_fullscreen_toggled(self, button, name, parent):
        if button.get_active():
            parent.is_fullscreen = True
        else:
            parent.is_fullscreen = False

    def button_clicked(self, button):
        if button.get_label() == "Run":
            self.response(Gtk.ResponseType.OK)
        elif button.get_label() == "Quit":
            self.response(Gtk.ResponseType.CANCEL)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style-pt2.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

app = MyApplication()
if app.popup_run_dialog():
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)