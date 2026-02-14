from collections.abc import Mapping
from typing import Any, Dict, List

from BaseClasses import MultiWorld
from Utils import visualize_regions
from worlds.AutoWorld import World

from . import data_loader, items, regions, locations, rules, web_world
from . import options as taxi_options


class YellowTaxiWorld(World):
    #TODO: Better description
    """
    Yellow Taxi Goes Vroom is a trippy arcade platformer ready to take you on a crazy adventure!
    """

    game = "Yellow Taxi Goes Vroom"

    web = web_world.YellowTaxiWebWorld()

    options_dataclass = taxi_options.YellowTaxiOptions
    options: taxi_options.YellowTaxiOptions

    regions_json: Dict[str, Any] = data_loader.regions_json_data
    location_name_to_id = data_loader.all_locations
    item_name_to_id = items.ITEM_NAME_TO_ID

    # Keeping default Menu region, just in case I want random starting location down the line
    origin_region_name = "Menu"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.num_gears : int = 0
        self.excluded_regions : List[str] = []
        self.included_levels : List[str] = []
        self.early_pizza_king : bool = False
        self.early_rat : bool = False
        self.early_doggo : bool = False
        self.early_backflip : bool = False
        self.early_psycho_taxi : bool = False

    def generate_early(self) -> None:
        # Determine which regions are not going to be included

        self.num_gears = 0
        self.excluded_regions = []
        self.included_levels = []

        # Include levels up to the goal
        # Always included levels
        self.included_levels = [
            "Hub",
            "Morio's Home",
            "Bombeach",
            "Gym Gears",
            "Fecal Matters",    # Remove this later if doggo is unreachable
        ]

        # Exclude unreachable hub areas past the goal
        # Rocket isn't pre-goal for any current goal types
        if not self.options.shuffle_rocket:
            self.excluded_regions += ["Granny's Island - Top of Rocket"]
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
                                          "Crash Again - Entrance",
                                          "Granny's Island - Sewer Island",
                                          "Granny's Island - Sewer Island Upper"]
            else:
                self.included_levels += ["Flushed Away"]
            # Cannot reach these spiky areas without golden spring
            if not self.options.shuffle_golden_spring:
                self.excluded_regions += ["Morio's Lab - Fourth Floor Jump Spikes"]
                if self.options.expert_level < 2:
                    self.excluded_regions += ["Morio's Lab - Fourth Floor Expert Jump Spikes"]
            # Can reach the upper floors via either morio's password (go backwards through pipe), OS or GS
            if (not self.options.shuffle_golden_spring and not self.options.shuffle_morios_password
                    and not self.options.shuffle_orange_switch):
                self.excluded_regions += ["Morio's Lab - Fourth Floor",
                                          "Morio's Lab - Ledge Above Maurizio's City Portal",
                                          "Morio's Lab - Fifth Floor Crash Test Area",
                                          "Morio's Lab - Fifth Floor Morio's Mind Area"]
                # This can be accessed in expert 2+, but not before
                if self.options.expert_level >= 2:
                    self.excluded_regions += ["Morio's Lab - Fourth Floor Expert Jump Spikes"]
                # Cannot include fecal matters if you cannot reach doggo
                if not self.options.shuffle_doggo:
                    self.included_levels.remove("Fecal Matters")
            # Final floor is hard locked behind Morio's Password
            if not self.options.shuffle_morios_password:
                self.excluded_regions += ["Morio's Lab - Fifth Floor Ruined Observatory Area",
                                          "Morio's Lab - Fifth Floor Golden Propeller",
                                          "Morio's Lab - Ledge Above Ruined Observatory Portal",
                                          "Morio's Lab - Ledge Below Tosla HQ Portal",
                                          "Morio's Lab - Fifth Floor Low Pillars",
                                          "Morio's Lab - Fifth Floor High Pillars",
                                          "Morio's Lab - Final Floor",
                                          "Morio's Lab - Final Floor Pipes",
                                          "Morio's Lab - Final Floor Catwalk"]

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_locations(self)
        visualize_regions(self.get_region("Menu"), "regions_test.puml", show_entrance_names=True, linetype_ortho=False)

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
            "shuffle_gela_toni",
            "shuffle_pizza_king",
            "shuffle_doggo",
            "shuffle_orange_switch",
            "shuffle_morios_password",
            "shuffle_rocket",
            "shuffle_full_game",
            "shuffle_psycho_taxi",
            "shuffle_rat",
            "bunnysanity",
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

        # IMPORTANT!! NEED TO INCREMENT THIS WHENEVER BREAKING APWORLD CHANGES ARE MADE!!
        dict["major_version"] = 0
        dict["minor_version"] = 1
        dict["early_pizza_king"] = self.early_pizza_king
        dict["early_rat"] = self.early_rat
        dict["early_doggo"] = self.early_doggo
        dict["early_backflip"] = self.early_backflip
        dict["early_psycho_taxi"] = self.early_psycho_taxi
        return dict
