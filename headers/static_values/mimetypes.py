import os

class MimeTypes():

    Type_List = []

    def __init__(self):
        pass

    @staticmethod
    def get_mime_list():
        if not MimeTypes.Type_List:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, 'mimetypes.txt')
            
            with open(filename) as type_file:
                MimeTypes.Type_List = type_file.read().splitlines()
            
        return MimeTypes.Type_List