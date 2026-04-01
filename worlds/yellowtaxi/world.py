import logging
from collections.abc import Mapping
from typing import Any, ClassVar, Dict, List, Set

from BaseClasses import MultiWorld
from Utils import visualize_regions, Version
from worlds.AutoWorld import World

from . import data_loader, items, regions, locations, rules, web_world
from . import options as taxi_options
from . import settings as taxi_settings


class YellowTaxiWorld(World):
    #TODO: Better description
    """
    Yellow Taxi Goes Vroom is a trippy arcade platformer ready to take you on a crazy adventure!
    """
    game = "Yellow Taxi Goes Vroom"

    web = web_world.YellowTaxiWebWorld()

    options_dataclass = taxi_options.YellowTaxiOptions
    options: taxi_options.YellowTaxiOptions
    settings_key = "yellowtaxi_options"
    settings: ClassVar[taxi_settings.YellowTaxiSettings]

    location_name_to_id = data_loader.all_locations
    location_name_groups = data_loader.all_location_groups
    item_name_to_id = items.ITEM_NAME_TO_ID

    # Universal Tracker stuff
    glitches_item_name = "Glitched Logic"

    # Keeping default Menu region, actual starting location can vary so this is simpler
    origin_region_name = "Menu"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.num_gears : int = 0
        self.num_bunnies : int = 0
        self.included_hats: Set[str] = set()
        self.hat_location_count : int = 0
        self.excluded_regions : List[str] = []
        self.included_levels : List[str] = []
        self.special_levels : List[str] = []
        self.lab_start : bool = False
        self.early_gela_toni : bool = False
        self.early_pizza_king : bool = False
        self.early_rat : bool = False
        self.early_doggo : bool = False
        self.early_sewer_island : bool = False
        self.early_backflip : bool = False
        self.early_psycho_taxi : bool = False
        self.early_orange_switch : bool = False
        self.early_golden_spring : bool = False
        self.early_golden_propeller : bool = False
        self.early_morios_password : bool = False
        self.early_rocket : bool = False
        self.exclude_spike_bunny : bool = False
        self.exclude_top_bunny : bool = False
        self.final_portal_cost : int = 0
        self.goal_levels : List[str] = ["Bombeach"]

    def generate_early(self) -> None:
        # Determine which regions are not going to be included

        self.num_gears = 0
        self.num_bunnies = 0
        self.included_hats = set()
        self.hat_location_count = 0
        self.excluded_regions = []
        self.included_levels = []

        match self.options.goal:
            case 0:
                self.goal_levels = ["Bombeach"]
            case 1:
                self.goal_levels =  ["Tosla Offices"]
            case 2:
                self.goal_levels = ["Tosla HQ", "Moon"]

        # Include levels up to the goal
        # Always included levels
        self.included_levels = [
            "Hub",
            "Morio's Home",
            "Bombeach",
        ]

        self.special_levels = [
            ""  # "Empty" = appears in multiple levels
        ]

        if self.options.locked_time_trials or self.options.time_trial_gears:
            self.included_levels += [
                "Baby Steps!",
                "Getting Gud!",
                "Pro Tricks!",
            ]

        has_golden_spring = self.options.shuffle_golden_spring or ("Tosla Offices" in self.included_levels and
                                                                   "Tosla Offices" not in self.goal_levels)
        has_orange_switch = self.options.shuffle_orange_switch or "Crash Test Industries" in self.included_levels
        has_golden_propeller = self.options.shuffle_golden_propeller or "Ruined Observatory" in self.included_levels
        has_rocket = self.options.shuffle_rocket

        if self.options.hatsanity == 1: # Special "level" for shared hats
            self.special_levels += ["Hatsanity"]

        # Exclude unreachable hub areas
        if not has_rocket:
            if not (self.options.expert_level >= 3 and has_golden_propeller):
                self.excluded_regions += ["Granny's Island - Top of Rocket"]
        else:
            self.included_levels += ["Mosk's Rocket"]
        # Pizza King and Gela-Toni are post BomBoss goal
        if self.options.goal < 1:
            if not self.options.shuffle_gela_toni:
                self.excluded_regions += ["Ice Cream Truck - Lower Path", "Ice Cream Truck - Upper Path"]
            if not self.options.shuffle_pizza_king:
                self.excluded_regions += ["Pizza Oven - Entrance", "Pizza Oven - Pillar"]
        # Doggo, Golden Spring, Orange Switch, Morio's Password, and Golden Propeller are all post Tosla HQ goal
        if self.options.goal < 2:
            # Can't reach Crash Again or Flushed Away without Orange Switch or Golden Propeller in Expert 1 and above
            if (not self.options.shuffle_orange_switch and
                    (not self.options.expert_level >= 1 or not self.options.shuffle_golden_propeller)):
                self.excluded_regions += ["Granny's Island - Crash Again Island",
                                          "Granny's Island - Crash Again Roof",
                                          "Crash Again - Starting Area",
                                          "Crash Again - End",
                                          "Granny's Island - Sewer Island",
                                          "Granny's Island - Sewer Island Upper"]
            #else:
            #    self.included_levels += ["Flushed Away"]
            # Cannot reach these spiky areas without golden spring
            if not self.options.shuffle_golden_spring:
                self.excluded_regions += ["Morio's Lab - Fourth Floor Jump Spikes",
                                          "Lab Memories - First Step",
                                          "Lab Memories - High Ground"]
                if self.options.expert_level < 2:
                    self.excluded_regions += ["Morio's Lab - Fourth Floor Expert Jump Spikes"]
            # Final floor is hard locked behind Morio's Password
            if not self.options.shuffle_morios_password:
                self.excluded_regions += ["Morio's Lab - Fifth Floor Ruined Observatory Area",
                                          "Morio's Lab - Fifth Floor Golden Propeller",
                                          "Morio's Lab - Fifth Floor Golden Propeller (Password)",
                                          "Morio's Lab - Ledge Above Ruined Observatory Portal",
                                          "Morio's Lab - Ledge Below Tosla HQ Portal",
                                          "Morio's Lab - Fifth Floor Low Pillars",
                                          "Morio's Lab - Fifth Floor High Pillars",
                                          "Morio's Lab - Final Floor",
                                          "Morio's Lab - Final Floor Pipes",
                                          "Morio's Lab - Final Floor Catwalk"]
                if self.options.expert_level == 0:
                    # Assume that expert 0 will not be using the shortcut pipe
                    self.excluded_regions += [
                        "Morio's Lab - Second Floor Falling From Shortcut Pipe",
                        "Morio's Lab - Second Floor Access to Shortcut Pipe",
                        "Morio's Lab - Fifth Floor Inside Shortcut Pipe",
                    ]

        # Add Gym Gears if included via settings
        if self.options.gym_gears_unlock_condition != self.options.gym_gears_unlock_condition.option_exclude:
            self.included_levels += ["Gym Gears"]
        # Add Fecal Matters if included via settings
        if self.options.fecal_matters_unlock_condition != self.options.fecal_matters_unlock_condition.option_exclude:
            self.included_levels += ["Fecal Matters"]
        # Add Flushed Away if included via settings and logically accessible
        if self.options.flushed_away_unlock_condition != self.options.flushed_away_unlock_condition.option_exclude:
            if self.options.flushed_away_unlock_condition != self.options.flushed_away_unlock_condition.option_default or "Granny's Island - Sewer Island" not in self.excluded_regions:
                self.included_levels += ["Flushed Away"]
                if "Granny's Island - Sewer Island" in self.excluded_regions:
                    self.excluded_regions.remove("Granny's Island - Sewer Island")
                    self.excluded_regions.remove("Granny's Island - Sewer Island Upper")
                    self.early_sewer_island = True

        # Make sure early items are set as needed
        if self.options.shuffle_gela_toni and self.options.exclude_goal_portal_checks and self.options.goal < 1:
            self.early_gela_toni = True
        if not "Pizza Time" in self.included_levels:
            if self.options.shuffle_pizza_king:
                self.early_pizza_king = True
            self.early_rat = True
        if self.options.shuffle_flip_o_will and "Morio's Lab - Final Floor" in self.excluded_regions:
            self.early_backflip = True
        if self.options.shuffle_psycho_taxi and not "Arcade Panik" in self.included_levels:
            self.early_psycho_taxi = True
        if self.options.shuffle_orange_switch and not "Crash Test Industries" in self.included_levels:
            self.early_orange_switch = True
        if self.options.shuffle_golden_spring and not "Tosla HQ" in self.included_levels:
            self.early_golden_spring = True
        if self.options.shuffle_golden_propeller and not "Ruined Observatory" in self.included_levels:
            self.early_golden_propeller = True
        if self.options.shuffle_morios_password and not "Morio's Mind" in self.included_levels:
            self.early_morios_password = True
        if self.options.shuffle_rocket:
            self.early_rocket = True

        if "Morio's Lab - Fourth Floor Jump Spikes" in self.excluded_regions:
            self.exclude_spike_bunny = True
        if "Morio's Lab - Final Floor Pipes" in self.excluded_regions:
            self.exclude_top_bunny = True

        if self.options.exclude_goal_portal_checks:
            for level in self.goal_levels:
                if level in self.included_levels:
                    self.included_levels.remove(level)

        if (self.options.coinsanity and self.multiworld.players > 1 and
                self.settings.multiworld_coinsanity_percentage_cap < self.options.coinsanity_percent):
            self.options.coinsanity_percent.value = self.settings.multiworld_coinsanity_percentage_cap
            logging.warning(
                f"{self.player_name}: Your options have been modified to avoid disrupting the multiworld.\n"
                f"Coinsanity Percent has been lowered to {self.options.coinsanity_percent.value}. "
                f"You can increase this by setting 'multiworld_coinsanity_percentage_cap' in the seed "
                f"generator's host.yaml to a higher value and generating locally.")
        if self.options.coinsanity_percent == 0:
            self.options.coinsanity.value = False

        goal_portal_threshold = (50 + 5 * (len(self.included_levels) - 1))
        if (not self.options.exclude_goal_portal_checks and self.multiworld.players == 1 and self.options.goal < 1 and
                self.options.goal_portal_gear_percentage > goal_portal_threshold):
            self.options.goal_portal_gear_percentage.value = goal_portal_threshold
            logging.warning(
                f"{self.player_name}: Your options have been modified to avoid generation failures.\n"
                f"Goal Portal Gear percentage has been capped to {goal_portal_threshold}%.")

        if not self.options.open_grannys_island and self.options.locked_morios_lab:
            self.lab_start = True

        if self.options.shuffle_flip_o_will != 0 and self.options.early_move:
            move = self.random.choice(["Progressive Jump", "Progressive Boost"])
            self.multiworld.local_early_items[self.player][move] = 1


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_locations(self)
        #visualize_regions(self.get_region("Menu"), "regions_test.puml", show_entrance_names=True, linetype_ortho=False)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.YellowTaxiItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Get relevant options needed for client
        dict = self.options.as_dict(
            "death_link",
            "goal",
            "open_grannys_island",
            "locked_morios_lab",
            "locked_morios_wardrobe",
            "locked_time_trials",
            "shuffle_gela_toni",
            "shuffle_pizza_king",
            "shuffle_orange_switch",
            "shuffle_morios_password",
            "shuffle_rocket",
            "shuffle_full_game",
            "shuffle_psycho_taxi",
            "shuffle_rat",
            "gym_gears_unlock_condition",
            "fecal_matters_unlock_condition",
            "flushed_away_unlock_condition",
            "bunnysanity",
            "hatsanity",
            "checkpointsanity",
            "safesanity",
            "chestsanity",
            "coinbagsanity",
            "coinsanity",
            "cheesesanity",
            "shuffle_flip_o_will",
            "shuffle_glide",
            "shuffle_golden_spring",
            "shuffle_golden_propeller",
            "extra_demo_collectables",
        )

        dict["major_version"] = self.world_version.major
        dict["minor_version"] = self.world_version.minor
        dict["build_version"] = self.world_version.build

        # Set counts that client needs to know
        dict["goal_portal_cost"] = self.final_portal_cost
        dict["total_gears"] = self.num_gears
        dict["total_bunnies"] = self.num_bunnies

        # Set early item states, in order to make it easier to track clientside without needing to match logic
        dict["early_gela_toni"] = self.early_gela_toni
        dict["early_pizza_king"] = self.early_pizza_king
        dict["early_rat"] = self.early_rat
        #dict["early_doggo"] = self.early_doggo
        dict["early_backflip"] = self.early_backflip
        dict["early_psycho_taxi"] = self.early_psycho_taxi
        dict["early_orange_switch"] = self.early_orange_switch
        dict["early_golden_spring"] = self.early_golden_spring
        dict["early_golden_propeller"] = self.early_golden_propeller
        dict["early_morios_password"] = self.early_morios_password
        dict["early_rocket"] = self.early_rocket
        dict["early_sewer_island"] = self.early_sewer_island
        dict["funny_faces"] = self.options.funny_faces.value

        # Set excluded bunnies
        dict["exclude_top_bunny"] = self.exclude_top_bunny
        dict["exclude_spike_bunny"] = self.exclude_spike_bunny

        # Start location
        dict["lab_start"] = self.lab_start

        return dict
