from fastapi_camelcase import CamelModel

class AlignFaceRequestBody(CamelModel):
    photo_url : str