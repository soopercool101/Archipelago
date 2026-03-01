from typing import Any, Dict

from . import locations

import orjson
import pkgutil

# Load regions from JSON
def load_json_data(data_name: str) -> Dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "json/" + data_name).decode("utf-8-sig"))

regions_json_data : Dict[str, Any] = (load_json_data("hub.json") |
                                      load_json_data("morioshome.json") |
                                      load_json_data("bombeach.json") |
                                      # load_json_data("arcadepanik.json") |
                                      load_json_data("gymgears.json")
                                      )

# Load static locations list
def get_all_locations(json_data: Dict[str, Any]) -> Dict[str, int]:
    # Get all location ids from JSON
    game_locations: Dict[str, int] = {}
    for reg_name in json_data.keys():
        reg = json_data[reg_name]
        game_locations = (game_locations | reg["gears"] | reg["bunnies"] | reg["safes"] | reg["chests"] |
                          reg["coinbags"] | reg["coins"] | reg["checkpoints"] | reg["cheeses"])
        # Include non-JSON optional locations for the region
        game_locations.update(locations.get_special_locations(None, reg_name))

    return game_locations

all_locations: Dict[str, int] = get_all_locations(regions_json_data)