from pathlib import Path
from .camera import *


class Singleton:
    """Alex Martelli implementation of Singleton (Borg)
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class stagePositions():
    def __init__(self, x, y, z1, af, z2):
        self.x = x
        self.y = y
        self.z1 = z1
        self.af = af
        self.z2 = z2


class configHelper(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        if self.hasLoaded():
            pass
        else:
            self._loaded = True
            self.top_left = None
            self.top_right = None
            self.bottom_left = None
            self.path = str(Path.home())

            self.invert_x = False
            self.invert_y = False

            self.num_rows = 10
            self.num_cols = 20
            self.x_dir_offset = 300
            self.y_dir_offset = 300
            self.row_offset = 0
            self.row_count_offset = 0

            self.height = 1412
            self.width = 1412
            self.pixel_size = 11
            self.x_per_overlap = 10
            self.y_per_overlap = 10
            self.camera = prime95BCamera()
            self.magnification = 10

            self.stg_positions = []

            self.available_cameras = {"Prime 95B": prime95BCamera(),
                                      "Orca Fusion": orcaFusionCamera(),
                                      "Orca Flash": orcaFlashCamera(),
                                      "CoolSNAP EZ": coolsnapEZCamera()}

    def hasLoaded(self):
        return hasattr(self, "_loaded")


