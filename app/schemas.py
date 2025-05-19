from typing import Optional, List
from pydantic import BaseModel


class BuildingBase(BaseModel):
    latitude: float
    longitude: float
    address: str


class Building(BuildingBase):
    id: str

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[str]


class Activity(ActivityBase):
    id: str
    children: List["Activity"] = []

    class Config:
        from_attributes = True


Activity.model_rebuild()


class ActivityTree(Activity):
    level: int


class ActivityWithOrganizations(Activity):
    organizations_count: int


class PhoneNumber(BaseModel):
    number: str


class OrganizationBase(BaseModel):
    name: str
    building_id: str
    phone_numbers: List[str]
    activity_ids: List[str]


class Organization(OrganizationBase):
    id: str
    building: Building
    activities: List[Activity]

    class Config:
        from_attributes = True


class OrganizationWithDistance(Organization):
    distance: float


class OrganizationSearchResult(BaseModel):
    results: List[Organization]
    total: int
