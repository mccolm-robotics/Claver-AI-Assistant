import cairo
import gi
import numpy as np
from OpenGL.GL import *
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
from Claver.assistant.avatar.guis.GuiTexture import GuiTexture
from Claver.assistant.avatar.guis.GuiRenderer import GuiRenderer
from Claver.assistant.avatar.water.WaterTile import WaterTile
from Claver.assistant.avatar.water.WaterFrameBuffers import WaterFrameBuffers
from Claver.assistant.avatar.water.WaterRenderer import WaterRenderer
from Claver.assistant.avatar.water.WaterShader import WaterShader
from Claver.assistant.avatar.fontRendering.TextMaster import TextMaster
from Claver.assistant.avatar.fontMeshCreator.FontType import FontType
from Claver.assistant.avatar.fontMeshCreator.GUIText import GUIText
from Claver.assistant.avatar.particles.ParticleMaster import ParticleMaster
from Claver.assistant.avatar.particles.Particle import Particle
from Claver.assistant.avatar.particles.ParticleSystem import ParticleSystem
from Claver.assistant.avatar.particles.ParticleTexture import ParticleTexture


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
        self.set_has_stencil_buffer(True)
        self.inputEvents = InputEvent()
        self.cursorCoords = None
        self.previousCursorCoords = None
        self.initializedCursor = False
        self.entities = []
        self.normalMapEntities = []

    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:  # Initializes the timer at the start of the program
            self.last_frame_time = 0  # Stores the previous timestamp
            self.last_frame_delta = 0
            self.frame_counter = 0  # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0  # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time  # Stores the timestamp set when the program was initalized
            self.set_start_time = True  # Prevents the initialization routine from running again in this instance

        self.delta = (self.current_frame_time - self.last_frame_delta) / 1000000
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
        print("\033[93m OpenGL context created successfully.\n -- Using OpenGL Version \033[94m" + str(major) + "." + str(minor) + "\033[0m")

        # Checks to see if there were errors creating the context
        if gl_area.get_error() != None:
            print(gl_area.get_error(), file=sys.stderr)

        # Get information about current GTK GLArea canvas
        self.window_rect = gl_area.get_allocation()
        self.window_size = (self.window_rect.width, self.window_rect.height)
        self.screen = Gdk.Screen.get_default()


        cursor = cairo.ImageSurface.create_from_png("../res/cursors/pointer.png")
        display = Gdk.Display.get_default()

        self.custom_cursor = Gdk.Cursor.new_from_surface(display, cursor, 0, 0)
        gl_area.get_window().set_cursor(self.custom_cursor)

        self.loader = Loader()
        TextMaster.init(self.loader)

        font = FontType(self.loader.loadTexture(res_dir['FONT_DISTANCE'] + "candara.png", False), res_dir['FONT_DISTANCE'] + "candara.fnt", self.window_rect)
        maximumLineLength = 0.5
        text = GUIText("Claver AI", 3, font, (0.25, 0.85), maximumLineLength, True)
        text.setColour(0.6, 0.6, 0.6)

        rawCube = ModelLoader().loadPrimitive(self.loader, Primitives().cube())
        rawCubeTexture = ModelTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "circuitTree.png", False))
        cubeModel = TexturedModel(rawCube, rawCubeTexture)
        cubeTexture = cubeModel.getTexture()
        cubeTexture.setShineDamper(10)
        cubeTexture.setReflectivity(1)
        self.cube = Entity(cubeModel, (3.0, 1.0, 2.0), 0.0, 0.0, 0.0, 1.0)
        self.entities.append(self.cube)


        lampModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS']+"Lamp.obj"),
                                  ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Lamp_Texture.png")))
        lampModel.getTexture().setUseFakeLighting(True)

        # # Normal Mapped Model
        # barrelModel = TexturedModel(ModelLoader().loadNormalMappedModel(self.loader, res_dir['MODELS']+"Barrel.obj"),
        #                           ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Barrel_Texture.png")))
        # barrelModel.getTexture().setNormalMap(self.loader.loadTexture(res_dir['MODELS'] + "Barrel_Normal.png"))
        # barrelModel.getTexture().setShineDamper(10)
        # barrelModel.getTexture().setReflectivity(0.5)
        # barrel = Entity(barrelModel, (-3.0, 1.75, -2.0), 0.0, 0.0, 0.0, 0.3)
        # self.normalMapEntities.append(barrel)
        #
        # boulderModel = TexturedModel(ModelLoader().loadNormalMappedModel(self.loader, res_dir['MODELS'] + "Boulder.obj"),
        #                             ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Boulder_Texture.png")))
        # boulderModel.getTexture().setNormalMap(self.loader.loadTexture(res_dir['MODELS'] + "Boulder_Normal.png"))
        # boulderModel.getTexture().setShineDamper(10)
        # boulderModel.getTexture().setReflectivity(0.5)
        # boulder = Entity(boulderModel, (10.0, 0, 8.0), 0.0, 0.0, 0.0, 0.3)
        # self.normalMapEntities.append(boulder)

        treeModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS']+"Pine.obj"),
                                  ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Pine_Texture.png")))
        treeModel.getTexture().setHasTransparency(True)

        grassModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS'] + "Grass.obj"),
                                  ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Grass_Texture.png")))
        grassModel.getTexture().setHasTransparency(True)
        grassModel.getTexture().setUseFakeLighting(True)

        fernTextureAtlas = ModelTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "fern.png"))
        fernTextureAtlas.setNumberOfRows(2)
        fernModel = TexturedModel(ModelLoader().loadModel(self.loader, res_dir['MODELS'] + "Fern.obj"), fernTextureAtlas)
        fernModel.getTexture().setHasTransparency(True)

        self.lights = []
        self.sun = Light(Vector3((0, 10000, -7000)), Vector3((.2,.2,.2)))
        self.lights.append(self.sun)
        self.lights.append(Light(Vector3((10, 8, 30)), Vector3((2, 2, 0)), Vector3((1, 0.01, 0.002))))
        self.lights.append(Light(Vector3((0, 8, -30)), Vector3((4, 0, 0)), Vector3((1, 0.01, 0.002))))

        self.lamp = Entity(lampModel, (10, 0, 30), 0.0, 0.0, 0.0, .3)
        self.entities.append(self.lamp)
        self.blueLamp = Entity(lampModel, (0, 0, -30), 0.0, 0.0, 0.0, .3)
        self.entities.append(self.blueLamp)

        backgroundTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "grass2.png"))
        rTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "mud.png"))
        gTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "grassFlowers2.png"))
        bTexture = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "path.png"))

        texturePack = TerrainTexturePack(backgroundTexture, rTexture, gTexture, bTexture)
        blendMap = TerrainTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "blendMap.png"))
        heightMap = res_dir['HEIGHT_MAPS'] + "heightmap.png"

        # Generate terrain for world
        TERRAIN_WIDTH = 2
        TERRAIN_HEIGHT = 2
        self.terrainTiles = np.empty(shape=[TERRAIN_WIDTH, TERRAIN_HEIGHT], dtype=np.object)
        for i in range(TERRAIN_WIDTH):
            for j in range(TERRAIN_HEIGHT):
                self.terrainTiles[i][j] = Terrain(i - (TERRAIN_WIDTH / 2), j - (TERRAIN_WIDTH / 2), self.loader, texturePack, blendMap, heightMap, (i,j))

        def getTerrainHeight(x, z):
            gridX = x / Terrain.getSize()
            gridZ = z / Terrain.getSize()
            tileX = int((gridX + 1) // 1)
            tileZ = int((gridZ + 1) // 1)
            return self.terrainTiles[tileX][tileZ].getHeightOfTerrain(x, z)

        # Add objects to world
        import random
        RANGE = .8
        for i in range(30):
            x1 = random.uniform(-RANGE, RANGE) * 100
            z1 = random.uniform(-RANGE, RANGE) * 100
            y1 = getTerrainHeight(x1, z1)
            self.entities.append(Entity(grassModel, (x1, y1, z1), 0.0, 0.0, 0.0, 1.0))
            x2 = random.uniform(-RANGE, RANGE) * 100
            z2 = random.uniform(-RANGE, RANGE) * 100
            y2 = getTerrainHeight(x2, z2)
            self.entities.append(Entity(treeModel, (x2, y2, z2), 0.0, 0.0, 0.0, 3.0))
            x3 = random.uniform(-RANGE, RANGE) * 100
            z3 = random.uniform(-RANGE, RANGE) * 100
            y3 = getTerrainHeight(x3, z3)
            self.entities.append(Entity(fernModel, (x3, y3, z3), 0.0, 0.0, 0.0, 0.4, random.randint(0,3)))

        # Create Player Avatar
        rawChibi = ModelLoader().loadModel(self.loader, res_dir['MODELS']+"Chibi.obj")
        rawChibiTexture = ModelTexture(self.loader.loadTexture(res_dir['MODELS'] + "Chibi_Texture.png"))
        chibiModel = TexturedModel(rawChibi, rawChibiTexture)
        chibiTexture = chibiModel.getTexture()
        chibiTexture.setShineDamper(10)
        chibiTexture.setReflectivity(1)
        self.player = Player(chibiModel, (0.0, 0.0, 0.0), 0.0, 0.0, 0.0, 0.25, self.inputEvents, self.terrainTiles)
        self.entities.append(self.player)

        self.guis = []
        self.guiRenderer = GuiRenderer(self.loader)

        # Create a manager to display world objects
        self.renderer = MasterRenderer(self.loader, self.window_rect, self.inputEvents, self.player)
        ParticleMaster.init(self.loader, self.renderer.getProjectionMatrix(), self.renderer.getCamera())

        self.FBO = WaterFrameBuffers(self.window_size)
        self.waterRenderer = WaterRenderer(self.loader, self.renderer.getCamera(), self.FBO)
        self.water = WaterTile(self.loader, (13.0, -0.2, 12.25))

        gui = GuiTexture(self.loader.loadTexture(res_dir['TEXTURES'] + "claver-brand.png", False), (0.5, 0.5), (0.25, 0.25))
        self.guis.append(gui)
        self.FBO_initialized = False

        particleTexture = ParticleTexture(self.loader.loadTexture(res_dir['TEXTURE_PARTICLES'] + "particleAtlas.png", False), 4)
        self.system = ParticleSystem(particleTexture, pps=20.0, speed=15.0, gravityComplient=0.5, lifeLength=3, scale=1)
        self.system.randomizeRotation()
        self.system.setDirection((0.0, 1.0, 0.0), 0.1)
        self.system.setLifeError(0.1)
        self.system.setSpeedError(0.4)
        self.system.setScaleError(0.8)
        return True

    def on_render(self, gl_area, gl_context):
        if self.FBO_initialized is False:
            self.default_FBO = glGetIntegerv(GL_FRAMEBUFFER_BINDING)  # GLArea does not seem to use FBO 0 as the default.
            self.FBO.initializeFramebuffer(self.default_FBO, self.window_size)
            self.FBO_initialized = True

        self.renderer.processMovement(self.delta)

        if self.delta < 1:
            self.system.generateParticles((1.0, 1.0, 1.0), self.delta)

        ParticleMaster.update(self.delta, self.renderer.getCamera())

        glEnable(GL_CLIP_DISTANCE0)
        self.FBO.bindReflectionFrameBuffer()
        distance = 2 * (self.renderer.getCamera().getPosition().y - self.water.getHeight())
        self.renderer.getCamera().setCameraHeight(self.renderer.getCamera().getPosition().y - distance, True)
        self.renderer.renderScene(self.entities, self.normalMapEntities, self.terrainTiles, self.lights, self.running_seconds_from_start, Vector4((0, 1, 0, -self.water.getHeight() + 0.5)))
        self.renderer.getCamera().setCameraHeight(self.renderer.getCamera().getPosition().y + distance)

        self.FBO.bindRefractionFrameBuffer()
        self.renderer.renderScene(self.entities, self.normalMapEntities, self.terrainTiles, self.lights, self.running_seconds_from_start, Vector4((0, -1, 0, self.water.getHeight())))

        glDisable(GL_CLIP_DISTANCE0)
        self.FBO.unbindCurrentFrameBuffer()


        self.renderer.renderScene(self.entities, self.normalMapEntities, self.terrainTiles, self.lights, self.running_seconds_from_start, Vector4((0, -1, 0, 15)))
        self.waterRenderer.render(self.delta, self.water, self.sun)

        ParticleMaster.renderParticles()

        self.guiRenderer.render(self.guis)
        TextMaster.render()
        self.queue_draw()  # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        ParticleMaster.cleanUp()
        TextMaster.cleanUp()
        self.FBO.cleanUp()
        self.waterRenderer.cleanUp()
        self.guiRenderer.cleanUp()
        self.renderer.cleanUp()
        self.loader.cleanUp()

    def registerKeyPress(self, key):
        self.inputEvents.registerKeyboardEvent(key)

    def cancelKeyPress(self, key):
        self.inputEvents.cancelKeyboardEvent(key)

    def on_mouse_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.renderer.getCamera().decreaseZoom()
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.renderer.getCamera().increaseZoom()

    def on_mouse_movement(self, widget, event):
        state = event.get_state()
        if state & Gdk.ModifierType.BUTTON3_MASK or state & Gdk.ModifierType.BUTTON1_MASK:
            self.inputEvents.setCursorPosition((int(event.x_root), int(event.y_root)))

    def on_mouse_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1 or event.button == 3:
                if self.initializedCursor is False:
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
                    self.initializedCursor = True
                if event.button == 1:
                    self.inputEvents.registerButtonEvent(1)
                elif event.button == 3:
                    self.inputEvents.registerButtonEvent(3)

    def on_mouse_release(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and (event.button == 1 or event.button == 3):
            # Left mouse button
            widget.get_toplevel().get_window().set_cursor(self.custom_cursor)
            Gdk.Device.warp(self.device, self.screen, self.cursorCoords[0], self.cursorCoords[1])
            self.renderer.getCamera().deactivateWarp()
            self.renderer.getCamera().setLastMovePosition((int(event.x_root), int(event.y_root)))
            self.inputEvents.setCursorPosition((int(event.x_root), int(event.y_root)))
            self.initializedCursor = False
            if event.button == 1:
                self.inputEvents.cancelButtonEvent(1)
            elif event.button == 3:
                self.inputEvents.cancelButtonEvent(3)

    def on_resize(self, area, width, height):
        self.window_size = (width, height)
        self.FBO.resizeBuffer(width, height)
        self.renderer.windowResized(width, height)
        # display = Gdk.Display.get_default()
        # monitor = display.get_monitor_at_window(gl_area.get_window())
        # geometry = monitor.get_geometry()
        # scale_factor = monitor.get_scale_factor()
        # width = scale_factor * geometry.width
        # height = scale_factor * geometry.height
        # print("width:{} height:{}".format(width, height))