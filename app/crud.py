from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import (
    Building,
    Activity,
    Organization,
    organization_activity,
)


async def get_building(db: AsyncSession, building_id: str):
    result = await db.execute(select(Building).where(Building.id == building_id))
    return result.scalars().first()


async def get_buildings(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Building).offset(skip).limit(limit))
    return result.scalars().all()


async def get_buildings_in_radius(
    db: AsyncSession, latitude: float, longitude: float, radius: float
):
    query = select(Building).where(
        (Building.latitude.between(latitude - radius, latitude + radius))
        & (Building.longitude.between(longitude - radius, longitude + radius))
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_child_activities(db: AsyncSession, parent_id: str, max_level: int = 3):
    if max_level <= 0:
        return []

    result = await db.execute(select(Activity).where(Activity.parent_id == parent_id))
    children = result.scalars().all()

    all_children = list(children)
    for child in children:
        child_children = await get_child_activities(db, child.id, max_level - 1)
        all_children.extend(child_children)

    return all_children


async def get_organization(db: AsyncSession, organization_id: str):
    result = await db.execute(
        select(Organization).where(Organization.id == organization_id)
    )
    return result.scalars().first()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    return result.scalars().all()


async def get_organizations_by_building(db: AsyncSession, building_id: str):
    result = await db.execute(
        select(Organization)
        .where(Organization.building_id == building_id)
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
    )
    organizations = result.scalars().all()

    return [
        {
            "id": org.id,
            "name": org.name,
            "building_id": org.building_id,
            "phone_numbers": [pn.phone_number for pn in org.phone_numbers],
            "activity_ids": [act.id for act in org.activities],
        }
        for org in organizations
    ]


async def get_organizations_by_activity(db: AsyncSession, activity_id: str):
    activities = await get_child_activities(db, activity_id)
    activity_ids = [activity.id for activity in activities] + [activity_id]

    result = await db.execute(
        select(Organization, organization_activity.c.activity_id)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(activity_ids))
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
    )

    organizations = result.scalars().all()

    return [
        {
            "id": org.id,
            "name": org.name,
            "building_id": org.building_id,
            "phone_numbers": [pn.phone_number for pn in org.phone_numbers],
            "activity_ids": [act.id for act in org.activities],
        }
        for org in organizations
    ]


async def search_organizations_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(Organization)
        .where(Organization.name.ilike(f"%{name}%"))
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
    )
    organizations = result.scalars().all()
    return [
        {
            "id": org.id,
            "name": org.name,
            "building_id": org.building_id,
            "phone_numbers": [pn.phone_number for pn in org.phone_numbers],
            "activity_ids": [act.id for act in org.activities],
        }
        for org in organizations
    ]


async def get_organizations_in_radius(
    db: AsyncSession, lat: float, lon: float, radius: float
):
    buildings_in_radius = await get_buildings_in_radius(db, lat, lon, radius)
    building_ids = [building.id for building in buildings_in_radius]

    if not building_ids:
        return []

    result = await db.execute(
        select(Organization)
        .where(Organization.building_id.in_(building_ids))
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
    )

    organizations = result.scalars().all()

    return [
        {
            "id": org.id,
            "name": org.name,
            "building_id": org.building_id,
            "phone_numbers": [pn.phone_number for pn in org.phone_numbers],
            "activity_ids": [act.id for act in org.activities],
        }
        for org in organizations
    ]


async def get_organization_by_id(db: AsyncSession, organization_id):
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
    )

    organization = result.scalars().first()

    return {
        "id": organization.id,
        "name": organization.name,
        "building_id": organization.building_id,
        "phone_numbers": [pn.phone_number for pn in organization.phone_numbers],
        "activity_ids": [act.id for act in organization.activities],
    }


async def get_organizations_by_name_activity(db: AsyncSession, activity_name: str):
    root_activity = await db.execute(
        select(Activity)
        .where(Activity.name.ilike(f"%{activity_name}%"))
        .where(Activity.parent_id.is_(None))
    )
    root_activity = root_activity.scalars().first()

    if not root_activity:
        return []

    all_activities = await db.execute(
        select(Activity).where(
            or_(
                Activity.id == root_activity.id,
                Activity.parent_id == root_activity.id,
            )
        )
    )
    activity_ids = [activity.id for activity in all_activities.scalars().all()]

    result = await db.execute(
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(activity_ids))
        .options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
        )
        .distinct()
    )

    organizations = result.scalars().all()

    return [
        {
            "id": org.id,
            "name": org.name,
            "building_id": org.building_id,
            "phone_numbers": [pn.phone_number for pn in org.phone_numbers],
            "activity_ids": [act.id for act in org.activities],
        }
        for org in organizations
    ]
