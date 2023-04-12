from abc import *

class storage(metaclass=ABCMeta):
    @abstractclassmethod
    def file_download(self):
        pass
    
    @abstractclassmethod
    def file_upload(self):
        pass
    