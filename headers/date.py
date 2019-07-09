from headers.static_values import *
from worker import *
from utils import *
import requests

class Date():

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
                        "Date" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def date_fuzz_tests(self):
        date_fuzz = [
            "Wed, 21 Oct 2015 07:28:00 GMT",
            "Wed, 21 Oct 1800 07:28:00 GMT",
            "Wed, 21 Oct 0 07:28:00 GMT",
            "Wed, 21 Oct -1 07:28:00 GMT",
            "Wed, 21 Oct 9999 07:28:00 GMT",
            "Wed, 21 Oct 999999999 07:28:00 GMT",
            "Abc, 21 Oct 2015 07:28:00 GMT",
            "Wed, 21 Abc 2015 07:28:00 GMT",
            "Wed, 21 Oct 2015 99:28:00 GMT",
            "Wed, 21 Oct 2015 07:99:00 GMT",
            "Wed, 21 Oct 2015 07:28:99 GMT",
            "Wed, 21 Oct 2015 07:28:00 Abc",
            "Wed, 21 Oct 2015 077:28:00 GMT",
            "Wed, 21 Oct 2015 07:288:00 GMT",
            "Wed, 21 Oct 2015 07:28:9999 GMT"
        ]

        for date in date_fuzz:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = date,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        "Date" : date
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.date_fuzz_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array