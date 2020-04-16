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
    # Gtk.GLArea is a widget that sets up its own Gdk.GLContext. It creates its own GL framebuffer and sets it as the default rendering target.
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)             # Set the version of OpenGL required by this OpenGL program
        self.set_has_depth_buffer(True)
        self.connect("realize", self.on_realize)    # This signal is used to initialize the OpenGL state
        self.connect("render", self.on_render)      # This signal is emitted for each frame that is rendered
        self.add_tick_callback(self.tick)           # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False                 # Boolean to track whether the clock has been initialized

        # This is the data provided to the vertex shader during the 'vertex fetching' stage of the OpenGL pipeline
        # Values are represented as four-component vectors. These are homogeneous coordinates rather than Cartesian coordinate triplets.
        # The fourth value is the 'w' coordinate
        # Coordinates are converted into Cartesian coordinates when OpenGL performs a perspective division. In this stage, all the coordinates are divided by the 'w' coord
        # leaving a value of 1.0 for 'w'
        self.vertices = [
            0.6,  0.6, 0.0, 1.0,
            -0.6,  0.6, 0.0, 1.0,
            0.0, -0.6, 0.0, 1.0]

        # See SuperBible p. 80 for discussion of the difference between clipping space, normalized device space
        # Normalized device space extends from -1.0 to 1.0 in x, y. From 0.0 to 1.0 in z.
        # The window has coordinates with (0,0)  at the bottom left and range (w-1, h-1)
        # The viewport transform is applied to the normalized device coordinates to move them into window coordinates
        # Viewport bounds are set by calling glViewport() and glDepthRange()
        # GL triangle winding, front face, and culling p.82A

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
        # This program is only called once so that we are not wasting time recompiling
        # OpenGL shaders are in in GLSL (OpenGL Shading Language). Languge is a derivative of C programming language
        # This compiler language is built into OpenGL

        # Vertex shader is the first programmable stage of the OpenGL pipeline. It is also the only mandatory shader that must
        # be written in order to create a valid OpenGL program.
        # Require to have a vertex shader and fragment shader to see any pixels on the screen.
        # #version 450 core tells the shader compiler we are using version 4.5 and just the features from the core profile.
        # gl_Position is a built-in variable that is part of GLSL that connects the vertex shader to the fragment shader
        # gl_Position represents the output position of the vertex
        # Declares position as an input variable of type vec4

        # in / out are storage qualifiers that are part of the GLSL these keywords are used to create data transport links between one shader and another.
        # vertex_position is called a 'vertex attribute'. It is a global variable and it is used for injecting data into the OpenGL pipeline
        # vertex attributes in the vertex shader are filled automatically during the vertex fetch stage. The vertex fetch stage is a fixed function pipeline stage
        VERTEX_SHADER_SOURCE = """
            #version 450 core
            in vec4 vertex_position;
            void main()
            {
                gl_Position = vertex_position;
            }
        """

        # fragColor is declared an output variable of type vec4.
        # The value of output variables are sent to the screen
        FRAGMENT_SHADER_SOURCE = """
            #version 450 core
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
        """
        # These are PyOpenGL Convenience Functions and *not* standard OpenGL functions
        # See page 59 of the OpenGL SuperBible (7th Edition) for the general OpenGL process in C.
        # This step combines three steps: 1) Creating a vertex shader object 2) Stores the source code in the shader object 3) compiles the shader object into intermediate binary representation
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
        # This step combines three steps: 1) Creating a fragment shader object 2) Stores the source code in the shader object 3) compiles the shader object into intermediate binary representation
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
        # This step combines three steps: 1) creates a shader program object 2) attaches the vertex and fragment shader objects 3) Links the shader object
        # together into the program 4) deletes the shader objects since the program object now contains the binary code for both shaders
        self.shader = compileProgram(vertex_shader, fragment_shader)

    def on_realize(self, area):
        # Print information about our OpenGL Context
        opengl_context = self.get_context() # Retrieves the GdkGLContext used by area
        opengl_context.make_current()       # Makes the Gdk.GLContext current to the drawable surfaced used by Gtk.GLArea
        major, minor = opengl_context.get_version()     # Gets the version of OpenGL currently used by the opengl context
        print("OpenGL context created successfully.\n-- Using OpenGL Version " + str(major) + "." + str(minor))

        # Check to see if there were errors creating the context (check for shader version support?)
        if area.get_error() != None:
            print(area.get_error())

        # Call our function for compiling and linking the shaders
        self.build_program()

        # Generate vertex array object (VAO)
        # This object maintains all of the state related to the input of the OpenGL pipeline
        # The VAO (vertex array object) supplies input to the vertex shader
        self.vertex_array_object = glGenVertexArrays(1) #glCreateVertexArrays() p.60
        glBindVertexArray(self.vertex_array_object)     # Binds the VAO to the context (ctx). This lets OpenGL know we want to use it.

        # Generate buffers to hold our vertices
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)

        # Get the position of the 'vertex_position' IN parameter of our vertex shader and bind it.
        self.vertex_position = glGetAttribLocation(self.shader, 'vertex_position')
        glEnableVertexAttribArray(self.vertex_position)

        # Describe the position data layout in the buffer
        glVertexAttribPointer(self.vertex_position, 4, GL_FLOAT, False, 0, ctypes.c_void_p(0))

        # Send the data over to the buffer
        glBufferData(GL_ARRAY_BUFFER, 48, self.vertices, GL_STATIC_DRAW)

        # Unbind the VAO first (Important)
        glBindVertexArray(0)

        # Unbind other stuff
        glDisableVertexAttribArray(self.vertex_position)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        return True

    def on_render(self, area, opengl_context):
        area.attach_buffers()


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Creates a vector of floating point numbers
        # Uses the value for number of seconds that the programming has been running
        # Uses this value in sin(), cos() for x and y values
        # This causes the background colour to oscillate
        # 4th value corresponds to opacity. value of 0 makes it transparent.
        color = [math.sin(self.running_seconds_from_start)*.5+.5, math.cos(self.running_seconds_from_start)*.5+.5, 0.0, 1.0]

        # Tells OpenGL to clear the buffer specified by GL_COLOR. The second paramater targets the specific buffer (multibuffer) and 3rd the vector of floating point numbers
        # fv: f = floating point numbers. v = vector
        glClearBufferfv(GL_COLOR, 0, color)

        # Tells OpenGL to use our program for rending geometry to the screen
        glUseProgram(self.shader)

        glBindVertexArray(self.vertex_array_object)
        # Send vertices into the OpenGL pipeline
        # The vertex shader is executed for each vertex in the array
        # GL_TRIANGLES is the type of graphics primitive to render (the rendering mode)
        # Parameter #3 is the number of vertices to render (represented by a Vector4)
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

        # Attach a Gtk.GLArea widget to the window
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