from __future__ import annotations

from math import floor
from typing import Dict, List, TYPE_CHECKING, Union

from BaseClasses import Location, Region, LocationProgressType

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
    coins : List[tuple[Region, Dict[str, int | None]]] = []
    use_simple_coinsanity = (hasattr(world.multiworld, "generation_is_fake") or
                             ((world.multiworld.players == 1 or
                               world.settings.multiworld_coinsanity_percentage_non_filler_cap >= 100) and
                              world.options.coinsanity_percent >= 100))
    for region in world.get_regions():
        if region.name == "Menu":
            continue
        reg = regions_json_data[region.name]
        level : str = reg["level"]

        if world.options.exclude_goal_portal_checks and level in world.goal_levels:
            continue

        locations : Dict[str, int | None] = {}
        if world.options.time_trial_gears or not level.endswith("!"): # Time Trial Levels all end with "!"
            locations = reg["gears"]
            world.num_gears += len(locations)
        if world.options.bunnysanity:
            locations = locations | reg["bunnies"]
            world.num_bunnies += len(reg["bunnies"])
        elif "Mosk's Rocket" in world.included_levels: # Non-bunnysanity still needs to track bunnies if rocket is in
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
            if use_simple_coinsanity:
                locations = locations | reg["coins"]
            else:
                for coin, coin_id in reg["coins"].items():
                    coins += [(region, {coin: coin_id})]
        if world.options.hatsanity != 0:
            locations = locations | get_hat_locations(world, reg["sublevel"], reg["hats"])

        if world.options.cheesesanity:
            locations = locations | reg["cheeses"]

        locations = locations | get_special_locations(world, region.name)
        region.add_locations(locations)

    # Set random coins as checks, based on coinsanity % setting
    if world.options.coinsanity and len(coins) > 0:
        selected_coin_count : int = len(coins)
        if world.options.coinsanity_percent < 100:
            selected_coin_count = floor((len(coins) * world.options.coinsanity_percent) / 100)
        max_nonfiller_coin_count : int = len(coins)
        if world.multiworld.players > 1:
            max_nonfiller_coin_count = floor((len(coins) *
                                              world.settings.multiworld_coinsanity_percentage_non_filler_cap) / 100)
        world.random.shuffle(coins)
        for i in range(0, selected_coin_count):
            coin_data = coins[i]
            # coin_data[0] is region, coin_data[1] is actual coin
            coin_data[0].add_locations(coin_data[1])
            if i > max_nonfiller_coin_count:
                # Exclude coins past the threshold
                loc : Location = world.get_location(list(coin_data[1].keys())[0])
                loc.progress_type = LocationProgressType.EXCLUDED

    if world.options.hatsanity == 0:
        world.get_region("Granny's Island Hat World").add_event(
            "Event: Granny's Island Hat World - Purchase Morio Hat", "Morio Hat",
            location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
        )

    if world.early_rat and not world.options.shuffle_rat:
        world.get_region("Granny's Island - Main Area").add_event(
            "Event: Granny's Island - Talk to Michele Near Beach", "Michele",
            location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
        )

    if world.options.goal == 0:
        world.get_region("Bombeach - Starting Area").add_event(
            "Event: Defeat Bomboss", "Victory",
            location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem
        )

def get_hat_locations(world: Union[YellowTaxiWorld | None], subarea_name: str, hat_dict: dict[str, int]) -> Dict[str, int | None]:
    # No hats, return early
    if len(hat_dict) == 0:
        return {}

    locations : dict[str, int | None] = {}

    if world is None or world.options.hatsanity == world.options.hatsanity.option_hatsanity:
        for (hat, hat_id) in hat_dict.items():
            # "No Hat" is not a hatsanity check
            if hat == "No Hat":
                continue
            # Add hat to the "included hats" list for item generation
            if world is not None:
                world.included_hats.add(hat)
            # Hats purchasable in multiple locations (Handled in special locations)
            if hat == "Propeller Cap" or hat == "Top Hat":
                continue

            true_id = (hat_id % 1_00_00000) + 99_00_00000
            locations[f"Purchase {hat}"] = true_id

    if world is None or world.options.hatsanity == world.options.hatsanity.option_shopsanity:
        for (hat, hat_id) in hat_dict.items():
            # Add hat to the "included hats" list for item generation, count hat-based locations
            if world is not None:
                if hat != "No Hat":
                    world.included_hats.add(hat)
                world.hat_location_count += 1

            locations[f"{subarea_name} - Purchase {hat}"] = hat_id

    return locations

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
            #if world is None or (world.options.shuffle_doggo and world.early_doggo):
            #    locations["Granny's Island - Talk to Doggo"] = 10_10007
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
                if world is not None:
                    world.num_bunnies += 1
        case "Morio's Lab - Inside Morio's Room":
            if world is None or world.options.locked_morios_lab:
                locations = {
                    "Morio's Lab - Talk to Morio in Morio's Room": 10_00000,
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
                    "Morio's Lab - Reach True Demo Wall": 10_00011,
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
            if world is None or (world.options.fecal_matters_unlock_condition ==
                                 world.options.fecal_matters_unlock_condition.option_shuffle_doggo):
                locations = {
                    "Morio's Lab - Talk to Doggo": 10_00007
                }
            elif (world.options.fecal_matters_unlock_condition ==
                  world.options.fecal_matters_unlock_condition.option_vanilla): # Doggo item still logically needed
                region = world.get_region(region_name)
                region.add_event(f"Event: Morio's Lab - Talk to Doggo", f"Doggo",
                                 location_type=YellowTaxiLocation, item_type=items.YellowTaxiItem)
        case "Morio's Lab - Fifth Floor Morio's Mind Area":
            # Backflip tutorial gets moved earlier
            if world is not None and world.options.shuffle_flip_o_will and world.early_backflip:
                locations = {
                    "Morio's Lab - PICI Backflip Tutorial": 8_00004,
                }
        case "Morio's Lab - Dream Machine":
            if world is None or (world.options.shuffle_morios_password and world.early_morios_password):
                locations = {
                    "Morio's Lab - Talk to Morio in Dream Machine": 11_00012
                }
        case "Morio's Lab - Final Floor":
            if world is None or (world.options.shuffle_flip_o_will and not world.early_backflip):
                locations = {
                    "Morio's Lab - PICI Backflip Tutorial": 8_00004,
                }
        case "Morio's Wardrobe":
            if world is None or world.options.locked_morios_wardrobe:
                locations = {
                    "Morio's Wardrobe - Talk to Mori-O-Tron": 11_00000,
                }
        case "Morio's Island - Starting Area":
            if world is None or world.options.shuffle_flip_o_will:
                locations = {
                    "Morio's Island - Talk to Morio": 3_08_00001,
                }
        case "Crash Again - End":
            if world is None or (world.options.shuffle_orange_switch and world.early_orange_switch):
                locations = {
                    "Crash Again - Talk to Ocra Taxi Goes Smooch": 11_00010
                }
        case "Bombeach - Starting Area":
            if world is None or (world.options.shuffle_gela_toni and not world.early_gela_toni):
                locations = {
                    "Bombeach - Save Gela-Toni - Defeat Bomboss": 1_11_00001
                }
            elif world is not None and not world.options.shuffle_gela_toni: # Gela-Toni item still logically needed
                region = world.get_region(region_name)
                region.add_event(f"Event: Bombeach - Save Gela-Toni - Defeat Bomboss", f"Gela-Toni",
                                 location_type=YellowTaxiLocation,
                                 item_type=items.YellowTaxiItem)
        case "Gym Gears - Starting Area":
            if world is None or (world.options.gym_gears_unlock_condition ==
                                 world.options.gym_gears_unlock_condition.option_shuffle_gym_membership):
                locations = {
                    "Gym Gears - Purchase Membership From Ultra Chad": 6_10_00006,
                }
        case "Arcade Panik - Starting Area":
            if world is None or (world.options.shuffle_psycho_taxi and not world.early_psycho_taxi):
                locations = {
                    "Arcade Panik - Psycho Taxi Cartridge": 4_20_99999,
                }
        case "Baby Steps! - Pillar":
            if world is None or world.options.locked_time_trials:
                locations = {
                    "Baby Steps! - Complete Time Trial": 17_00_00000,
                }
        case "Getting Gud! - High Ground":
            if world is None or world.options.locked_time_trials:
                locations = {
                    "Getting Gud! - Complete Time Trial": 18_00_00000,
                }
        case "Pro Tricks! - Final Section":
            if world is None or world.options.locked_time_trials:
                locations = {
                    "Pro Tricks! - Complete Time Trial": 19_00_00000,
                }
        case "Flushed Away - Starting Area":
            if (world is None or
                    world.options.flushed_away_unlock_condition ==
                    world.options.flushed_away_unlock_condition.option_shuffle_sewer_key):
                locations = {
                    "Flushed Away - Talk to Michele": 8_10_00008,
                }
        case "Any Hat World":
            if world is None or world.options.hatsanity == world.options.hatsanity.option_hatsanity:
                locations = {
                    "Purchase Top Hat": 99_07_00002,
                }
                if world is not None:
                    world.included_hats.add("Top Hat")
        case "Propeller Cap Access":
            if world is None or world.options.hatsanity == world.options.hatsanity.option_hatsanity:
                locations = {
                    "Purchase Propeller Cap": 99_07_00001,
                }
                if world is not None:
                    world.included_hats.add("Propeller Cap")

    return locations