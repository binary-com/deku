import logging

class Client:
    def __init__(self, client):
        self.client = client

    def is_running(self):
        try:
            return self.client.ping()
        except Exception as e:
            logging.warn('Docker service is down: %s' % (e))
