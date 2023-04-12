from abc import *

class preprocessor(metaclass=ABCMeta):
    @abstractclassmethod
    def preprocess(self):
        pass