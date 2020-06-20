import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/res/"

res_dir = dict(
    LOADER_GUI=RES_FOLDER + "interface/program_loader/",
    FONT_ATLAS=RES_FOLDER + "fonts/atlas/",
    TEXTURES=RES_FOLDER + "textures/",
    MODELS=RES_FOLDER + "models/",
    SKYBOX_CLOUDS=RES_FOLDER + "skybox/clouds/",
    SKYBOX_NIGHT=RES_FOLDER + "skybox/night/",
    HEIGHT_MAPS=RES_FOLDER + "heightmaps/"
)
