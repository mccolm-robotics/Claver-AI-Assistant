"""
Author: Praxis (McColm Robotics)
Title: Illuminated Rotating Chibi
Created: April 2020
Python interpreter: 3.7
GTK3 version: 3.24
PyCharm version: 2020.1
Platform: Ubuntu 19.10
"""

#from Claver_Program_Launcher import *
import gi, pyrr
import sys
import numpy as np
import pyassimp

gi.require_version('Gtk', '3.0')
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from gi.repository import Gtk, Gdk
from pyassimp import *
from pyassimp.helper import get_bounding_box
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image

class GLCanvas(Gtk.GLArea):
    def __init__(self):
        super().__init__()
        self.set_required_version(4, 5)             # Sets the version of OpenGL required by this OpenGL program
        self.connect("realize", self.on_initialize) # This signal is used to initialize the OpenGL state
        self.connect("unrealize", self.on_unrealize)  # Catch this signal to clean up buffer objects and shaders
        self.connect("render", self.on_render)      # This signal is emitted for each frame that is rendered
        self.connect("resize", self.on_resize)      # This signal is emitted when the window is resized
        self.add_tick_callback(self.tick)           # This is a frame time clock that is called each time a frame is rendered
        self.set_start_time = False                 # Boolean to track whether the clock has been initialized
        self.set_has_depth_buffer(True)
        # self.loader = Loader()

    def recur_node(self, node, level=0):
        print("  " + "\t" * level + "- " + str(node))
        for child in node.children:
            self.recur_node(child, level + 1)

    def view_pyassimp_model(self):
        # Begin Pyassimp functions
        print("SCENE:")
        print("   meshes: " + str(len(self.scene.meshes)))
        print("   total faces: %d" % sum([len(mesh.faces) for mesh in self.scene.meshes]))
        print("   materials: " + str(len(self.scene.materials)))
        print("   textures: " + str(len(self.scene.textures)))
        print("NODES:")
        self.recur_node(self.scene.rootnode)
        print("MESHES")
        for index, mesh in enumerate(self.scene.meshes):
            print("   MESH " + str(index+1))
            print("      material id: " + str(mesh.materialindex+1))
            print("      vertices: " + str(len(mesh.vertices)))
            print("      faces: " + str(len(mesh.faces)))
            print("      normals: " + str(len(mesh.normals)))
            # self.bb_min, self.bb_max = get_bounding_box(self.scene)
            # print("      bounding box:" + str(self.bb_min) + " - " + str(self.bb_max))
            #
            # self.scene_center = [(a + b) / 2. for a, b in zip(self.bb_min, self.bb_max)]
            # print("      scene center: ", self.scene_center)
            print("      first 3 verts:\n" + str(mesh.normals[:3]))
            if mesh.normals.any():
                print("      first 3 normals:\n" + str(mesh.normals[:3]))
            else:
                print("      no normals")
            print("      colors: " + str(len(mesh.colors)))
            self.tcs = mesh.texturecoords
            if self.tcs.any():
                for tc_index, tc in enumerate(self.tcs):
                    print("      texture-coords " + str(tc_index) + ": " + str(len(self.tcs[tc_index])) + "      first 3: " + str(self.tcs[tc_index][:3]))
            else:
                print("      no texture coordinates")
            print("      uv-component-count: " + str(len(mesh.numuvcomponents)))
            print("      faces: " + str(len(mesh.faces)) + " -> first 3:\n", mesh.faces[:3])
            print("      bones: " + str(len(mesh.bones)) + " -> first: " + str([str(b) for b in mesh.bones[:3]]))
        print("MATERIALS:")
        for index, material in enumerate (self.scene.materials):
            print("   MATERIAL (id: " + str(index+1) + ")")
            for key, value in material.properties.items():
                print("      %s: %s" % (key, value))
        print("TEXTURES:")
        for index, texture in enumerate(self.scene.textures):
            print("   TEXTURE " + str(index+1))
            print("      width: " + str(texture.width))
            print("      height: " + str(texture.height))
            print("      hint: " + str(texture.achformathint))
            print("      data (size): " + str(len(texture.data)))
        # End Pyassimp functions
        #print(help(pyassimp.structs.Face))
        #print(dir(pyassimp.structs.Face))

    def tick(self, widget, frame_clock):
        self.current_frame_time = frame_clock.get_frame_time()  # Gets the current timestamp in microseconds

        if self.set_start_time == False:                        # Initializes the timer at the start of the program
            self.last_frame_time = 0                            # Stores the previous timestamp
            self.frame_counter = 0                              # Counts the total frames rendered per seconds
            self.running_seconds_from_start = 0                 # Stores the cumulative running time of the program
            self.starting_time = self.current_frame_time        # Stores the timestamp set when the program was initalized
            self.set_start_time = True                          # Prevents the initialization routine from running again in this instance

        self.application_clock = (self.current_frame_time - self.starting_time)/1000000    # Calculate the total number of seconds that the program has been running

        self.frame_counter += 1                                         # The frame counter is called by GTK each time a frame is rendered. Keep track of how many are rendered.
        # Track how many Frames Per Second (FPS) are rendered
        if self.current_frame_time - self.last_frame_time > 1000000:    # Checks to see if 60 seconds have elapsed since the last counter reset
            print("\r" + str(self.frame_counter) + " FPS", end="")      # Prints out the number of frames rendered in the last second
            self.frame_counter = 0                                      # Resets the frame counter
            self.last_frame_time = self.current_frame_time              # Records the current timestamp to compare against for the next second
        return True                                                     # Returns true to indicate that tick callback should contine to be called

    def build_program(self):
        VERTEX_SHADER_SOURCE = """
            #version 450 core
            layout(location = 0) in vec4 vertex_position;
            layout(location = 1) in vec2 texture_position;
            layout(location = 2) in vec3 normal;
            layout(location = 3) out vec2 texture_coordinates;
            layout(location = 4) out vec3 surface_normal;
            layout(location = 5) out vec3 to_light_vector[4];
            uniform mat4 model_matrix;
            uniform mat4 view_matrix;
            uniform mat4 perspective_matrix;
            uniform vec3 light_position[4];
            uniform float useFakeLighting;
            void main()
            {
                vec4 world_position_matrix = model_matrix * vertex_position;
                gl_Position = perspective_matrix * view_matrix * world_position_matrix;
                texture_coordinates = texture_position;
                vec3 actualNormal = normal;
                if(useFakeLighting > 0.5){
                    actualNormal = vec3(0.0, 1.0, 0.0);
                }
                surface_normal = (model_matrix * vec4(actualNormal, 0.0)).xyz;
                for(int i=0; i<4; i++){
                    to_light_vector[i] = light_position[i] - world_position_matrix.xyz;
                }
            }
        """
        FRAGMENT_SHADER_SOURCE = """
            #version 450 core
            layout(location = 3) in vec2 texture_coordinates;
            layout(location = 4) in vec3 surface_normal;
            layout(location = 5) in vec3 to_light_vector[4];
            out vec4 out_colour;
            uniform sampler2D samplerTexture;
            uniform vec3 light_colour[4];
            uniform vec3 attenuation[4];
            uniform float shineDamper;
            uniform float reflectivity;
            void main()
            {
                vec3 unitNormal = normalize(surface_normal);
                vec3 unitVec torToCamera = normalize(toCameraVector);
                
                vec3 totalDiffuse = vec3(0.0);
                vec3 totalSpecular = vec3(0.0);
                
                for(int i=0; i<4; i++){
                float distance = length(toLightVector[i]);
                    vec3 unitLightVector = normalize(to_light_vector[i]);
                    float attFactor = attenuation[i].x + (attenuation[i].y * distance) + (attenuation[i].z * distance * distance);
                    float nDot1 = dot(unitNormal,unitLightVector);
                    float brightness = max(nDot1,0.0);
                    vec3 lightDirection = -unitLightVector;
                    vec3 reflectedLightDirection = reflect(lightDirection, unitNormal);
                    float specularFactor = dot(reflectedLightDirection, unitVectorToCamera);
                    specularFactor = max(specularFactor, 0.0);
                    float dampedFactor = pow(specularFactor, shineDamper);
                    totalDiffuse = totalDiffuse + (brightness * light_colour[i])/attFactor;
                    totalSpecular = totalSpecular + (dampedFactor * reflectivity * lightColour[i])/attFactor;
                }
                totalDiffuse = max(totalDiffuse, 0.3);
                
                vec4 textureColour = texture(samplerTexture, texture_coordinates);
                if(textureColour.a < 0.5){
                    discard;
                }
                
                out_colour = vec4(totalDiffuse,1.0) * textureColour;
            }
        """
        # self.shader = StaticShader("vertexShader", "fragmentShader")
        # These are helper functions provided by PyOpenGL
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)           # Compiles the vertex shader into intermediate binary representation
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)     # Compiles the fragment object into intermediate binary representation
        self.shader = compileProgram(vertex_shader, fragment_shader)                    # Links the vertex and fragment shader objects together into a program
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        # Bind attributes
        self.vertexLocationInShader = glGetAttribLocation(self.shader, 'vertex_position')
        self.textureLocationInShader = glGetAttribLocation(self.shader, 'texture_position')
        self.normalLocationInShader = glGetAttribLocation(self.shader, "normal")
        # Bind uniforms
        self.modelMatrixLocationInShader = glGetUniformLocation(self.shader, "model_matrix")
        self.viewMatrixLocationInShader = glGetUniformLocation(self.shader, "view_matrix")
        self.perspectiveMatrixLocationInShader = glGetUniformLocation(self.shader, "perspective_matrix")
        self.lightPositionLocationInShader = glGetUniformLocation(self.shader, "light_position")
        self.lightColourLocationInShader = glGetUniformLocation(self.shader, "light_colour")
        self.useFakeLightingLocationInShader = glGetUniformLocation(self.shader, "useFakeLighting")

    def load_geometry(self):

        self.scene = load('models/char_01_triangulated.obj')
        self.blenderModel = self.scene.meshes[0]
        print("Name of model being loaded: ", self.blenderModel)
        self.model = np.concatenate((self.blenderModel.vertices, self.blenderModel.normals, self.blenderModel.texturecoords[0]), axis=0)

        self.vertices_offset = 0
        self.normal_offset = self.model.itemsize * len(self.blenderModel.vertices) * 3
        self.texture_offset = self.normal_offset + (self.model.itemsize * len(self.blenderModel.texturecoords[0]) * 3) # Assimp represents the texture as a vec3 (u, v, 0)


        self.vertex_array_object = GLuint()                                 # Stores the name of the vertex array object
        glCreateVertexArrays(1, ctypes.byref(self.vertex_array_object))     # Creates the vertex array object and initalizes it to default values
        glBindVertexArray(self.vertex_array_object)

        # Creates a buffer to hold the vertex data and binds it to the OpenGL pipeline
        self.vertex_buffer_object = GLuint()                           # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(self.vertex_buffer_object))    # Generates a buffer to hold the vertex data
        glNamedBufferStorage(self.vertex_buffer_object, self.model.nbytes, self.model, GL_MAP_READ_BIT) # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_object)       # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glEnableVertexAttribArray(self.vertexLocationInShader)
        # self.model.itemsize*3 specifies the stride (how to step through the data in the buffer). This is important for telling OpenGL how to step through a buffer having concatinated vertex and color data (see: https://youtu.be/bmCYgoCAyMQ).
        # This function puts the VBO into the VAO
        glVertexAttribPointer(self.vertexLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.vertices_offset))

        # Describe the position data layout in the buffer
        glEnableVertexAttribArray(self.textureLocationInShader)
        glVertexAttribPointer(self.textureLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.texture_offset))

        glEnableVertexAttribArray(self.normalLocationInShader)
        glVertexAttribPointer(self.normalLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.normal_offset))

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open("models/Chibi_Texture_D.png")
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(flipped_image.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        image.close()
        #glDisableVertexAttribArray(self.vertex_position_attribute)
        #glDisableVertexAttribArray(self.texture_in)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.view_pyassimp_model()

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

        glEnable(GL_DEPTH_TEST) # Enable depth testing to ensure pixels closer to the viewer appear closest
        glDepthFunc(GL_LESS)    # Set the type of calculation used by the depth buffer
        glEnable(GL_CULL_FACE)  # Enable face culling
        glCullFace(GL_BACK)     # Discard the back faces of polygons (determined by the vertex winding order)

        # self.model = ModelLoader.loadModel("filename.fbx", self.loader)
        # self.texture = ModelTexture(loader.loadTexture("models/Chibi_Texture_D.png"))
        # chibiModel = TexturedModel(self.model, self.texture)

        # Snippet: grass.getTexture().setHasTransparency(true)
        # Snippet: modelTextureAtlas = ModelTexture(self.loader.loadTexture("file.png"))
        # Snippet: modelTextureAtlas.setNumberOfRows(2)

        # self.guis = []
        # gui = GuiTexture(loader.loadTexture("textureName"), (0.5, 0.5), (0.25, 0.25))
        # self.guis.append(gui)
        # self.guiRenderer = GuiRenderer(self.loader)

        # texture = texturedModel.getTexture()
        # texture.setShineDamper(10)
        # texture.setReflectivity(1)
        # self.entity = Entity(texturedModel,yghujikoljuyhik, atlas# (0, 0, -1), 0, 0, 0, 1)

        # light = Light([0, 10000, -7000], [1.0, 1.0, 1.0]) # This is the sun
        # lights = []
        # lights.append(light)
        # lights.append(Light([-200, 10, -200], [10.0, 0.0, 0.0], [1.0, 0.01, 0.002]))
        # lights.append(Light([200, 10, 200], [0.0, 0.0, 10.0], [1.0, 0.01, 0.002]))


        # self.camera = Camera()

        # self.renderer = MasterRenderer(self.loader)

        self.build_program()      # Calls build_program() to compile and link the shaders
        self.load_geometry()      # Calls load_geometry() to create vertex and colour data

        # Get information about current GTK GLArea canvas
        window = gl_area.get_allocation()
        # Construct perspective matrix using width and height of window allocated by GTK
        self.perspective_matrix = Matrix44.perspective_projection(45.0, window.width / window.height, 0.1, 200.0)

        glUseProgram(self.shader)
        glUniformMatrix4fv(self.perspectiveMatrixLocationInShader, 1, GL_FALSE, self.perspective_matrix)

        glUseProgram(0)

        #aiFace.indices = [aiFace.mIndices[i] for i in range(aiFace.mNumIndices)]
        #faces = [f.indices for f in target.faces]

        return True

    def on_render(self, gl_area, gl_context):


        glClearColor(0.0, 0.0, 0.0, 0.0)    # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER

        eye = (0.0, 5, 18.0)        # Eye coordinates (location of the camera)
        target = (0.0, 7.0, 0.0)    # Target coordinates (where the camera is looking)
        up = (0.0, 1.0, 0.0)        # A vector representing the 'up' direction.


        view_matrix = Matrix44.look_at(eye, target, up) # Calculate the view matrix
        model_matrix = Matrix44.from_translation([0.0, 0.0, 0.0]) * pyrr.matrix44.create_from_axis_rotation((0.0, 1.0, 0.0), self.application_clock) * Matrix44.from_scale([1.0, 1.0, 1.0])

        # self.camera.move()
        # for entity in list_of_entities_to_render:
        #     self.renderer.processEntity(entity)
        # self.renderer.render(self.lights, self.camera)
        # self.guiRenderer.render(self.guis)

        glUseProgram(self.shader)  # Tells OpenGL to use the shader program for rendering geometry
        glUniformMatrix4fv(self.viewMatrixLocationInShader, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(self.modelMatrixLocationInShader, 1, GL_FALSE, model_matrix)
        glUniform3f(self.lightPositionLocationInShader, 0.0, 3.0, 10.0)
        glUniform3f(self.lightColourLocationInShader, 1.0, 1.0, 1.0)
        glUniform1f(self.useFakeLightingLocationInShader, 0.0)
        glBindVertexArray(self.vertex_array_object)                                             # Binds the self.vertex_array_object to the OpenGL pipeline vertex target
        glDrawArrays(GL_TRIANGLES, 0, len(self.blenderModel.vertices))

        glBindVertexArray(0)
        glUseProgram(0)  # Tells OpenGL to use the shader program for rendering geometry

        self.queue_draw()   # Schedules a redraw for Gtk.GLArea

    def on_unrealize(self, gl_area):
        # self.guiRenderer.cleanUp()
        # self.renderer.cleanUp()
        # self.loader.cleanUp()
        release(self.scene)  # Pyassimp function
        glDeleteVertexArrays(1, self.vertex_array_object)
        glDeleteBuffers(1, self.vertex_buffer_object)
        glDeleteTextures(self.texture)
        glDeleteProgram(self.shader)

    def on_resize(self, area, width, height):
        # Field of view, aspect ration, distance to near, distance to far
        self.perspective_matrix = Matrix44.perspective_projection(45.0, width / height, 0.1, 200.0) # Recalculate the perspective matrix when the window is resized
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.perspectiveMatrixLocationInShader, 1, GL_FALSE, self.perspective_matrix)
        glUseProgram(0)


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