from __future__ import annotations

from .data_loader import regions_json_data
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
    for reg_name in regions_json_data.keys():
        if reg_name in world.excluded_regions:
            continue
        reg = regions_json_data[reg_name]
        if reg["level"] not in world.included_levels and reg["level"] not in world.goal_levels:
            continue
        regions += [Region(reg_name, world.player, world.multiworld)]

    world.multiworld.regions += regions


def connect_regions(world: YellowTaxiWorld) -> None:
    for region in world.get_regions():
        if region.name == "Menu":
            # Connect starting area. TODO: Change if ever adding random starting area
            region.connect(world.get_region("Granny's Island - Starting Area"))
            continue
        reg = regions_json_data[region.name]

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

