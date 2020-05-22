import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from Claver.assistant.avatar.renderEngine.Loader import Loader
from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
from Claver.assistant.avatar.shaders.StaticShader import StaticShader
from Claver.assistant.avatar.textures.ModelTexture import ModelTexture
from Claver.assistant.avatar.models.TexturedModel import TexturedModel
from Claver.assistant.avatar.entities.Entity import Entity
from Claver.assistant.avatar.entities.Light import Light
from Claver.interface.Settings import res_dir
from Claver.interface.KeyboardEvent import KeyboardEvent
from Claver.assistant.avatar.entities.Camera import Camera
from Claver.assistant.avatar.renderEngine.ModelLoader import ModelLoader


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)  # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize)  # This signal is used to initialize the OpenGL state
        self.connect("unrealize", self.on_unrealize)  # Catch this signal to clean up buffer objects and shaders
        self.connect("render", self.on_render)  # This signal is emitted for each frame that is rendered
        self.connect("resize", self.on_resize)  # This signal is emitted when the window is resized
        self.add_tick_callback(self.tick)  # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False  # Boolean to track whether the clock has been initialized
        self.set_has_depth_buffer(True)
        self.keyboard = KeyboardEvent()


    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:  # Initializes the timer at the start of the program
            self.last_frame_time = 0  # Stores the previous timestamp
            self.frame_counter = 0  # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0  # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time  # Stores the timestamp set when the program was initalized
            self.set_start_time = True  # Prevents the initialization routine from running again in this instance

        self.running_seconds_from_start = (self.current_frame_time - self.starting_time) / 1000000  # Calculate the total number of seconds that the program has been running

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

        # Get information about current GTK GLArea canvas
        window = gl_area.get_allocation()

        self.loader = Loader()

        self.model = ModelLoader().loadModel(res_dir['MODELS']+"Chibi.obj", self.loader)
        modelTexture = ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Chibi_Texture.png"))
        staticModel = TexturedModel(self.model, modelTexture)
        texture = staticModel.getTexture()
        texture.setShineDamper(10)
        texture.setReflectivity(1)


        self.entity = Entity(staticModel, (0.0, -6.0, -10.0), 0.0, 2.0, 0.0, 1.0)
        self.light = Light(Vector3((0, 0, 5)), Vector3((1,1,1)))

        self.camera = Camera()

        self.renderer = MasterRenderer()

        # for i in range(200):
        #     x = random(range)
        #     y = randome(range)
        #     z = random(range)
        #     allCubes.add(Entity(cubeModel, Vector3(x,y,z), random.nextFloat * 180, random.nextFloat * 180, 0, 1))
        return True

    def on_render(self, gl_area, gl_context):
        self.camera.move(self.keyboard)

        for entityType in myEntityTypeList:
            self.renderer.processEntity(entityType)

        self.renderer.render(self.light, self.camera, self.running_seconds_from_start)
        self.queue_draw()  # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        self.renderer.cleanUp()
        self.loader.cleanUp()

    def registerKeyPress(self, key):
        self.keyboard.registerEvent(key)

    def cancelKeyPress(self, key):
        self.keyboard.cancelEvent(key)

    def on_resize(self, area, width, height):
        self.renderer.updateProjectionMatrix(width, height)
