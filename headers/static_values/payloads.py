import os

class Payloads():

    Payload_List = []

    def __init__(self):
        pass

    @staticmethod
    def get_payload_list(ip_address=None, port_number=None):
        if not Payloads.Payload_List:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, 'payloads.txt')

            with open(filename) as type_file:
                Payloads.Payload_List = type_file.read().splitlines()

        if ip_address and port_number:
            Payloads.Payload_List = [x.format(ip_address, port_number) for x in Payloads.Payload_List]
            
        return Payloads.Payload_List