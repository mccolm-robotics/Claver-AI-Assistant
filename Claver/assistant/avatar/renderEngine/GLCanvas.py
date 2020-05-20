import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Claver.assistant.avatar.renderEngine.Loader import Loader
from Claver.assistant.avatar.renderEngine.Renderer import Renderer
from Claver.assistant.avatar.shaders.StaticShader import StaticShader
from Claver.assistant.avatar.textures.ModelTexture import ModelTexture
from Claver.assistant.avatar.models.TexturedModel import TexturedModel
from Claver.interface.Settings import res_dir


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)  # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize)  # This signal is used to initialize the OpenGL state
        self.connect("unrealize", self.on_unrealize)  # Catch this signal to clean up buffer objects and shaders
        self.connect("render", self.on_render)  # This signal is emitted for each frame that is rendered
        self.add_tick_callback(self.tick)  # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False  # Boolean to track whether the clock has been initialized

        self.vertices = [
            -0.5, 0.5, 0.0,
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.5, 0.5, 0.0]

        self.textureCoords = [
            0.0, 0.0,  # V0
            0.0, 1.0,  # V1
            1.0, 1.0,  # V2
            1.0, 0.0  # V3
        ]

    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:  # Initializes the timer at the start of the program
            self.last_frame_time = 0  # Stores the previous timestamp
            self.frame_counter = 0  # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0  # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time  # Stores the timestamp set when the program was initalized
            self.set_start_time = True  # Prevents the initialization routine from running again in this instance

        self.running_seconds_from_start = (
                                                      self.current_frame_time - self.starting_time) / 1000000  # Calculate the total number of seconds that the program has been running

        self.frame_counter += 1  # The frame counter is called by GTK each time a frame is rendered. Keep track of how many are rendered.
        # Track how many Frames Per Second (FPS) are rendered
        if self.current_frame_time - self.last_frame_time > 1000000:  # Checks to see if 60 seconds have elapsed since the last counter reset
            print(str(self.frame_counter) + "/s")  # Prints out the number of frames rendered in the last second
            self.frame_counter = 0  # Resets the frame counter
            self.last_frame_time = self.current_frame_time  # Records the current timestamp to compare against for the next second
        return True  # Returns true to indicate that tick callback should contine to be called

    def on_initialize(self, gl_area):
        # Prints information about our OpenGL Context
        opengl_context = self.get_context()  # Retrieves the Gdk.GLContext used by gl_area
        opengl_context.make_current()  # Makes the Gdk.GLContext current to the drawing surfaced used by Gtk.GLArea
        major, minor = opengl_context.get_version()  # Gets the version of OpenGL currently used by the opengl_context
        print("OpenGL context created successfully.\n-- Using OpenGL Version " + str(major) + "." + str(minor))

        # Checks to see if there were errors creating the context
        if gl_area.get_error() != None:
            print(gl_area.get_error(), file=sys.stderr)

        self.loader = Loader()
        self.renderer = Renderer()
        self.shader = StaticShader()

        model = self.loader.loadToVAO(self.vertices, self.textureCoords)
        texture = ModelTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "test_image.png"))
        self.texturedModel = TexturedModel(model, texture)

        return True

    def on_render(self, gl_area, gl_context):

        self.renderer.prepare()
        self.shader.start()
        self.renderer.render(self.texturedModel)
        self.shader.stop()

        self.queue_draw()  # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        self.shader.cleanUp()
        self.loader.cleanUp()
