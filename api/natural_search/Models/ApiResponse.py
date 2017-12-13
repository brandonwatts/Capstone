"""APIResponse.py is the response the the api/nlp endpoint"""


class ApiResponse(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
