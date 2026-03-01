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
    from .data_loader import regions_json_data

    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    world.num_gears = 0
    world.num_bunnies = 0
    for region in world.get_regions():
        if region.name == "Menu":
            continue
        reg = regions_json_data[region.name]
        level : str = reg["level"]

        if world.options.exclude_goal_portal_checks and level in world.goal_levels:
            continue

        locations : Dict[str, int | None] = reg["gears"]
        world.num_gears += len(locations)
        if world.options.bunnysanity:
            locations = locations | reg["bunnies"]
            world.num_bunnies += len(reg["bunnies"])
        else: # Non-bunnysanity still needs to track bunnies
            for bunny in reg["bunnies"]:
                bunny_level : str = level
                if level == "Hub":
                    bunny_level = "Morio's Lab"
                region.add_event(f"Event: {bunny}", f"Bunny ({bunny_level})",
                                 location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem)
                world.num_bunnies += 1

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

        locations = locations | get_special_locations(world, region.name)
        region.add_locations(locations)

    world.get_region("Granny's Island - Hat World").add_event(
        "Event: Granny's Island Hat World - Purchase Morio Hat", "Morio Hat",
        location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
    )
    if world.early_rat and not world.options.shuffle_rat:
        world.get_region("Granny's Island - Main Area").add_event(
            "Event: Granny's Island - Talk to Michele Near Beach", "Michele",
            location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
        )


def get_special_locations(world: Union[YellowTaxiWorld | None], region_name: str) -> Dict[str, int | None]:
    # Get locations that are not in the json due to not fitting the main categories/being settings exclusive.
    # If world is None, indicates all possible locations should be returned (for full location list purposes)
    locations : Dict[str, int | None] = {}
    match region_name:
        case "Granny's Island - Main Area":
            if world is None or (world.options.shuffle_gela_toni and world.early_gela_toni):
                locations["Granny's Island - Talk to Gela-Toni"] = 11_00001
            if world is None or (world.options.shuffle_pizza_king and world.early_pizza_king):
                locations["Granny's Island - Talk to Pizza King"] = 11_00002
            if world is None or (world.options.shuffle_doggo and world.early_doggo):
                locations["Granny's Island - Talk to Doggo"] = 10_10007
            if world is None or (world.options.shuffle_rat and world.early_rat):
                locations["Granny's Island - Talk to Michele Near Beach"] = 21_99999
            if world is None or (world.options.shuffle_rocket and world.early_rocket):
                locations["Granny's Island - Talk to Alien Mosk"] = 10_00016
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
            if world is None or world.options.shuffle_golden_propeller and world.early_golden_propeller:
                locations["Granny's Island - Talk to Nick-O-Will"] = 11_00013
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
                if world is None or world.options.bunnysanity:
                    locations["Morio's Lab - Bunny - Above Morio's Home Portal"] = 2_00003
                else:  # Non-bunnysanity still needs to track bunnies
                    region = world.get_region(region_name)
                    region.add_event(f"Event: Morio's Lab - Bunny - Above Morio's Home Portal", f"Bunny (Morio's Lab)",
                                         location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem)
                if not world is None:
                    world.num_bunnies += 1
        case "Morio's Lab - Second Floor":
            # Matches existing location, so don't add it to location cache twice
            if world is not None and world.options.shuffle_flip_o_will and world.early_backflip:
                locations = {
                    "Morio's Lab - PICI Backflip Tutorial": 8_00004,
                }
        case "Morio's Lab - Psycho Taxi Arcade Machine":
            if world is None or (world.options.shuffle_psycho_taxi and world.early_psycho_taxi):
                locations = {
                    "Morio's Lab - Interact with Psycho Taxi Arcade Machine": 20_99999,
                }
        case "Morio's Lab - Second Floor Above Demo Wall":
            if world is None or world.options.extra_demo_collectables:
                if world is None or world.options.bunnysanity:
                    locations = {
                        "Morio's Lab - Bunny - Above Pizza Time Portal": 2_00004,
                    }
                else:  # Non-bunnysanity still needs to track bunnies
                    region = world.get_region(region_name)
                    region.add_event(f"Event: Morio's Lab - Bunny - Above Pizza Time Portal", f"Bunny (Morio's Lab)",
                                         location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem)
                if not world is None:
                    world.num_bunnies += 1
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
            if world is None or world.options.shuffle_golden_spring and world.early_golden_spring:
                locations["Morio's Lab - Talk to Morio Near Tosla Offices Portal"] = 11_00005
        case "Morio's Lab - Fourth Floor":
            if world is None or (world.options.shuffle_doggo and not world.early_doggo):
                locations = {
                    "Morio's Lab - Talk to Doggo": 10_00007
                }
        case "Morio's Lab - Fifth Floor Morio's Mind Area":
            if world is None or (world.options.shuffle_morios_password and world.early_morios_password):
                locations = {
                    "Morio's Lab - Talk to Morio in Dream Machine": 11_00012
                }
        case "Morio's Lab - Final Floor":
            if world is None or (world.options.shuffle_flip_o_will and not world.early_backflip):
                locations = {
                    "Morio's Lab - PICI Backflip Tutorial": 8_00004,
                }
        case "Morio's Island - Starting Area":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Island - Talk to Morio": 8_00001,
                }
        case "Crash Again - End":
            if world is None or (world.options.shuffle_orange_switch and world.early_orange_switch):
                locations = {
                    "Crash Again - Talk to Ocra Taxi Goes Smooch": 11_00010
                }
        case "Arcade Panik - Starting Area":
            if world is None or (world.options.shuffle_psycho_taxi and not world.early_psycho_taxi):
                locations = {
                    "Arcade Panik - Psycho Taxi Cartridge": 4_20_99999,
                }

    return locations