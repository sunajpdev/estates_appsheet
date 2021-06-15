from sqlalchemy import Column, Integer, Float, Text, DateTime
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.functions import current_timestamp

from settings_database import Base


class Estate(Base):
    __tablename__ = "estates"
    id = Column(Text, primary_key=True)
    note = Column(Text, unique=False)
    price = Column(Integer, unique=False)
    shop = Column(Text, unique=False)
    place = Column(Text, unique=False)
    prefecture = Column(Text, unique=False)
    city = Column(Text, unique=False)
    station = Column(Text, unique=False)
    route = Column(Text, unique=False)
    work = Column(Text, unique=False)
    area = Column(Float, unique=False)
    buildingarea = Column(Float, unique=False)
    ldk = Column(Text, unique=False)
    buildingyear = Column(Text, unique=False)
    url = Column(Text, unique=False)
    # created= Column(DateTime, nullable=False, server_default=current_timestamp)
    created = Column(DateTime)

    def __init__(
        self,
        id=None,
        note=None,
        price=None,
        shop=None,
        place=None,
        prefecture=None,
        city=None,
        station=None,
        route=None,
        work=None,
        area=None,
        buildingarea=None,
        ldk=None,
        buildingyear=None,
        url=None,
        created=None,
    ):
        self.id = id
        self.note = note
        self.price = price
        self.shop = shop
        self.place = place
        self.prefecture = prefecture
        self.city = city
        self.station = station
        self.route = route
        self.work = work
        self.area = area
        self.buildingarea = buildingarea
        self.ldk = ldk
        self.buildingyear = buildingyear
        self.url = url
        self.created = created
