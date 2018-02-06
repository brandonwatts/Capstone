class ApiResponseBuilder:

    def __init__(self):
        self.data = {}

    def build(self):
        api_response = ApiResponse(**self.data)
        return api_response

    def add_extraction_point(self, name, value):
        self.data[name] = value


class ApiResponse(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)