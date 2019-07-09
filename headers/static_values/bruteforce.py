import os
from base64 import b64encode

class BruteForce():

    UserPass_List = []

    def __init__(self):
        pass

    @staticmethod
    def get_userpass_list():
        if not BruteForce.UserPass_List:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, 'userpass.txt')
            
            with open(filename) as type_file:
                BruteForce.UserPass_List = type_file.read().splitlines()
                BruteForce.UserPass_List = [userpass.replace(" ", ":") for userpass in BruteForce.UserPass_List]
                BruteForce.UserPass_List = [b64encode(userpass.encode()).decode() for userpass in BruteForce.UserPass_List]
        
        return BruteForce.UserPass_List