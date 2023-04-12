from fastapi_camelcase import CamelModel

class CombinAvatarRequestBody(CamelModel):
    head_url : str
    body_num : int
    hair_num : int
