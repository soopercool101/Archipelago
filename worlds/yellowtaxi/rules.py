from __future__ import annotations

import math
from typing import TYPE_CHECKING, Callable, Mapping, Union

from .data_loader import regions_json_data
from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import add_rule, set_rule
from rule_builder.rules import Rule, True_, False_, Has, CanReachRegion, CanReachLocation

if TYPE_CHECKING:
    from .world import YellowTaxiWorld


def set_all_rules(world: YellowTaxiWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.
    rf = RuleFactory(world)
    set_all_entrance_location_rules(world, rf)
    set_completion_condition(world)


def set_all_entrance_location_rules(world: YellowTaxiWorld, rf: RuleFactory) -> None:
    for region in world.get_regions():
        region_name = region.name
        if region_name == "Menu": # Menu doesn't have json data or any rules
            continue
        reg = regions_json_data[region_name]

        # Basic connections
        for connect, rule in reg["connections"].items():
            if rule:
                rf.assign_connection_rule(region_name, connect, rule)

        # Subwarps
        for subwarp, connect_and_rule in reg["subwarps"].items():
            rule = connect_and_rule[1]
            if rule:
                rf.assign_entrance_rule(subwarp, rule)

        # Warps
        for warp, connect_and_rule in reg["warps"].items():
            rule = connect_and_rule[1]
            if rule:
                rf.assign_entrance_rule(warp, rule)

        # Cheeses
        if world.options.cheesesanity:
            for cheese in reg["cheeses"]:
                try:
                    cheese_loc = world.get_location(cheese)
                    world.set_rule(cheese_loc, Has("Michele"))
                except KeyError:
                    break # If cheese doesn't exist here, region has no items

        # Special rules
        for location, rule in reg["specialrules"].items():
            rf.assign_location_rule(location, rule)

def set_completion_condition(world: YellowTaxiWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)


# Shamelessly copying SM64's rule factory implementation
class RuleFactory:
    world: YellowTaxiWorld

    class YTGVLogicException(Exception):
        pass

    def __init__(self, world: YellowTaxiWorld):
        self.world = world

    def assign_location_rule(self, target_name: str, rule_expr: str):
        try:
            target = self.world.get_location(target_name)
        except KeyError:
            return
        if target is None:
            return
        try:
            rule = self.build_rule(rule_expr)
        except RuleFactory.YTGVLogicException as exception:
            raise RuleFactory.YTGVLogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule is not None:
            self.world.set_rule(target, rule)

    def assign_connection_rule(self, region_from: str, region_to: str, rule_expr: str):
        self.assign_entrance_rule(f"{region_from} -> {region_to}", rule_expr)

    def assign_entrance_rule(self, entrance_name: str, rule_expr: str):
        try:
            target = self.world.get_entrance(entrance_name)
        except KeyError:
            return
        if target is None:
            return
        try:
            rule = self.build_rule(rule_expr)
        except RuleFactory.YTGVLogicException as exception:
            raise RuleFactory.YTGVLogicException(
                f"Error generating rule for {entrance_name} using rule expression {rule_expr}: {exception}")
        if rule is not None:
            self.world.set_rule(target, rule)

    def build_rule(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rule: Union[Rule | None] = None
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression)
            if rule is None:
                rule = or_clause
            else:
                rule = rule | or_clause
        if rule is None:
            return True_()
        return rule

    def combine_and_clauses(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" & ")
        rule: Union[Rule | None] = None
        for expression in expressions:
            and_clause = self.evaluate_subclause(expression)
            if rule is None:
                rule = and_clause
            else:
                rule = rule & and_clause
        if rule is None:
            return True_()
        return rule

    def evaluate_subclause(self, expression: str) -> Rule:
        if '+' in expression:
            tokens = expression.split('+')
            rule: Union[Rule | None] = None
            for token in tokens:
                item = self.parse_token(token)
                if rule is None:
                    rule = item
                else:
                    rule = rule & item
            if rule is None:
                return True_()
            return rule
        if '/' in expression:
            tokens = expression.split('/')
            rule: Union[Rule | None] = None
            for token in tokens:
                item = self.parse_token(token)
                if rule is None:
                    rule = item
                else:
                    rule = rule | item
            if rule is None:
                return True_()
            return rule
        if '{{' in expression:
            return CanReachLocation(expression[2:-2])
        if '{' in expression:
            return CanReachRegion(expression[1:-1])
        return self.parse_token(expression)

    def parse_token(self, token: str) -> Rule:
        if token == "B1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has("Progressive Boost")
        if token == "B2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has("Progressive Boost", 2)
        if token == "J1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has("Progressive Jump")
        if token == "J2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has("Progressive Jump", 2)
        if token == "SP":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has("Spin Attack")
        if token == "GS":
            return Has("Golden Spring Unlock")
        if token == "GST":
            if self.world.options.shuffle_golden_spring == 0:
                return True_()
            return Has("Golden Spring Unlock")
        if token == "OS":
            return Has("Orange Switch")
        if token == "GP":
            return Has("Golden Propeller Unlock")
        if token == "FGU":
            if self.world.options.shuffle_full_game == 0:
                return True_()
            return Has("Full Game Unlock")
        if token == "GelaToni":
            return Has("Gela-Toni")
        if token == "PizzaKing":
            return Has("Pizza King")
        if token == "Doggo":
            match self.world.options.fecal_matters_unlock_condition:
                case self.world.options.fecal_matters_unlock_condition.option_open:
                    return True_()
                case self.world.options.fecal_matters_unlock_condition.option_full_game:
                    if self.world.options.shuffle_full_game == 0:
                        return True_()
                    return Has("Full Game Unlock")
                case self.world.options.fecal_matters_unlock_condition.option_vanilla |\
                     self.world.options.fecal_matters_unlock_condition.option_shuffle_doggo:
                    return Has("Doggo")
                case self.world.options.fecal_matters_unlock_condition.option_exclude:
                    return False_()
        if token == "Password":
            return Has("Morio's Password")
        if token == "Rocket":
            return Has("Mosk's Rocket")
        if token == "MorioHat":
            return Has("Morio Hat")
        if token == "MoskHat":
            return Has("Alien Mosk Hat (Good)")
        # Portals. TODO: Allow variable portal costs beyond just final portal
        if token == "PortalMorioHome":
            return Has("Gear", 3)
        if token == "PortalBombeach":
            if self.world.options.goal == 0:
                self.world.final_portal_cost = math.floor((self.world.num_gears * self.world.options.goal_portal_gear_percentage) / 100)
                return Has("Gear", self.world.final_portal_cost)

            return Has("Gear", 6)
        if token == "PortalArcadePanik":
            return Has("Gear", 18)
        if token == "PortalPizzaTime":
            return Has("Gear", 32)
        if token == "PortalToslaOffices":
            if self.world.options.goal == 1:
                self.world.final_portal_cost = math.floor((self.world.num_gears * self.world.options.goal_portal_gear_percentage) / 100)
                return Has("Gear", self.world.final_portal_cost)

            return Has("Gear", 50)
        if token == "PortalGymGears":
            return True_()
        if token == "PortalFecalMatters":
            return True_()
        if token == "PortalFlushedAway":
            return True_()
        if token == "PortalMauriziosCity":
            return Has("Gear", 65)
        if token == "PortalCrashTestIndustries":
            return Has("Gear", 80)
        if token == "PortalMoriosMind":
            return True_()
        if token == "PortalRuinedObservatory":
            return True_()
        if token == "PortalToslaHQ":
            if self.world.options.goal == 2:
                self.world.final_portal_cost = math.floor((self.world.num_gears * self.world.options.goal_portal_gear_percentage) / 100)
                return Has("Gear", self.world.final_portal_cost)

            return Has("Gear", 130)
        if token == "NPR":
            # No Portal randomization. Placeholder rule for now.
            return True_()
        if token == "NSAR":
            # No Subarea randomization. Placeholder rule for now.
            return True_()
        if token == "NHPR":
            # No Hub Portal randomization. Placeholder rule for now.
            # Hub portals launch you upwards when declining entry, making them logical access rules in some cases.
            return True_()
        if token == "OGI":
            if self.world.options.open_grannys_island.value == 1:
                return True_()
            return False_()
        if token == "LabKey":
            if self.world.options.locked_morios_lab:
                return Has("Lab Key")
            return True_()
        if token == "WardrobeKey":
            if self.world.options.locked_morios_wardrobe:
                return Has("Morio's Wardrobe")
            return True_()
        if token == "GymKey":
            match self.world.options.gym_gears_unlock_condition:
                case self.world.options.gym_gears_unlock_condition.option_open:
                    return True_()
                case self.world.options.gym_gears_unlock_condition.option_full_game:
                    if self.world.options.shuffle_full_game == 0:
                        return True_()
                    return Has("Full Game Unlock")
                case self.world.options.gym_gears_unlock_condition.option_shuffle_gym_membership:
                    return Has("Gym Membership")
                case self.world.options.gym_gears_unlock_condition.option_exclude:
                    return False_()
        if token == "HatMembership":
            return True_()
        if token == "SewerKey":
            match self.world.options.flushed_away_unlock_condition:
                case self.world.options.flushed_away_unlock_condition.option_open:
                    return True_()
                case self.world.options.flushed_away_unlock_condition.option_full_game | self.world.options.flushed_away_unlock_condition.option_default:
                    if self.world.options.shuffle_full_game == 0:
                        return True_()
                    return Has("Full Game Unlock")
                case self.world.options.flushed_away_unlock_condition.option_shuffle_sewer_key:
                    return Has("Sewer Key")
                case self.world.options.flushed_away_unlock_condition.option_exclude:
                    return False_()
        if token == "EarlySewer":
            if self.world.early_sewer_island:
                return True_()
            return False_()
        if token == "TT1":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Baby Steps!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote")
        if token == "TT2":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Getting Gud!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote", 2)
        if token == "TT3":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Pro Tricks!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote", 3)
        if token == "NHS":
            if self.world.options.hatsanity == 0:
                return True_()
            return False_()
        if token == "HS":
            if self.world.options.hatsanity != 0:
                return True_()
            return False_()
        if token.startswith("Bunny-"):
            bunny_level : str = token[len("Bunny-"):]
            if bunny_level == "Hub":
                hub_bunnies = 3
                if self.world.options.extra_demo_collectables:
                    hub_bunnies += 2
                if self.world.exclude_spike_bunny:
                    hub_bunnies -= 1
                if self.world.exclude_top_bunny:
                    hub_bunnies -= 1
                return Has("Bunny (Morio's Lab)", hub_bunnies)
            else:
                adjusted_bunny_level : str = bunny_level
                match bunny_level:
                    case "MH":
                        adjusted_bunny_level = "Morio's Home"
                    case "BB":
                        adjusted_bunny_level = "Bombeach"
                    case "GG":
                        adjusted_bunny_level = "Gym Gears"
                    case "FM":
                        adjusted_bunny_level = "Fecal Matters"
                    case "FA":
                        adjusted_bunny_level = "Flushed Away"
                return Has(f"Bunny ({adjusted_bunny_level})", 3)
        if token.startswith("X"):
            expert_level = int(token[1:])
            if (hasattr(self.world.multiworld, "generation_is_fake")
                    and self.world.options.expert_level < expert_level):
                return Has("Glitched Logic", expert_level - self.world.options.expert_level)
            if self.world.options.expert_level >= expert_level:
                return True_()
            return False_()

        raise Exception(f"Invalid token: '{token}'")
