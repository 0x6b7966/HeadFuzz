import requests
import logging
import time
import json
from utils import *

class Executor():
    def __init__(self):
        pass

    def execute(self, pre_request):

        try:
            for key, value in Config.static_cookies.items():
                pre_request.cookies[key] = value

            start = time.time()

            # ======= START =======

            if pre_request.req_type is "GET":
                response = requests.get(
                    pre_request.destination,
                    headers=pre_request.headers,
                    cookies=pre_request.cookies
                )
            elif pre_request.req_type is "POST":
                response = requests.post(
                    pre_request.destination,
                    headers=pre_request.headers,
                    cookies=pre_request.cookies,
                    data=pre_request.body
                )
            elif pre_request.req_type is "PUT":
                response = requests.put(
                    pre_request.destination,
                    headers=pre_request.headers,
                    cookies=pre_request.cookies,
                    data=pre_request.body
                )
            elif pre_request.req_type is "PATCH":
                response = requests.patch(
                    pre_request.destination,
                    headers=pre_request.headers,
                    cookies=pre_request.cookies,
                    data=pre_request.body
                )

            # ========= END =========

            end = time.time()

            if pre_request.expected_status_code in Config.http_codes:
                expected_code_str = str(pre_request.expected_status_code) + " (" + Config.http_codes[pre_request.expected_status_code] +")"
            else:
                expected_code_str = str(pre_request.expected_status_code) + " (Unknown Code)"

            if response.status_code in Config.http_codes:
                response_code_str = str(response.status_code) + " (" + Config.http_codes[response.status_code] + ")"
            else:
                response_code_str = str(response.status_code) + " (" + response.reason + ")"

            if str(response.status_code) in Config.exclude_code:
                Config.logger.info("Returning because of exclude code: " + str(response.status_code))
                return

            if Config.include_code:
                if str(response.status_code) not in Config.include_code:
                    Config.logger.info("Returning because of include code: " + str(response.status_code))
                    return

            if response.status_code != pre_request.expected_status_code:
                log_string  = ""
                log_string += "===============================================================================>>\n"
                log_string += "Event Type: Server Response Changed" + "\n"
                log_string += "Request Type: " + pre_request.req_type + "\n"
                log_string += "Execution Time: " + str(end - start) + "\n"
                log_string += "Expected Code: " + expected_code_str + "\n"
                log_string += "Response Code: " + response_code_str + "\n"
                log_string += "Payload: " + str(pre_request.payload) + "\n"
                log_string += "Headers: " + str(pre_request.headers) + "\n"
                log_string += "Cookies: " + str(pre_request.cookies) + "\n"

                Config.logger.info(log_string)

            if type(pre_request.payload) is dict:
                for key, value in pre_request.payload.items():
                    if value in response.text and value not in Config.initial_response.text:
                        log_string  = ""
                        log_string += "===============================================================================>>\n"
                        log_string += "Event Type: Reflective Header" + "\n"
                        log_string += "Request Type: " + pre_request.req_type + "\n"
                        log_string += "Execution Time: " + str(end - start) + "\n"
                        log_string += "Expected Code: " + expected_code_str + "\n"
                        log_string += "Response Code: " + response_code_str + "\n"
                        log_string += "Payload: " + str(key) + " : " + str(value) + "\n"
                        log_string += "Headers: " + str(pre_request.headers) + "\n"
                        log_string += "Cookies: " + str(pre_request.cookies) + "\n"

                        Config.logger.info(log_string)
            else:
                if pre_request.payload in response.text and pre_request.payload not in Config.initial_response.text:
                    log_string  = ""
                    log_string += "===============================================================================>>\n"
                    log_string += "Event Type: Reflective Header" + "\n" 
                    log_string += "Request Type: " + pre_request.req_type + "\n"
                    log_string += "Execution Time: " + str(end - start) + "\n"
                    log_string += "Expected Code: " + expected_code_str + "\n"
                    log_string += "Response Code: " + response_code_str + "\n"
                    log_string += "Payload: " + str(pre_request.payload) + "\n"
                    log_string += "Headers: " + str(pre_request.headers) + "\n"
                    log_string += "Cookies: " + str(pre_request.cookies) + "\n"

                    Config.logger.info(log_string)

            

        except Exception:
            Config.logger.debug("Error occured in executor function!", exc_info=True)