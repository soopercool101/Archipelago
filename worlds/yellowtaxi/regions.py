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
    if world.using_ut:
        ut_sorted_sublevels: dict[str, int] = {}
        ut_sort_region_counters: dict[str, int] = {}
        ut_sorted_levels: dict[str, int] = {}
        ut_sorted_level_counter: int = 0
        include_oob_areas: bool = (
                    world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_full)
    else:
        include_oob_areas: bool = (
                    world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_full
                    and world.options.expert_level >= 1)
    for reg_name in regions_json_data.keys():
        if reg_name in world.excluded_regions:
            continue
        if world.options.expert_level < 1 and "(EXPERTS ONLY)" in reg_name:
            continue
        if not include_oob_areas and "out-of-bounds" in reg_name.lower():
            continue
        if (world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_none and
                "hidden coins" in reg_name.lower()):
            continue
        reg = regions_json_data[reg_name]
        if reg["level"] not in world.included_levels and reg["level"] not in world.special_levels and reg["level"] not in world.goal_levels:
            continue
        if reg["level"] == "Mosk's Rocket" and reg["kaizolevel"] not in world.included_levels:
            continue
        regions += [Region(reg_name, world.player, world.multiworld)]
        # UT sorting. Basically it adds level # * 100 and sublevel # based on order defined in the json
        # TODO: Make this more accurate based on level order, especially when level rando is in
        # May need to move this elsewhere if doing so, since level order may not yet be able to be inferred
        # Also this could probably be simplified significantly but it works for the time being
        if world.using_ut:
            if reg["level"] not in ut_sorted_levels.keys():
                ut_sorted_levels[reg["level"]] = ut_sorted_level_counter
                ut_sorted_level_counter += 1
            if reg["sublevel"] not in ut_sorted_sublevels:
                if reg["level"] in ut_sort_region_counters.keys():
                    ut_sort_region_counters[reg["level"]] += 1
                else:
                    ut_sort_region_counters[reg["level"]] = 1
                ut_sorted_sublevels[reg["sublevel"]] = ((ut_sorted_levels[reg["level"]] * 100) +
                                                        ut_sort_region_counters[reg["level"]])
            world.ut_sort_region_dict[reg_name] = ut_sorted_sublevels[reg["sublevel"]]

    world.multiworld.regions += regions


def connect_regions(world: YellowTaxiWorld) -> None:
    for region in world.get_regions():
        if region.name == "Menu":
            # Connect starting area
            if world.lab_start:
                region.connect(world.get_region("Morio's Lab - Ground Floor"))
            else:
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

