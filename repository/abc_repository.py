from abc import *

class repository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_body_url(self):
        pass
    
    @abstractclassmethod
    def get_hair_url(self):
        pass
    
    @abstractclassmethod
    def get_body_config(self):
        pass
    
    @abstractclassmethod
    def get_hair_config(self):
        pass
    