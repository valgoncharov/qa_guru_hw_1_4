class Server:
    def __init__(self, env):
        self.app = {
            "dev": "http://127.0.0.1:8002",
            "stage": "http://127.0.0.1:8002",
            "prod": "http://127.0.0.1:8002",
        }[env]