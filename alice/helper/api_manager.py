import requests
import simplejson as json

class ApiManager(object):
    @staticmethod
    def get(url, headers, data=None):
        response = requests.get(url, headers=headers, data=data)
        return {"status_code": response.status_code, "content": response.content, "response": response}


    @staticmethod
    def post(url, headers, data=None):
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return {"status_code": response.status_code, "content": response.content, "response": response}




