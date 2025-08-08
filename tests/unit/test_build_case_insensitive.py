from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from squid.db.builds import Build
from squid.db.schema import BuildCategory, Restriction, Type


@pytest.mark.asyncio
async def test_get_restrictions_case_insensitive():
    build = Build(category=BuildCategory.DOOR)
    build.wiring_placement_restrictions = ["  flush "]
    build.component_restrictions = ["NO PISTONS"]
    build.miscellaneous_restrictions = [" unknown "]

    session = AsyncMock(spec=AsyncSession)
    flush = Restriction(name="Flush", type="wiring-placement", build_category="Door")
    pistons = Restriction(name="No pistons", type="component", build_category="Door")
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_scalars.all.return_value = [flush, pistons]

    restrictions_input = (
        build.wiring_placement_restrictions + build.component_restrictions + build.miscellaneous_restrictions
    )

    found, unknown = await build._get_restrictions(session, restrictions_input)

    assert flush in found and pistons in found
    assert unknown == {"miscellaneous_restrictions": ["unknown"]}


@pytest.mark.asyncio
async def test_get_types_case_insensitive():
    build = Build(category=BuildCategory.DOOR)
    session = AsyncMock(spec=AsyncSession)
    regular = Type(name="Regular", build_category="Door")
    full_tnt = Type(name="Full TNT", build_category="Door")
    mock_result = MagicMock()
    session.execute.return_value = mock_result
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_scalars.all.return_value = [regular, full_tnt]

    types, unknown = await build._get_types(
        session,
        [" regular ", "FULL tNt", "Odd"],
    )

    assert regular in types and full_tnt in types
    assert unknown == ["Odd"]
