import sys
import gi, pyrr
import numpy

gi.require_version('Gtk', '3.0')
from pyrr import matrix44, Vector3
from gi.repository import Gtk
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram
from PIL import Image


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(3, 2)             # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize) # This signal is used to initialize the OpenGL state
        self.connect("render", self.on_render)      # This signal is emitted for each frame that is rendered
        self.add_tick_callback(self.tick)           # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False                 # Boolean to track whether the clock has been initialized
        self.set_has_depth_buffer(True)
        self.set_has_stencil_buffer(True)

    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds
        if self.set_start_time == False:                        # Initializes the timer at the start of the program
            self.starting_time = self.current_frame_time        # Stores the timestamp set when the program was initalized
            self.set_start_time = True                          # Prevents the initialization routine from running again in this instance
        self.application_clock = (self.current_frame_time - self.starting_time)/1000000    # Calculate the total number of seconds that the program has been running
        return True                                                     # Returns true to indicate that tick callback should contine to be called

    def on_initialize(self, gl_area):
        # Prints information about our OpenGL Context
        opengl_context = self.get_context()             # Retrieves the Gdk.GLContext used by gl_area
        opengl_context.make_current()                   # Makes the Gdk.GLContext current to the drawing surfaced used by Gtk.GLArea
        major, minor = opengl_context.get_version()     # Gets the version of OpenGL currently used by the opengl_context
        # https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
        print("\033[93m OpenGL context created successfully.\n -- Using OpenGL Version \033[94m" + str(major) + "." + str(minor) + "\033[0m")

        # Checks to see if there were errors creating the context
        if gl_area.get_error() != None:
            print(gl_area.get_error())

        # Get information about current GTK GLArea canvas
        window = gl_area.get_allocation()

        w_width, w_height = window.width, window.height
        self.aspect_ratio = w_width / w_height

        self.cube_positions = [(1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
        self.plane_position = matrix44.create_from_translation(Vector3([-3.0, 1.0, 0.0]))

        cube = [-0.5, -0.5, 0.5, 0.0, 0.0,
                0.5, -0.5, 0.5, 1.0, 0.0,
                0.5, 0.5, 0.5, 1.0, 1.0,
                -0.5, 0.5, 0.5, 0.0, 1.0,

                -0.5, -0.5, -0.5, 0.0, 0.0,
                0.5, -0.5, -0.5, 1.0, 0.0,
                0.5, 0.5, -0.5, 1.0, 1.0,
                -0.5, 0.5, -0.5, 0.0, 1.0,

                0.5, -0.5, -0.5, 0.0, 0.0,
                0.5, 0.5, -0.5, 1.0, 0.0,
                0.5, 0.5, 0.5, 1.0, 1.0,
                0.5, -0.5, 0.5, 0.0, 1.0,

                -0.5, 0.5, -0.5, 0.0, 0.0,
                -0.5, -0.5, -0.5, 1.0, 0.0,
                -0.5, -0.5, 0.5, 1.0, 1.0,
                -0.5, 0.5, 0.5, 0.0, 1.0,

                -0.5, -0.5, -0.5, 0.0, 0.0,
                0.5, -0.5, -0.5, 1.0, 0.0,
                0.5, -0.5, 0.5, 1.0, 1.0,
                -0.5, -0.5, 0.5, 0.0, 1.0,

                0.5, 0.5, -0.5, 0.0, 0.0,
                -0.5, 0.5, -0.5, 1.0, 0.0,
                -0.5, 0.5, 0.5, 1.0, 1.0,
                0.5, 0.5, 0.5, 0.0, 1.0]

        cube = numpy.array(cube, dtype=numpy.float32)

        self.cube_indices = [0, 1, 2, 2, 3, 0,
                        4, 5, 6, 6, 7, 4,
                        8, 9, 10, 10, 11, 8,
                        12, 13, 14, 14, 15, 12,
                        16, 17, 18, 18, 19, 16,
                        20, 21, 22, 22, 23, 20]

        self.cube_indices = numpy.array(self.cube_indices, dtype=numpy.uint32)

        plane = [-0.5, -0.5, 0.0, 0.0, 0.0,
                 2.0, -0.5, 0.0, 1.0, 0.0,
                 2.0, 1.0, 0.0, 1.0, 1.0,
                 -0.5, 1.0, 0.0, 0.0, 1.0]

        plane = numpy.array(plane, dtype=numpy.float32)

        self.plane_indices = [0, 1, 2, 2, 3, 0]
        self.plane_indices = numpy.array(self.plane_indices, dtype=numpy.uint32)

        vertex_shader = """
        #version 330
        in vec3 position;
        in vec2 textCoords;
        uniform mat4 vp;
        uniform mat4 model;
        out vec2 outText;
        void main()
        {
            gl_Position =  vp * model * vec4(position, 1.0f);
            outText = textCoords;
        }
        """

        fragment_shader = """
        #version 330
        in vec2 outText;
        out vec4 outColor;
        uniform sampler2D renderedTexture;
        void main()
        {
            outColor = texture(renderedTexture, outText);
        }
        """

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        # cube VAO
        self.cube_vao = glGenVertexArrays(1)
        glBindVertexArray(self.cube_vao)
        cube_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, cube_VBO)
        glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)
        cube_EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.cube_indices.itemsize * len(self.cube_indices), self.cube_indices, GL_STATIC_DRAW)
        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # textures
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        # plane VAO
        self.plane_vao = glGenVertexArrays(1)
        glBindVertexArray(self.plane_vao)
        plane_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, plane_VBO)
        glBufferData(GL_ARRAY_BUFFER, plane.itemsize * len(plane), plane, GL_STATIC_DRAW)
        plane_EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, plane_EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.plane_indices.itemsize * len(self.plane_indices), self.plane_indices,
                     GL_STATIC_DRAW)
        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, plane.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # textures
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, plane.itemsize * 5, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        ###########################################################################################

        self.plane_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.plane_texture)
        # texture wrapping params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # texture filtering params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w_width, w_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)

        depth_buff = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buff)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, w_width, w_height)

        self.FBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.plane_texture, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buff)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        ###########################################################################################
        self.crate_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.crate_texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # load image
        image = Image.open("models/crate.jpg")
        img_data = numpy.array(list(image.getdata()), numpy.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        ###########################################################################################

        glEnable(GL_DEPTH_TEST)

        view = matrix44.create_from_translation(Vector3([0.0, 0.0, -5.0]))
        projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)

        vp = matrix44.multiply(view, projection)

        glUseProgram(shader)
        vp_loc = glGetUniformLocation(shader, "vp")
        self.model_loc = glGetUniformLocation(shader, "model")
        glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)



        return True

    def on_render(self, gl_area, gl_context):
        self.default_ID = glGetIntegerv(GL_FRAMEBUFFER_BINDING) # GLArea does not seem to use FBO 0 as the default.
        glClearColor(0.2, 0.25, 0.27, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_y = pyrr.Matrix44.from_y_rotation(self.application_clock * 2)

        # draw to the default frame buffer
        glBindVertexArray(self.cube_vao)
        glBindTexture(GL_TEXTURE_2D, self.crate_texture)
        for i in range(len(self.cube_positions)):
            model = matrix44.create_from_translation(self.cube_positions[i])
            if i == 0:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, rot_y * model)
            elif i == 1:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)
            else:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

            glDrawElements(GL_TRIANGLES, len(self.cube_indices), GL_UNSIGNED_INT, None)

        # draw to the custom frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i in range(len(self.cube_positions)):
            model = matrix44.create_from_translation(self.cube_positions[i])
            if i == 0:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, rot_y * model)
            elif i == 1:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)
            else:
                glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

            glDrawElements(GL_TRIANGLES, len(self.cube_indices), GL_UNSIGNED_INT, None)

        glBindFramebuffer(GL_FRAMEBUFFER, self.default_ID)
        glBindVertexArray(0)

        # draw the plane
        glBindVertexArray(self.plane_vao)
        glBindTexture(GL_TEXTURE_2D, self.plane_texture)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.plane_position)
        glDrawElements(GL_TRIANGLES, len(self.plane_indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        self.queue_draw()   # Schedules a redraw for Gtk.GLArea

class RootWindow(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = Gtk.Window(application=self)
        window.set_title("Render To Texture")
        window.set_default_size(1280, 720)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.add(GLCanvas())
        window.show_all()

win = RootWindow()
exit_status = win.run(sys.argv)
sys.exit(exit_status)