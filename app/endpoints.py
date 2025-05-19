from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud, schemas
from .database import get_async_session

router = APIRouter()


@router.get(
    "/buildings/{building_id}/organizations",
    response_model=List[schemas.OrganizationBase],
)
async def get_organizations_in_building(
    building_id: str, db: AsyncSession = Depends(get_async_session)
):
    organizations_in_building = await crud.get_organizations_by_building(
        db, building_id=building_id
    )
    return organizations_in_building


@router.get(
    "/organizations/nearby",
    response_model=List[schemas.OrganizationBase],
)
async def get_organizations_nearby(
    lat: float,
    lon: float,
    radius: float,
    db: AsyncSession = Depends(get_async_session),
):

    organizations_in_radius = await crud.get_organizations_in_radius(
        db, lat=lat, lon=lon, radius=radius
    )

    return organizations_in_radius


@router.get(
    "/organizations/by-activity/{activity_id}",
    response_model=List[schemas.OrganizationBase],
)
async def get_organizations_by_activity(
    activity_id: str, db: AsyncSession = Depends(get_async_session)
):
    organizations_by_activity = await crud.get_organizations_by_activity(
        db, activity_id=activity_id
    )
    return organizations_by_activity


@router.get("/organizations/{organization_id}", response_model=schemas.OrganizationBase)
async def get_organization_by_id(
    organization_id: str, db: AsyncSession = Depends(get_async_session)
):
    organization = await crud.get_organization_by_id(db, organization_id)

    return organization


@router.get("organizations/by_activity", response_model=List[schemas.OrganizationBase])
async def get_organizations_by_activity(
    activity_name: str = None, db: AsyncSession = Depends(get_async_session)
):
    if activity_name:
        organizations = await crud.get_organizations_by_name_activity(db, activity_name)
        return organizations
    return []


@router.get("/organizations/search", response_model=List[schemas.OrganizationBase])
async def search_organizations(
    name: str = None, db: AsyncSession = Depends(get_async_session)
):
    if name:
        organizations = await crud.search_organizations_by_name(db, name=name)
        return organizations
    return []
