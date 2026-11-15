import logging
from collections.abc import Mapping
from typing import Any, List, Dict, Optional

from BaseClasses import MultiWorld, Region, Location
from Options import Option, OptionError
from Utils import messagebox
from rule_builder.rules import Rule, True_, Has
from worlds.AutoWorld import World
from . import data_loader, items, web_world
from . import options as cut_the_rope_options
from .rules import RuleFactory
from ..LauncherComponents import components, Component, Type


class CutTheRopeLocation(Location):
    game = "Cut the Rope"

class CutTheRopeWorld(World):
    """
    A mysterious package has arrived, and the little monster inside has only one request… CANDY!
    Use your mouse to cut the ropes and release delicious bundles of candy into Om Nom's mouth.
    """
    game = "Cut the Rope"
    web = web_world.CutTheRopeWebWorld()

    options_dataclass = cut_the_rope_options.CutTheRopeOptions
    options: cut_the_rope_options.CutTheRopeOptions

    location_name_to_id = data_loader.all_locations
    item_name_to_id = items.ITEM_NAME_TO_ID

    # Universal Tracker stuff
    glitches_item_name = "Additional Expert Logic Level"
    ut_can_gen_without_yaml = True
    #found_entrances_datastorage_key: list[str] = ["Slot:{player}:PortalSave"]

    # Shamelessly taken from Tunic's implementation
    def attempt_launch_ut(*args: str) -> None:
        try:
            from worlds.tracker import launch_client

            launch_client(*args)
        except ImportError as e:
            logging.getLogger(__name__).error(e)
            messagebox(
                "Cannot Load UT",
                "There was an error loading Universal Tracker. Please ensure it is installed and up to date.",
            )

    components.append(
        Component(
            "Universal Tracker for Cut the Rope",
            func=attempt_launch_ut,
            game_name="Cut the Rope",
            component_type=Type.HIDDEN,
            supports_uri=True,
        )
    )

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    origin_region_name = "Menu"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.level_order : List[str] = []
        # Track which puzzle elements are required by the included levels. Only make items that are needed
        self.has_bubble : bool = False
        self.has_autograb : bool = False
        self.has_air_cushion : bool = False
        self.has_slider : bool = False
        self.has_electric_gates : bool = False
        self.has_hat : bool = False
        self.has_bouncer : bool = False
        self.has_wheel : bool = False
        self.has_gravity_button : bool = False
        self.has_blade : bool = False
        self.has_bee : bool = False
        self.has_record : bool = False
        # Spikes appear in enough levels to make this worth always adding when the option is enabled
        # This changes whether it's considered progression or useful
        self.spikes_progression : bool = False
        # Same with spiders
        self.spider_removal_progression : bool = False
        # Same with timed stars kinda
        # TODO: Make list of levels containing timed stars, if none are present don't make the item at all
        self.timed_star_progression : bool = False
        self.starting_box : int = 1

        self.using_ut : bool = False
        # UT only
        if getattr(self.multiworld, "generation_is_fake", False):
            self.using_ut = True

    def generate_early(self) -> None:
        # UT YAML-less
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            major_version : int = 0
            minor_version : int = 0
            build_version : int = 0
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_data.items():
                if key == "level_order":
                    for level in value:
                        for levelName, levelId in data_loader.level_ids.items():
                            if level == levelId:
                                self.level_order += [levelName]
                                break
                    continue

                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
                elif key == "major_version":
                    major_version = value
                elif key == "minor_version":
                    minor_version = value
                elif key == "build_version":
                    build_version = value
                elif key == "starting_box":
                    self.starting_box = value

            if major_version != self.world_version.major or minor_version != self.world_version.minor:
                message : str = ("APWorld version (v" +
                                 f"{self.world_version.major}.{self.world_version.minor}.{self.world_version.build}" +
                                 ") is not the same version used at generation (v" +
                                 f"{major_version}.{minor_version}.{build_version})!")
                try:
                    from worlds.tracker import TrackerException
                except:
                    raise OptionError(message)
                raise TrackerException(message=message)
        # UT doesn't need to choose a starting box
        elif not self.using_ut and self.options.random_starting_box:
            if self.options.box_locking_mode == self.options.box_locking_mode.option_box_items_with_skips:
                # Every world has a starting sphere with skips enabled
                self.starting_box = self.random.choice(range(1, self.options.goal_box - 1))
            elif self.options.box_locking_mode == self.options.box_locking_mode.option_box_items:
                # Only certain boxes allow immediately accessible locations, dependent on starsanity settings
                allowed_boxes : List[int] = [1, 5, 6, 8, 10]
                if self.options.starsanity_mode == self.options.starsanity_mode.option_individual:
                    # Individual starsanity boxes have some more options, albeit most of these will be quite restrictive
                    allowed_boxes += [4, 9, 11]
                self.starting_box = self.random.choice([i for i in allowed_boxes if i < self.options.goal_box])

        # Cap the number of stars to goal at 75 x number of non-goal boxes
        # This guarantees enough stars can be placed prior to the goal
        # Might still need to tweak this honestly, but it's probably fine for now
        goal_star_threshold = (self.options.goal_box - 1) * 75
        if self.options.goal_box_star_requirement.value > goal_star_threshold:
            self.options.goal_box_star_requirement.value = goal_star_threshold
            logging.warning(
                f"{self.player_name}: Your options have been modified.\n"
                f"Goal Box Star Requirement has been capped to {goal_star_threshold}.")
        self.level_order = list(data_loader.regions_json_data.keys())
        # TODO: Level shuffle
        # Get only the levels needed for the box count. 25 per box
        self.level_order = self.level_order[:(self.options.goal_box * 25)]

    def create_regions(self) -> None:
        # TODO: Create regions and locations at same time, no need to overcomplicate
        # World docs says setting rules can be done here too so probably will
        # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#create_regions
        # Also, create_regions is called *before* create_items, so can determine what items are needed programmatically
        #regions.create_and_connect_regions(self)
        #locations.create_all_locations(self)

        # Rules
        rule_factory = RuleFactory(self)

        regions : List[Region] = []

        menu : Region = Region("Menu", self.player, self.multiworld)
        regions += [menu]

        level_index : int = 0
        previous_region : Region = menu

        for box_num in range(0, self.options.goal_box):
            previous_region = menu
            for level_num in range(0, 25):
                # Each level is made up of two regions. "Level" and "Goal"
                # "Goal" is inherently needed for non-individual starsanity, and is also how the levels connect
                level_name = self.level_order[level_index]
                level_json = data_loader.regions_json_data[level_name]
                current_level : Region = Region(level_name, self.player, self.multiworld)
                level_access_rule : Rule = True_()
                # First level in each world may need additional rules
                if level_num == 0:
                    if box_num == self.options.goal_box - 1:
                        # Goal level has a star requirement
                        level_access_rule = Has("Star", self.options.goal_box_star_requirement.value)
                    elif box_num != self.starting_box - 1:
                        # Boxes have an item requirement on non-open world mode
                        if self.options.box_locking_mode != self.options.box_locking_mode.option_open_world:
                            level_access_rule = Has(items.BOX_ITEMS[box_num])
                # Connect the level to previous area
                previous_region.connect(current_level, rule=level_access_rule)
                # Get goal rule from json
                goal_rule : Rule = rule_factory.build_rule(level_json["goal"])
                # Create and connect goal region
                current_goal : Region = Region(f"{level_name} (Level Complete)", self.player, self.multiworld)
                current_level.connect(current_goal, rule=goal_rule)

                # Create locations and location rules
                goal_area_locations : Dict[str, int | None] = {}
                location_rules : Dict[str, str] = {}
                # First get base ID for the level, which is in form BB_LL_0_0
                # B = Original Box Number, L = Original Level Number
                level_base_id : int = int(level_name.split('-')[0]) * 10000 + int(level_name.split('-')[1]) * 100

                # Goal location. No rule since it is in the level complete region. Uses just the base ID for the level
                goal_area_locations[f"{level_name} - Complete Level"] = level_base_id

                # Starsanity count locations
                if self.options.starsanity_mode == self.options.starsanity_mode.option_per_level_count:
                    for i in range(1, 4):
                        star_name = f"{level_name} - {i} Star"
                        if i > 1:
                            star_name += "s"
                        goal_area_locations[star_name] = level_base_id + 1_0 + i
                        location_rules[star_name] = level_json["starcounts"][i - 1]

                # Add all goal region locations
                current_goal.add_locations(goal_area_locations, CutTheRopeLocation)

                # Add individual starsanity locations
                if self.options.starsanity_mode == self.options.starsanity_mode.option_individual:
                    level_locations : Dict[str, int | None] = {}
                    star_num = 0
                    for star, rule_str in level_json["starsanity"].items():
                        star_name = f"{level_name} - {star}"
                        level_locations[star_name] = level_base_id + 2_0 + star_num
                        star_num += 1
                        location_rules[star_name] = rule_str
                    current_level.add_locations(level_locations, CutTheRopeLocation)


                # Set rules
                for location_str, rule_str in location_rules.items():
                    loc : Location = self.get_location(location_str)
                    rule : Rule = rule_factory.build_rule(rule_str)
                    self.set_rule(loc, rule)

                regions += [current_level, current_goal]

                if self.options.box_locking_mode == self.options.box_locking_mode.option_box_items_with_skips:
                    previous_region = current_level
                else:
                    previous_region = current_goal
                level_index += 1

        previous_region.add_event("Complete Goal Box", "Victory")
        self.multiworld.regions += regions

    def create_items(self) -> None:
        items.create_all_items(self)

    def set_rules(self) -> None:
        # Most rules are set in create regions, but set the completion rule here
        self.set_completion_rule(Has("Victory"))

    def create_item(self, name: str) -> items.CutTheRopeItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data : dict[str, Any] = self.options.as_dict(
            "goal_box",
            "goal_box_star_requirement",
            "box_locking_mode",
            "starsanity_mode",
            "death_link",
            "death_link_amnesty",

            # Needed to make sure tutorials display by default when off
            "tutorials_item",

            # Needed for Universal Tracker
            "expert_level",
            # *Technically* I don't need these for UT but allows for simplified rules that closer match the seed
            "disable_spikes_item",
            "progressive_electric_sparks",
            "progressive_blades",
            "star_timer_disable_item",
            toggles_as_bools=True
        )

        slot_data["major_version"] = self.world_version.major
        slot_data["minor_version"] = self.world_version.minor
        slot_data["build_version"] = self.world_version.build
        slot_data["starting_box"] = self.starting_box

        return slot_data
