import hashlib
import hmac
import json
import os
import random
import requests
import time
import yaml


class Client:
    def __init__(self, MMOS_API_KEY, MMOS_API_SECRET, **kwargs):
        self.protocol = "https"
        self.host = "api.depo.mmos.blue"
        self.port = 443
        self.version = "v2"
        self.game = "dev-yvan-le-bras-mnhn-fr"
        self.apiKey = {"key": MMOS_API_KEY, "secret": MMOS_API_SECRET}

        self.playerCode = "YVAN001"
        self.projectCode = "spipoll-fly"
        self.urlBase = "%s://%s" % (self.protocol, self.host)

    def digest(self, key, data):
        h = hmac.new(bytes(str(key).encode("utf-8")), digestmod=hashlib.sha256)
        h.update(data.encode("utf-8"))
        return h.hexdigest()

    def build_headers(self, method, path, body={}):
        CONTENT_SEPARATOR = "|"
        SIGNING_ALGORITHM = "MMOS1-HMAC-SHA256"
        nonce = random.randint(0, 1000000000)
        timestamp = int(time.time() * 1000)

        # timestamp = 1567416082496
        # nonce = 222773350332

        contentParts = [
            SIGNING_ALGORITHM,
            self.apiKey["key"],
            timestamp,
            nonce,
            method,
            path,
            json.dumps(body, separators=(",", ":")),
        ]
        content = CONTENT_SEPARATOR.join(map(str, contentParts))

        signingKey = self.digest(timestamp, self.apiKey["secret"])
        signature = self.digest(signingKey, content)

        return {
            "Content-Type": "application/json",
            "X-MMOS-Algorithm": SIGNING_ALGORITHM,
            "X-MMOS-Credential": self.apiKey["key"],
            "X-MMOS-Timestamp": str(timestamp),
            "X-MMOS-Nonce": str(nonce),
            "X-MMOS-Signature": signature,
        }

    def info(self):
        path = "/"
        body = {}
        headers = self.build_headers("GET", path, body)
        r = requests.get(self.urlBase + path, headers=headers, data=body)
        return r.json()

    def create_task(self):
        path = "/games/%s/players/%s/tasks" % (self.game, self.playerCode)
        body = {
            "projects": [self.projectCode],
            "player": {"accountCode": self.playerCode},
        }
        headers = self.build_headers("POST", path, body)
        r = requests.post(self.urlBase + path, headers=headers, json=body)
        return r.json()

    def classify(self, sex, task_created, task_id):
        path = "/classifications"
        body = {
            "game": self.game,
            # "taskId": task_id,
            # "playerCode": self.playerCode,
            "playergroup": "group1122",
            # "result": {"gender": sex},
            "circumstances": {"t": int((time.time() * 1000) - task_created)},
            "task": {"id": task_id, "result": {"gender": sex}},
            "player": self.playerCode,
            # "playergroup": "group1122",
        }
        headers = self.build_headers("POST", path, body)
        r = requests.post(self.urlBase + path, headers=headers, json=body)
        return r.json()


if __name__ == "__main__":
    with open(os.environ.get("CONFIG_PATH", "./config.yaml"), "r") as f:
        config = yaml.safe_load(f)

    m = Client(**config)
    __import__("pprint").pprint(m.info())
    __import__("pprint").pprint(m.create_task())
