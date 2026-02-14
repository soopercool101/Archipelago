from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Mapping, Union

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import add_rule, set_rule

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
    for reg in world.regions_json.values():
        region_name = reg["name"]

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
                cheese_loc = world.get_location(cheese)
                set_rule(cheese_loc, lambda state: state.has("Michele", world.player))

        # Special rules
        for location, rule in reg["specialrules"].items():
            rf.assign_location_rule(location, rule)

    return
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    overworld_to_bottom_right_room = world.get_entrance("Overworld to Bottom Right Room")
    overworld_to_top_left_room = world.get_entrance("Overworld to Top Left Room")
    right_room_to_final_boss_room = world.get_entrance("Right Room to Final Boss Room")

    # An access rule is a function. We can define this function like any other function.
    # This function must accept exactly one parameter: A "CollectionState".
    # A CollectionState describes the current progress of the players in the multiworld, i.e. what items they have,
    # which regions they've reached, etc.
    # In an access rule, we can ask whether the player has a collected a certain item.
    # We can do this via the state.has(...) function.
    # This function takes an item name, a player number, and an optional count parameter (more on that below)
    # Since a rule only takes a CollectionState parameter, but we also need the player number in the state.has call,
    # our function needs to be locally defined so that it has access to the player number from the outer scope.
    # In our case, we are inside a function that has access to the "world" parameter, so we can use world.player.
    def can_destroy_bush(state: CollectionState) -> bool:
        return state.has("Sword", world.player)

    # Now we can set our "can_destroy_bush" rule to our entrance which requires slashing a bush to clear the path.
    # One way to set rules is via the set_rule() function, which works on both Entrances and Locations.
    set_rule(overworld_to_bottom_right_room, can_destroy_bush)

    # Because the function has to be defined locally, most worlds prefer the lambda syntax.
    set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))

    # Conditions can depend on event items.
    set_rule(right_room_to_final_boss_room, lambda state: state.has("Top Left Room Button Pressed", world.player))

    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    if world.options.hammer:
        overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
        set_rule(overworld_to_top_middle_room, lambda state: state.has("Hammer", world.player))


#def set_all_location_rules(world: YellowTaxiWorld, rf: RuleFactory) -> None:
    #return
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # Sometimes, you may want to have different rules depending on the player's chosen options.
    # There is a wrong way to do this, and a right way to do this. Let's do the wrong way first.
    right_room_enemy = world.get_location("Right Room Enemy Drop")

    # DON'T DO THIS!!!!
    set_rule(
        right_room_enemy,
        lambda state: (
            state.has("Sword", world.player)
            and (not world.options.hard_mode or state.has_any(("Shield", "Health Upgrade"), world.player))
        ),
    )
    # DON'T DO THIS!!!!

    # Now, what's actually wrong with this? It works perfectly fine, right?
    # If hard mode disabled, Sword is enough. If hard mode is enabled, we also need a Shield or a Health Upgrade.
    # The access rule we just wrote does this correctly, so what's the problem?
    # The problem is performance.
    # Most of your world code doesn't need to be perfectly performant, since it just runs once per slot.
    # However, access rules in particular are by far the hottest code path in Archipelago.
    # An access rule will potentially be called thousands or even millions of times over the course of one generation.
    # As a result, access rules are the one place where it's really worth putting in some effort to optimize.
    # What's the performance problem here?
    # Every time our access rule is called, it has to evaluate whether world.options.hard_mode is True or False.
    # Wouldn't it be better if in easy mode, the access rule only checked for Sword to begin with?
    # Wouldn't it also be better if in hard mode, it already knew it had to check Shield and Health Upgrade as well?
    # Well, we can achieve this by doing the "if world.options.hard_mode" check outside the set_rule call,
    # and instead having two *different* set_rule calls depending on which case we're in.

    if world.options.hard_mode:
        # If you have multiple conditions, you can obviously chain them via "or" or "and".
        # However, there are also the nice helper functions "state.has_any" and "state.has_all".
        set_rule(
            right_room_enemy,
            lambda state: (
                state.has("Sword", world.player) and state.has_any(("Shield", "Health Upgrade"), world.player)
            ),
        )
    else:
        set_rule(right_room_enemy, lambda state: state.has("Sword", world.player))

    # Another way to chain multiple conditions is via the add_rule function.
    # This makes the access rules a bit slower though, so it should only be used if your structure justifies it.
    # In our case, it's pretty useful because hard mode and easy mode have different requirements.
    final_boss = world.get_location("Final Boss Defeated")

    # For the "known" requirements, it's still better to chain them using a normal "and" condition.
    add_rule(final_boss, lambda state: state.has_all(("Sword", "Shield"), world.player))

    if world.options.hard_mode:
        # You can check for multiple copies of an item by using the optional count parameter of state.has().
        add_rule(final_boss, lambda state: state.has("Health Upgrade", world.player, 2))


def set_completion_condition(world: YellowTaxiWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    #world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Sword", "Shield"), world.player)

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    #world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Gear", world.player, world.num_gears - 3) and state.can_reach(world.get_region("Morio's Lab - Final Floor"))


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
        if rule == False:
            raise RuleFactory.YTGVLogicException(
                f"Error: {target_name} rule expression {rule_expr} always returns False")
        elif rule:
            set_rule(target, rule)

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
        if rule == False: # Entrances may only be accessible on certain difficulties
            set_rule(target, lambda state: False)
        elif rule:
            set_rule(target, rule)

    def build_rule(self, rule_expr: str) -> Union[Callable, bool, None]:
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rules = []
        any_failed_rules = False
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression)
            if or_clause is True:
                return None
            if or_clause is not False:
                rules.append(or_clause)
            else:
                any_failed_rules = True
        if rules:
            if len(rules) == 1:
                return lambda state: rules[0](state)
            else:
                return lambda state: any(rule(state) for rule in rules)
        elif any_failed_rules:
            return False
        return None

    def combine_and_clauses(self, rule_expr: str) -> Union[Callable, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_lambda(expression)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

    def make_lambda(self, expression: str) -> Union[Callable, bool]:
        if '+' in expression:
            tokens = expression.split('+')
            items: dict[str, int] = {}
            for token in tokens:
                item = self.parse_token(token)
                if item is True:
                    continue
                if item is False:
                    return False
                items[item[0]] = int(item[1])
            if items:
                if all(c == 1 for c in items.values()):
                    return lambda state: state.has_all(list(items), self.world.player)
                return lambda state: state.has_all_counts(items, self.world.player)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            items: dict[str, int] = {}
            for token in tokens:
                item = self.parse_token(token)
                if item is True:
                    return True
                if item is False:
                    continue
                items[item[0]] = int(item[1])
            if items:
                if all(c == 1 for c in items.values()):
                    return lambda state: state.has_any(list(items), self.world.player)
                return lambda state: state.has_any_count(items, self.world.player)
            else:
                return False
        if '{{' in expression:
            return lambda state: state.can_reach(expression[2:-2], "Location", self.world.player)
        if '{' in expression:
            return lambda state: state.can_reach(expression[1:-1], "Region", self.world.player)
        item = self.parse_token(expression)
        if item in (True, False):
            return item
        return lambda state: state.has(item[0], self.world.player, item[1])

    def parse_token(self, token: str) -> Union[tuple[str, int], bool]:
        if token == "B1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True
            return "Progressive Boost", 1
        if token == "B2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True
            return "Progressive Boost", 2
        if token == "J1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True
            return "Progressive Jump", 1
        if token == "J2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True
            return "Progressive Jump", 2
        if token == "SP":
            if self.world.options.shuffle_flip_o_will == 0:
                return True
            return "Spin Attack", 1
        if token == "GS":
            return "Golden Spring Unlock", 1
        if token == "GST":
            if self.world.options.shuffle_golden_spring == 0:
                return True
            return "Golden Spring Unlock", 1
        if token == "OS":
            return "Orange Switch", 1
        if token == "GP":
            return "Golden Propeller Unlock", 1
        if token == "FGU":
            if self.world.options.shuffle_full_game == 0:
                return True
            return "Full Game Unlock", 1
        if token == "GelaToni":
            return "Gela-Toni", 1
        if token == "PizzaKing":
            return "Pizza King", 1
        if token == "Doggo":
            return "Doggo", 1
        if token == "Password":
            return "Morio's Password", 1
        if token == "Rocket":
            return "Mosk's Rocket", 1
        if token == "MorioHat":
            return "Morio Hat", 1
        if token == "MoskHat":
            return "Mosk Hat", 1
        # Portals. TODO: Allow variable portal costs
        if token == "PortalMorioHome":
            return "Gear", 3
        if token == "PortalBombeach":
            return "Gear", 6
        if token == "PortalArcadePanik":
            return "Gear", 18
        if token == "PortalPizzaTime":
            return "Gear", 32
        if token == "PortalToslaOffices":
            return "Gear", 50
        if token == "PortalGymGears":
            return True
        if token == "PortalFecalMatters":
            return True
        if token == "PortalFlushedAway":
            return True
        if token == "PortalMauriziosCity":
            return "Gear", 65
        if token == "PortalCrashTestIndustries":
            return "Gear", 80
        if token == "PortalMoriosMind":
            return True
        if token == "PortalRuinedObservatory":
            return True
        if token == "PortalToslaHQ":
            return "Gear", 130
        if token.startswith("X"):
            expert_level = int(token[1:])
            return self.world.options.expert_level >= expert_level

        raise Exception(f"Invalid token: '{token}'")
