class PreRequest():
    def __init__(self, req_type=None, destination=None, payload=None, headers=None, cookies={}, body=None, expected_status_code=200):
        self.req_type             = req_type
        self.destination          = destination
        self.payload              = payload
        self.headers              = headers
        self.cookies              = cookies
        self.body                 = body
        self.expected_status_code = expected_status_code