import cairo
import gi

from Claver.assistant.avatar.entities.Player import Player

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from Claver.assistant.avatar.renderEngine.Loader import Loader
from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
from Claver.assistant.avatar.shaders.StaticShader import StaticShader
from Claver.assistant.avatar.terrain.Terrain import Terrain
from Claver.assistant.avatar.textures.TerrainTexture import TerrainTexture
from Claver.assistant.avatar.textures.TerrainTexturePack import TerrainTexturePack
from Claver.assistant.avatar.textures.ModelTexture import ModelTexture
from Claver.assistant.avatar.models.TexturedModel import TexturedModel
from Claver.assistant.avatar.entities.Entity import Entity
from Claver.assistant.avatar.entities.Light import Light
from Claver.interface.Settings import res_dir
from Claver.interface.InputEvent import InputEvent
from Claver.assistant.avatar.entities.Camera import Camera
from Claver.assistant.avatar.renderEngine.ModelLoader import ModelLoader
from Claver.assistant.avatar.toolbox.Primitives import Primitives


class GLCanvas(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_required_version(4, 5)  # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize)  # This signal is used to initialize the OpenGL state
        self.connect("unrealize", self.on_unrealize)  # Catch this signal to clean up buffer objects and shaders
        self.connect("render", self.on_render)  # This signal is emitted for each frame that is rendered
        self.connect("resize", self.on_resize)  # This signal is emitted when the window is resized
        self.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.BUTTON_MOTION_MASK|Gdk.EventMask.BUTTON_PRESS_MASK|Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect("scroll-event", self.on_mouse_scroll)
        self.connect("motion-notify-event", self.on_mouse_movement)
        self.connect("button-press-event", self.on_mouse_press)
        self.connect("button-release-event", self.on_mouse_release)
        self.add_tick_callback(self.tick)  # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False  # Boolean to track whether the clock has been initialized
        self.set_has_depth_buffer(True)
        self.inputEvents = InputEvent()
        self.cursorCoords = None
        self.previousCursorCoords = None
        self.initalizedCursor = False

    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:  # Initializes the timer at the start of the program
            self.last_frame_time = 0  # Stores the previous timestamp
            self.last_frame_delta = 0
            self.frame_counter = 0  # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0  # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time  # Stores the timestamp set when the program was initalized
            self.set_start_time = True  # Prevents the initialization routine from running again in this instance

        self.delta = self.current_frame_time - self.last_frame_delta
        self.last_frame_delta = self.current_frame_time
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
        self.window_rect = gl_area.get_allocation()
        self.screen = Gdk.Screen.get_default()

        cursor = cairo.ImageSurface.create_from_png("../res/cursors/pointer.png")
        display = Gdk.Display.get_default()

        self.custom_cursor = Gdk.Cursor.new_from_surface(display, cursor, 0, 0)
        gl_area.get_window().set_cursor(self.custom_cursor)

        self.loader = Loader()

        rawChibi = ModelLoader().loadModel(self.loader, res_dir['MODELS']+"Chibi.obj")
        rawChibiTexture = ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Chibi_Texture.png"))
        chibiModel = TexturedModel(rawChibi, rawChibiTexture)
        chibiTexture = chibiModel.getTexture()
        chibiTexture.setShineDamper(10)
        chibiTexture.setReflectivity(1)
        self.chibi = Player(chibiModel, (0.0, 0.0, 0.0), 0.0, 0.0, 0.0, 0.25, self.inputEvents)

        rawCube = ModelLoader().loadPrimitive(self.loader, Primitives().cube())
        rawCubeTexture = ModelTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "CircuitTree.png", False))
        cubeModel = TexturedModel(rawCube, rawCubeTexture)
        cubeTexture = cubeModel.getTexture()
        cubeTexture.setShineDamper(10)
        cubeTexture.setReflectivity(1)
        self.cube = Entity(cubeModel, (3.0, 1.0, 2.0), 0.0, 0.0, 0.0, 1.0)

        treeModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS']+"Tree.obj"),
                                  ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Tree_Texture.png")))

        grassModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS'] + "Grass.obj"),
                                  ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Grass_Texture.png")))
        grassModel.getTexture().setHasTransparency(True)
        grassModel.getTexture().setUseFakeLighting(True)

        fernModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS'] + "Fern.obj"),
                                   ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Fern_Texture.png")))
        fernModel.getTexture().setHasTransparency(True)


        self.light = Light(Vector3((0, 0, 5)), Vector3((1,1,1)))

        backgroundTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "grass2.png"))
        rTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "mud.png"))
        gTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "grassFlowers2.png"))
        bTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "path.png"))

        texturePack = TerrainTexturePack(backgroundTexture, rTexture, gTexture, bTexture)
        blendMap = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "blendMap.png"))

        self.terrain = []
        for i in range(-1, 1):
            for j in range(-1, 1):
                self.terrain.append(Terrain(i, j, self.loader, texturePack, blendMap))

        import random
        self.entities = []
        for i in range(30):
            self.entities.append(Entity(grassModel, (random.uniform(-.8, .8) * 120, 0.0, random.uniform(-.8, .8) * 120), 0.0, 0.0, 0.0, 1.0))
            self.entities.append(Entity(treeModel, (random.uniform(-.8, .8) * 120, 0.0, random.uniform(-.8, .8) * 120), 0.0, 0.0, 0.0, 3.0))
            self.entities.append(Entity(fernModel, (random.uniform(-.8, .8) * 120, 0.0, random.uniform(-.8, .8) * 120), 0.0, 0.0, 0.0, 0.4))

        self.renderer = MasterRenderer(self.window_rect, self.inputEvents)

        return True

    def on_render(self, gl_area, gl_context):
        self.renderer.processMovement(self.delta)
        self.chibi.move(self.delta)

        for terrain in self.terrain:
            self.renderer.processTerrain(terrain)
        for entity in self.entities:
            self.renderer.processEntity(entity)
        self.renderer.processEntity(self.chibi)
        self.renderer.processEntity(self.cube)

        self.renderer.render(self.light, self.running_seconds_from_start)
        self.queue_draw()  # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        self.renderer.cleanUp()
        self.loader.cleanUp()

    def registerKeyPress(self, key):
        self.inputEvents.registerKeyboardEvent(key)

    def cancelKeyPress(self, key):
        self.inputEvents.cancelKeyboardEvent(key)


    def on_mouse_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.renderer.getCamera().decreaseFOV()
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.renderer.getCamera().increaseFOV()

    def on_mouse_movement(self, widget, event):
        state = event.get_state()
        if state & Gdk.ModifierType.BUTTON3_MASK:
            self.inputEvents.setCursorPosition((int(event.x_root), int(event.y_root)))

    def on_mouse_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                print("Left mouse button clicked")
            if event.button == 3:
                if self.initalizedCursor is False:
                    self.device = event.get_device()
                    self.inputEvents.setDevice(event.get_device())
                    self.cursorCoords = (int(event.x_root), int(event.y_root))
                    self.renderer.getCamera().setStartingPosition((int(event.x_root), int(event.y_root)))
                    self.renderer.getCamera().setLastMovePosition((int(event.x_root), int(event.y_root)))
                    self.renderer.getCamera().activateWarp()
                    self.inputEvents.setCursorPosition(self.cursorCoords)
                    self.inputEvents.setStaringCoordinate(self.cursorCoords)
                    blank_cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR)
                    widget.get_toplevel().get_window().set_cursor(blank_cursor)
                    self.initalizedCursor = True


    def on_mouse_release(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
            # Right mouse button
            print("Left mouse button released")
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 3:
            # Left mouse button
            widget.get_toplevel().get_window().set_cursor(self.custom_cursor)
            Gdk.Device.warp(self.device, self.screen, self.cursorCoords[0], self.cursorCoords[1])
            self.renderer.getCamera().deactivateWarp()
            self.renderer.getCamera().setLastMovePosition((int(event.x_root), int(event.y_root)))
            self.inputEvents.setCursorPosition((int(event.x_root), int(event.y_root)))
            self.initalizedCursor = False


    def on_resize(self, area, width, height):
        self.renderer.windowResized(width, height)
