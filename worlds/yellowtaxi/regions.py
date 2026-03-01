from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from BaseClasses import Entrance, Region


if TYPE_CHECKING:
    from .world import YellowTaxiWorld

def create_and_connect_regions(world: YellowTaxiWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: YellowTaxiWorld) -> None:
    regions = [Region("Menu", world.player, world.multiworld)]
    # TODO: Don't include postgame regions based on goal
    for reg in world.regions_json.values():
        reg_name = reg["name"]
        if reg_name in world.excluded_regions:
            continue
        if reg["level"] not in world.included_levels and reg["level"] not in world.goal_levels:
            continue
        regions += [Region(reg["name"], world.player, world.multiworld)]

    world.multiworld.regions += regions


def connect_regions(world: YellowTaxiWorld) -> None:
    # Connect starting area. TODO: Change if ever adding random starting area
    world.get_region("Menu").connect(world.get_region("Granny's Island - Starting Area"))
    for reg in world.regions_json.values():
        try:
            region = world.get_region(reg["name"])
        except KeyError:
            continue

        # Connect basic connections
        for connect in reg["connections"].items():
            try:
                connecting_region = world.get_region(connect[0])
            except KeyError:
                continue
            region.connect(connecting_region, f"{region.name} -> {connecting_region.name}")

        # Connect subwarps
        # TODO: Entrance Rando
        for subwarp in reg["subwarps"].items():
            try:
                connecting_region = world.get_region(subwarp[1][0])
            except KeyError:
                continue
            region.connect(connecting_region, subwarp[0])

        # Connect full warps
        # TODO: Entrance Rando
        for warp in reg["warps"].items():
            try:
                connecting_region = world.get_region(warp[1][0])
            except KeyError:
                continue
            region.connect(connecting_region, warp[0])

