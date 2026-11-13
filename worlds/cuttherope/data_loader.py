from typing import Any, Dict, Set, List

import orjson
import pkgutil

regions_json_data : Dict[str, Any] = orjson.loads(pkgutil.get_data(__name__, "levels.json").decode("utf-8-sig"))

def get_all_locations() -> Dict[str, int]:
    locations : Dict[str, int] = {}
    for level_name, level_data in regions_json_data.items():
        # First get base ID for the level, which is in form BB_LL_0_0
        # B = Original Box Number, L = Original Level Number
        level_base_id: int = int(level_name.split('-')[0]) * 10000 + int(level_name.split('-')[1]) * 100

        # Goal location
        locations[f"{level_name} - Complete Level"] = level_base_id

        # Starsanity count locations
        for i in range(1, 4):
            star_name = f"{level_name} - {i} Star"
            if i > 1:
                star_name += "s"
            locations[star_name] = level_base_id + 1_0 + i

        # Individual starsanity locations
        i = 0
        for star in level_data["starsanity"]:
            locations[f"{level_name} - {star}"] = level_base_id + 2_0 + i
            i += 1

    return locations

all_location_groups : Dict[str, Set[str]] = {}
all_locations: Dict[str, int | None] = get_all_locations()