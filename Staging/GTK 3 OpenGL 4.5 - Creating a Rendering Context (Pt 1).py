"""
Author: Praxis (McColm Robotics)
Created: April 2020
Python interpreter: 3.7
GTK3 version: 3.24
PyCharm version: 2020.1
Platform: Ubuntu 19.10
"""

#from Claver_Program_Launcher import *
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
        self.set_required_version(4, 5)             # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize) # This signal is used to initialize the OpenGL state
        self.connect("render", self.on_render)      # This signal is emitted for each frame that is rendered
        self.add_tick_callback(self.tick)           # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False                 # Boolean to track whether the clock has been initialized

        self.vertices = [           # Triangle
            0.6,  0.6, 0.0, 1.0,    # Vertex 1
            -0.6,  0.6, 0.0, 1.0,   # Vertex 2
            0.0, -0.6, 0.0, 1.0]    # Vertex 3

        self.vertices = np.array(self.vertices, dtype=np.float32)   # Converts the Python list into a NumPy array


    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:                        # Initializes the timer at the start of the program
            self.last_frame_time = 0                            # Stores the previous timestamp
            self.frame_counter = 0                              # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0                 # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time        # Stores the timestamp set when the program was initalized
            self.set_start_time = True                          # Prevents the initialization routine from running again in this instance

        self.running_seconds_from_start = (self.current_frame_time - self.starting_time)/1000000    # Calculate the total number of seconds that the program has been running

        self.frame_counter += 1                                         # The frame counter is called by GTK each time a frame is rendered. Keep track of how many are rendered.
        # Track how many Frames Per Second (FPS) are rendered
        if self.current_frame_time - self.last_frame_time > 1000000:    # Checks to see if 60 seconds have elapsed since the last counter reset
            print(str(self.frame_counter) + "/s")                       # Prints out the number of frames rendered in the last second
            self.frame_counter = 0                                      # Resets the frame counter
            self.last_frame_time = self.current_frame_time              # Records the current timestamp to compare against for the next second
        return True                                                     # Returns true to indicate that tick callback should contine to be called

    def build_program(self):
        VERTEX_SHADER_SOURCE = """
            #version 450 core
            in vec4 vertex_position;
            void main()
            {
                gl_Position = vertex_position;
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
        # These are helper functions provided by PyOpenGL
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)           # Compiles the vertex shader into intermediate binary representation
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)     # Compiles the fragment object into intermediate binary representation
        self.shader = compileProgram(vertex_shader, fragment_shader)                    # Links the vertex and fragment shader objects together into a program

    def on_initialize(self, gl_area):
        # Prints information about our OpenGL Context
        opengl_context = self.get_context()             # Retrieves the Gdk.GLContext used by gl_area
        opengl_context.make_current()                   # Makes the Gdk.GLContext current to the drawing surfaced used by Gtk.GLArea
        major, minor = opengl_context.get_version()     # Gets the version of OpenGL currently used by the opengl_context
        print("OpenGL context created successfully.\n-- Using OpenGL Version " + str(major) + "." + str(minor))

        # Checks to see if there were errors creating the context
        if gl_area.get_error() != None:
            print(gl_area.get_error())

        self.build_program()    # Calls build_program() to compile and link the shaders

        self.vao_list = np.empty(0, dtype=np.uint32)
        # Initializes the vertex array object and activates the 'vertex_position' attribute
        vertex_array_object = GLuint()                                # Stores the name of the vertex array object
        glCreateVertexArrays(1, ctypes.byref(vertex_array_object))     # Creates the vertex array object and initalizes it to default values
        self.vao_list = np.append(self.vao_list, vertex_array_object)
        glBindVertexArray(GLuint(self.vao_list[0]))                       # Binds the vertex array object to the OpenGL pipeline target
        self.vertex_attribute_position = glGetAttribLocation(self.shader, 'vertex_position')    # Obtains a reference to the 'vertex_position' attribute from the vertex shader
        glEnableVertexAttribArray(self.vertex_attribute_position)                               # Activates client-side use of vertex attribute arrays for rendering

        # Creates a buffer to hold the vertex data and binds it to the OpenGL pipeline
        self.vertex_buffer = GLuint()                           # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(self.vertex_buffer))    # Generates a buffer to hold the vertex data
        glNamedBufferStorage(self.vertex_buffer, self.vertices.nbytes, self.vertices, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)       # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glVertexAttribPointer(self.vertex_attribute_position, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0)) # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        return True

    def on_render(self, gl_area, gl_context):
        # Changes the background colour based on the the value of the program's running time
        colour_vector = [math.sin(self.running_seconds_from_start)*.5+.5, math.cos(self.running_seconds_from_start)*.5+.5, 0.0, 1.0]
        glClearBufferfv(GL_COLOR, 0, colour_vector)     # Clears the colour buffer to the value of colour_vector

        glUseProgram(self.shader)                       # Tells OpenGL to use the shader program for rendering geometry

        glBindVertexArray(GLuint(self.vao_list[0]))     # Binds the self.vertex_array_object to the OpenGL pipeline vertex target
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertices)/4))    # Constructs geometric primitives (GL_TRIANGLES) using sequential elements of the vertex array

        self.queue_draw()   # Schedules a redraw for Gtk.GLArea

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

        # Attach a Gtk.GLArea widget to the window. GLCanvas subclasses Gtk.GLArea
        window.add(GLCanvas())

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
        dialog = PopUp(self) # This class is defined in Claver_Program_Launcher.py
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return True
        elif response == Gtk.ResponseType.CANCEL:
            return False

win = RootWindow()
# Uncomment these lines to enable the program launcher
# You must also uncomment the top import statement and make sure that
# Claver_Program_Launcher.py is sitting in the same directory as this file

#if win.popup_run_dialog():
#    exit_status = win.run(sys.argv)
#    sys.exit(exit_status)
exit_status = win.run(sys.argv)
sys.exit(exit_status)