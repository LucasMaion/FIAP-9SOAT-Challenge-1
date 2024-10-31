from pydantic import BaseModel


class CreateClientSchema(BaseModel):
    name: str
    email: str
    document: str
