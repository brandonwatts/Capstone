from Api.Models.ApiResponse import ApiResponse

class ApiResponseBuilder:

    def __init__(self):
        self.data = {}

    def build(self):
        api_response = ApiResponse(**self.data)
        return api_response

    def add_extraction_point(self, name, value):
        self.data[name] = value


