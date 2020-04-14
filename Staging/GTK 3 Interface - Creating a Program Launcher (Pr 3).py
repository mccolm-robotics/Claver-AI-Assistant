import gi
import sys
import cairo

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class RootWindow(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.is_fullscreen = False
        self.monitor_num_for_display = 0

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path('style.css')
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
d
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

        self.set_default_size(651, 397)
        self.set_decorated(False)  # Creates a borderless window without a title bar
        self.set_app_paintable(True)
        self.connect('draw', self.draw)
        self.connect("button-press-event", self.do_button_press_event)
        self.connect("motion-notify-event", self.do_button_movement)

        area = self.get_content_area()
        grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        area.add(grid)

        RUN_Button = Gtk.Button(label="Run")
        RUN_Button.connect("clicked", self.button_clicked)
        RUN_Button.get_style_context().add_class('button-background')
        RUN_Button.set_name("myButton_green")

        QUIT_Button = Gtk.Button(label="Quit")
        QUIT_Button.connect("clicked", self.button_clicked)
        QUIT_Button.get_style_context().add_class('button-background')
        QUIT_Button.set_name("myButton_red")

        vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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
                label = "Monitor #" + repr(i + 1) + " - " + repr(width) + " X " + repr(height) + " (PRIMARY)"

                button = Gtk.RadioButton.new_with_label_from_widget(group, label)
                button.get_style_context().add_class('blue-text')
                button.connect("toggled", self.on_button_toggled, i, parent)
                button.set_active(True)
            else:
                label = "Monitor #" + repr(i + 1) + " - " + repr(width) + " X " + repr(height)

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
        grid.get_style_context().add_class('main-grid')

        self.show_all()

    def do_button_press_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            self.window_x, self.window_y = self.get_position()
            self.mouse_x = event.x_root
            self.mouse_y = event.y_root

        return True  # Returning true prevents the event from being propagated to other event handlers

    def do_button_movement(self, widget, event):
        state = event.get_state()
        if state & Gdk.ModifierType.BUTTON1_MASK:
            delta_x = self.mouse_x - event.x_root
            delta_y = self.mouse_y - event.y_root

            self.window_x -= delta_x
            self.window_y -= delta_y
            self.move(self.window_x, self.window_y)

            self.mouse_x = event.x_root
            self.mouse_y = event.y_root

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

    def draw(self, widget, context):
        self.image = cairo.ImageSurface.create_from_png("claver-splash.png")
        input_region = Gdk.cairo_region_create_from_surface(self.image)
        self.input_shape_combine_region(input_region)

        context.set_operator(cairo.OPERATOR_SOURCE)
        context.set_source_surface(self.image, 0, 0)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

win = RootWindow()
if win.popup_run_dialog():
    exit_status = win.run(sys.argv)
    sys.exit(exit_status)