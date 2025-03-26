from pydantic import BaseModel, Field


class TRXAdressAddSchema(BaseModel):
    trx_adress: str = Field(min_length=34, max_length=34, pattern=r"^T[A-Za-z1-9]{33}$")

class TRXAdressSchema(TRXAdressAddSchema):
    id: int