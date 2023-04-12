from fastapi_camelcase import CamelModel

class MakeHeadRequestItem(CamelModel):
    photo_url : str
    style_code : str
