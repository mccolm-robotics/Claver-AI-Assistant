import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Claver.assistant.avatar.renderEngine.Loader import *
from Claver.assistant.avatar.renderEngine.Renderer import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)             # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize) # This signal is used to initialize the OpenGL state
        self.connect("unrealize", self.on_unrealize)  # Catch this signal to clean up buffer objects and shaders
        self.connect("render", self.on_render)      # This signal is emitted for each frame that is rendered
        self.add_tick_callback(self.tick)           # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False                 # Boolean to track whether the clock has been initialized

        self.vertices = [           # Triangle
            0.6,  0.6, 0.0,    # Vertex 1
            -0.6,  0.6, 0.0,   # Vertex 2
            0.0, -0.6, 0.0]    # Vertex 3

        # self.vertices = np.array(self.vertices, dtype=np.float32)   # Converts the Python list into a NumPy array

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

    def on_initialize(self, gl_area):
        # Prints information about our OpenGL Context
        opengl_context = self.get_context()             # Retrieves the Gdk.GLContext used by gl_area
        opengl_context.make_current()                   # Makes the Gdk.GLContext current to the drawing surfaced used by Gtk.GLArea
        major, minor = opengl_context.get_version()     # Gets the version of OpenGL currently used by the opengl_context
        print("OpenGL context created successfully.\n-- Using OpenGL Version " + str(major) + "." + str(minor))

        # Checks to see if there were errors creating the context
        if gl_area.get_error() != None:
            print(gl_area.get_error())

        self.loader = Loader()
        self.renderer = Renderer()

        self.model = self.loader.loadToVAO(self.vertices)

        # self.build_program()    # Calls build_program() to compile and link the shaders
        #
        # # Initializes the vertex array object and activates the 'vertex_position' attribute
        # self.vertex_array_object = GLuint()                                 # Stores the name of the vertex array object
        # glCreateVertexArrays(1, ctypes.byref(self.vertex_array_object))     # Creates the vertex array object and initalizes it to default values
        # glBindVertexArray(self.vertex_array_object)                         # Binds the vertex array object to the OpenGL pipeline target
        # self.vertex_attribute_position = glGetAttribLocation(self.shader, 'vertex_position')    # Obtains a reference to the 'vertex_position' attribute from the vertex shader
        # glEnableVertexAttribArray(self.vertex_attribute_position)                               # Activates client-side use of vertex attribute arrays for rendering
        #
        # # Creates a buffer to hold the vertex data and binds it to the OpenGL pipeline
        # self.vertex_buffer = GLuint()                           # Stores the name of the vertex buffer
        # glCreateBuffers(1, ctypes.byref(self.vertex_buffer))    # Generates a buffer to hold the vertex data
        # glNamedBufferStorage(self.vertex_buffer, self.vertices.nbytes, self.vertices, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        # glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)       # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        # glVertexAttribPointer(self.vertex_attribute_position, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0)) # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        return True

    def on_render(self, gl_area, gl_context):

        self.renderer.prepare()
        # self.renderer.render(self.model)
        # # Changes the background colour based on the the value of the program's running time
        # colour_vector = [math.sin(self.running_seconds_from_start)*.5+.5, math.cos(self.running_seconds_from_start)*.5+.5, 0.0, 1.0]
        # glClearBufferfv(GL_COLOR, 0, colour_vector)     # Clears the colour buffer to the value of colour_vector
        #
        # glUseProgram(self.shader)                       # Tells OpenGL to use the shader program for rendering geometry
        #
        # glBindVertexArray(self.vertex_array_object)     # Binds the self.vertex_array_object to the OpenGL pipeline vertex target
        # glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertices)/4))    # Constructs geometric primitives (GL_TRIANGLES) using sequential elements of the vertex array

        self.queue_draw()   # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        self.loader.cleanUp()