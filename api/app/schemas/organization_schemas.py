from app.schemas.base_schema import BaseSchema


class OrganizationBase(BaseSchema):
    id: str
    name: str
