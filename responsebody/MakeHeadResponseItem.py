from pydantic import BaseModel, Field
from fastapi_camelcase import CamelModel
class MakeHeadResponseItem(CamelModel):
    toonify_url : str
    head_url : str
    result : int