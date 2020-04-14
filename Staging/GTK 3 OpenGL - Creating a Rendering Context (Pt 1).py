from Claver_Program_Launcher import *
import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.add_tick_callback(self.tick)
        self.set_start_time = False

        self.vertices = [
            0.6,  0.6, 0.0, 1.0,
            -0.6,  0.6, 0.0, 1.0,
            0.0, -0.6, 0.0, 1.0]

        self.vertices = np.array(self.vertices, dtype=np.float32)

    def tick(self, widget, frame_clock):
        # A frame clock is compatible with OpenGL. It automatically stops painting when it knows frames will not be visible.
        # A tick is issued every time GTK draws a new frame.
        # Gets a timestamp in microseconds
        self.current_frame_time = frame_clock.get_frame_time() # https://developer.gnome.org/gdk3/stable/GdkFrameClock.html#gdk-frame-clock-get-frame-time

        if self.set_start_time == False:
            self.last_frame_time = 0
            self.frame_counter = 0
            self.running_seconds_from_start = 0
            self.starting_time = self.current_frame_time
            self.set_start_time = True

        self.running_seconds_from_start = (self.current_frame_time - self.starting_time)/1000000

        self.frame_counter += 1
        if self.current_frame_time - self.last_frame_time > 1000000:
            print(str(self.frame_counter) + "/s")
            self.frame_counter = 0
            self.last_frame_time = self.current_frame_time
        return True #Return true to indicate that tick callback should contine to be called https://developer.gnome.org/gtk3/unstable/GtkWidget.html#GtkTickCallback

    def build_program(self):
        VERTEX_SHADER_SOURCE = """
            #version 450 core
            in vec4 position;
            void main()
            {
                gl_Position = position;
            }
        """
        FRAGMENT_SHADER_SOURCE = """
            #version 450 core
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
        """
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, fragment_shader)

    def on_realize(self, area):
        # Print information about our OpenGL Context
        ctx = self.get_context()
        ctx.make_current()
        major, minor = ctx.get_version()
        print("OpenGL context created successfully.\n-- Using OpenGL Version " + str(major) + "." + str(minor))

        self.build_program()
        # Generate vertex array object (VAO)
        # This object maintains all of the state related to the input of the OpenGL pipeline
        self.vertex_array_object = glGenVertexArrays(1) #glCreateVertexArrays() p.60
        glBindVertexArray(self.vertex_array_object)     # Binds the VAO to the context (ctx)

        # Generate buffers to hold our vertices
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)

        # Get the position of the 'position' in parameter of our shader and bind it.
        self.position = glGetAttribLocation(self.shader, 'position')
        glEnableVertexAttribArray(self.position)

        # Describe the position data layout in the buffer
        glVertexAttribPointer(self.position, 4, GL_FLOAT, False, 0, ctypes.c_void_p(0))

        # Send the data over to the buffer
        glBufferData(GL_ARRAY_BUFFER, 48, self.vertices, GL_STATIC_DRAW)

        # Unbind the VAO first (Important)
        glBindVertexArray(0)

        # Unbind other stuff
        glDisableVertexAttribArray(self.position)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        return True

    def on_render(self, area, ctx):
        area.attach_buffers()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        color = [math.sin(self.running_seconds_from_start)*.5+.5, math.cos(self.running_seconds_from_start)*.5+.5, 0.0, 1.0]
        glClearBufferfv(GL_COLOR, 0, color)
        glUseProgram(self.shader)

        glBindVertexArray(self.vertex_array_object)
        # Send vertices into the OpenGL pipeline
        # The vertex shader is executed for each vertex in the array
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertices)/4))
        glBindVertexArray(0)

        glUseProgram(0)
        glFlush()

        # Schedule Redraw
        self.queue_draw()

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

    def do_activate(self):
        window = Gtk.Window(application=self)
        window.set_title("McColm Robotics GTK Framework")
        window.set_default_size(500, 300)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("key-release-event", self.on_key_release)

        glCanvas = GLCanvas()
        glCanvas.set_has_depth_buffer(True)
        window.add(glCanvas)

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

win = RootWindow()
exit_status = win.run(sys.argv)
sys.exit(exit_status)

"""
if win.popup_run_dialog():
    exit_status = win.run(sys.argv)
    sys.exit(exit_status)
"""