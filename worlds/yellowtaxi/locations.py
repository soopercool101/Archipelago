from __future__ import annotations

from typing import Dict, TYPE_CHECKING, Union

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import YellowTaxiWorld

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class YellowTaxiLocation(Location):
    game = "Yellow Taxi Goes Vroom"

def create_locations(world: YellowTaxiWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    world.num_gears = 0
    for reg in world.regions_json.values():
        region_name = reg["name"]
        # if a region doesn't exist, don't make items for it
        try:
            region = world.get_region(region_name)
        except KeyError:
            continue
        locations : Dict[str, int | None] = reg["gears"]
        world.num_gears += len(locations)
        if world.options.bunnysanity:
            locations = locations | reg["bunnies"]
        else: # Non-bunnysanity still needs to track bunnies
            for bunny in reg["bunnies"]:
                region.add_event(bunny, f"Bunny - {reg["level"]}",
                                 location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem)
        if world.options.checkpointsanity:
            locations = locations | reg["checkpoints"]
        if world.options.safesanity:
            locations = locations | reg["safes"]
        if world.options.chestsanity:
            locations = locations | reg["chests"]
        if world.options.coinbagsanity:
            locations = locations | reg["coinbags"]
        if world.options.coinsanity:
            locations = locations | reg["coins"]
        if world.options.cheesesanity:
            locations = locations | reg["cheeses"]

        locations = locations | get_special_locations(world, region_name)
        region.add_locations(locations)

    world.get_region("Granny's Island - Hat World").add_event(
        "Granny's Island Hat World - Purchase Morio Hat", "Morio Hat",
        location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
    )


def get_special_locations(world: Union[YellowTaxiWorld | None], region_name: str) -> Dict[str, int | None]:
    # Get locations that are not in the json due to not fitting the main categories/being settings exclusive.
    # If world is None, indicates all possible locations should be returned (for full location list purposes)
    locations : Dict[str, int | None] = {}
    match region_name:
        case "Granny's Island - Main Area":
            if world is None or (world.options.shuffle_pizza_king and world.options.goal < 1):
                locations["Granny's Island - Talk to Pizza King"] = 10_10002
            if world is None or (world.options.shuffle_doggo and world.options.goal < 2 and not world.options.shuffle_golden_spring):
                locations["Granny's Island - Talk to Doggo"] = 10_10007
            if world is None or (world.options.shuffle_rat and world.options.goal < 1):
                locations["Granny's Island - Talk to Michele Near Beach"] = 2_21_99999
        case "Granny's Island - Crash Again Roof":
            if world is None or world.options.extra_demo_collectables:
                locations = {
                    "Granny's Island - Gear - On Crash Again Roof": 1_10010,
                }
                if world is not None:
                    world.num_gears += 1
        case "Granny's Island - Sewer Island Upper":
            if world is None or world.options.extra_demo_collectables:
                locations["Granny's Island - Gear - Above Sewer"] = 1_10020
                if world is not None:
                    world.num_gears += 1
        case "Granny's Island - High Ground":
            if world is None or world.options.extra_demo_collectables:
                locations = {
                    "Granny's Island - Gear - On Pizza Oven": 1_10004
                }
                if world is not None:
                    world.num_gears += 1
        case "Morio's Lab - Ground Floor Orange Blocks":
            if world is None or world.options.extra_demo_collectables:
                locations = {
                    "Morio's Lab - Gear - On Orange Blocks": 1_10019,
                }
                if world is not None:
                    world.num_gears += 1
        case "Morio's Lab - Ground Floor Bolts":
            if world is None or world.options.shuffle_glide:
                locations = {
                    "Morio's Lab - PICI Glide Tutorial": 8_00006,
                }
            if world is None or world.options.extra_demo_collectables:
                locations["Morio's Lab - Gear - Under Nut Above Ground Floor"] = 1_10024
                if world is not None:
                    world.num_gears += 1
        case "Morio's Lab - Path to Morio's Room":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Lab - PICI Superboost Tutorial": 8_00002,
                }
            if world is None or world.options.extra_demo_collectables:
                locations["Morio's Lab - Bunny - Above Morio's Home Portal"] = 2_00003
        case "Morio's Lab - Second Floor Above Demo Wall":
            if world is None or world.options.extra_demo_collectables:
                locations = {
                    "Morio's Lab - Bunny - Above Pizza Time Portal": 2_00004,
                }
        case "Morio's Lab - Second Floor Inside True Demo Wall":
            if world is None or world.options.shuffle_full_game:
                locations = {
                    "Reach True Demo Wall": 10_00011,
                }
        case "Morio's Lab - Second Floor After True Demo Wall":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Lab - PICI Flip Tutorial": 8_00003,
                }
        case "Morio's Lab - Third Floor":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Lab - PICI Spin Attack Tutorial": 8_00005,
                }
        case "Morio's Lab - Fourth Floor":
            if world is None or (world.options.shuffle_doggo and world.options.goal > 1):
                locations = {
                    "Morio's Lab - Talk to Doggo": 10_00007
                }
        case "Morio's Lab - Final Floor":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Lab - PICI Backflip Tutorial": 8_00004,
                }
        case "Morio's Island - Starting Area":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Island - Talk to Morio": 8_00001,
                }
        #case "Arcade Panik - Starting Area":
        #    if world is None or world.options.shuffle_psycho_taxi:
        #        locations = {
        #            "Arcade Panik - Psycho Taxi Cartridge": 4_20_99999,
        #        }

    return locations