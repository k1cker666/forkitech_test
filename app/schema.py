from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TRXAdressAddSchema(BaseModel):
    trx_adress: str = Field(min_length=34, max_length=34, pattern=r"^T[A-Za-z1-9]{33}$")

class TRXAdressSchema(TRXAdressAddSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    id: int
    added_at: datetime