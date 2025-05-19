from sqlalchemy import Column, Float, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("activities.id"), nullable=True)

    children = relationship("Activity", back_populates="parent")
    parent = relationship("Activity", back_populates="children", remote_side=[id])


organization_activity = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", String, ForeignKey("organizations.id")),
    Column("activity_id", String, ForeignKey("activities.id")),
)


organization_phone = Table(
    "organization_phones",
    Base.metadata,
    Column("organization_id", String, ForeignKey("organizations.id"), primary_key=True),
    Column("phone_number", String, primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity)
    phone_numbers = relationship("OrganizationPhone", back_populates="organization")


class OrganizationPhone(Base):
    __table__ = organization_phone

    organization = relationship("Organization", back_populates="phone_numbers")
