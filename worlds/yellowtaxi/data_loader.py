from typing import Any, Dict, Set, List

from . import locations

import orjson
import pkgutil

# Load regions from JSON
def load_json_data(data_name: str) -> Dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "json/" + data_name).decode("utf-8-sig"))

regions_json_data : Dict[str, Any] = (load_json_data("LXX.special.json") |
                                      load_json_data("L00.hub.json") |
                                      load_json_data("L03.morioshome.json") |
                                      load_json_data("L01.bombeach.json") |
                                      load_json_data("L04.arcadepanik.json") |
                                      load_json_data("L02.pizzatime.json") |
                                      load_json_data("L05.toslaoffices.json") |
                                      load_json_data("L06.gymgears.json") |
                                      load_json_data("L07.fecalmatters.json") |
                                      load_json_data("L08.flushedaway.json") |
                                      load_json_data("L09.maurizioscity.json") |
                                      load_json_data("L16.rocket.json") |
                                      load_json_data("L17.babysteps.json") |
                                      load_json_data("L18.gettinggud.json") |
                                      load_json_data("L19.protricks.json")
                                      )

# Load static locations list
def get_all_locations(json_data: Dict[str, Any]) -> Dict[str, int | None]:
    # Get all location ids from JSON
    game_locations: Dict[str, int | None] = {}
    location_keys : List[str] = [
        "gears",
        "bunnies",
        "safes",
        "chests",
        "coinbags",
        "coins",
        "checkpoints",
        "cheeses",
        # Hats are handled specially
    ]
    for reg_name in json_data.keys():
        reg = json_data[reg_name]
        reg_locations : Dict[str, int | None] = {}
        for key in location_keys:
            if key in reg.keys():
                reg_locations |= reg[key]

        if "hats" in reg.keys():
            reg_locations |= locations.get_hat_locations(None, reg["sublevel"], reg["hats"])

        reg_locations |= locations.get_special_locations(None, reg_name)
        game_locations.update(reg_locations)
        for location in reg_locations:
            if reg["sublevel"] in all_location_groups:
                all_location_groups[reg["sublevel"]].add(location)
            else:
                all_location_groups[reg["sublevel"]] = {location}


    return game_locations

all_location_groups : Dict[str, Set[str]] = {}
all_locations: Dict[str, int | None] = get_all_locations(regions_json_data)