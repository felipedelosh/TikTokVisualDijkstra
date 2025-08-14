"""
FelipedelosH
2025
"""
import os
from os import scandir

class Controller:
    def __init__(self):
        self.path = str(os.path.dirname(os.path.abspath(__file__)))
        self._graphsPaths = f"{self.path}/INPUT"
        self.w = 405
        self.h = 720

    def getWindowSize(self):
        return f"{self.w}x{self.h}"
    
    def loadGraphFiles(self):
        _filesNames = []

        try:
            for i in scandir(self._graphsPaths):
                if i.is_file():
                    if ".json" in i.name:
                        _filesNames.append(i.name)
        except:
            pass

        return _filesNames
