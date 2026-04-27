from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.types import DOUBLE, BIGINT

class Client(SQLModel, table=True):
    __tablename__ = 'clients'
    id: int|None = Field(default=None, primary_key=True)
    cid: str = Field(unique=True, index=True)
    ua: str|None

    locations: list['Location'] = Relationship(back_populates='client')  # `client`はLocationの属性名

class Location(SQLModel, table=True):
    __tablename__ = 'locations'
    id: int|None = Field(default=None, primary_key=True)
    timestamp: int = Field(sa_type=BIGINT)
    latitude: float = Field(sa_type=DOUBLE)
    longitude: float = Field(sa_type=DOUBLE)
    distance: float|None = Field(default=None, sa_type=DOUBLE)
    address: str
    client_id: int|None = Field(default=None, foreign_key='clients.id')

    client: Client|None = Relationship(back_populates='locations')  # `locations`はClientの属性名
