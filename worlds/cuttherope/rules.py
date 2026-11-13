from __future__ import annotations

import math
from typing import TYPE_CHECKING, Callable, Mapping, Union, override, ClassVar

from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from .data_loader import regions_json_data
from BaseClasses import CollectionState, Location
from rule_builder.rules import Rule, True_, False_, Has, CanReachRegion, CanReachLocation

if TYPE_CHECKING:
    from .world import CutTheRopeWorld

# Shamelessly copying SM64's rule factory implementation
class RuleFactory:
    world: CutTheRopeWorld

    class CutTheRopeLogicException(Exception):
        pass

    def __init__(self, world: CutTheRopeWorld):
        self.world = world
        self.skip_unnecessary_rule_calculations = not self.world.using_ut
        self.cached_complex_rules : dict[str, Rule] = {}

    def build_rule(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rule: Union[Rule | None] = None
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression)
            if self.skip_unnecessary_rule_calculations and or_clause.Resolved.always_true:
                return True_()
            if rule is None:
                rule = or_clause
            else:
                rule |= or_clause
        if rule is None:
            return True_()
        return rule

    def combine_and_clauses(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" & ")
        rule: Union[Rule | None] = None
        for expression in expressions:
            and_clause = self.evaluate_subclause(expression)
            if self.skip_unnecessary_rule_calculations and and_clause.Resolved.always_false:
                return False_()
            if rule is None:
                rule = and_clause
            else:
                rule &= and_clause
        if rule is None:
            return True_()
        return rule

    def evaluate_subclause(self, expression: str) -> Rule:
        if '+' in expression:
            tokens = expression.split('+')
            rule: Union[Rule | None] = None
            for token in tokens:
                and_clause = self.parse_token(token)
                if self.skip_unnecessary_rule_calculations and and_clause.Resolved.always_false:
                    return False_()
                if rule is None:
                    rule = and_clause
                else:
                    rule &= and_clause
            if rule is None:
                return True_()
            return rule
        if '/' in expression:
            tokens = expression.split('/')
            rule: Union[Rule | None] = None
            for token in tokens:
                or_clause = self.parse_token(token)
                if self.skip_unnecessary_rule_calculations and or_clause.Resolved.always_true:
                    return True_()
                if rule is None:
                    rule = or_clause
                else:
                    rule |= or_clause
            if rule is None:
                return True_()
            return rule
        return self.parse_token(expression)

    def parse_token(self, token: str) -> Rule:
        if token == "Bu":
            self.world.has_bubble = True
            return Has("Bubbles")
        if token == "AR":
            self.world.has_autograb = True
            return Has("Automatic Ropes")
        if token == "AC":
            self.world.has_air_cushion = True
            return Has("Air Cushions")
        if token == "SD":
            if not self.world.options.disable_spikes_item:
                return False_()
            self.world.spikes_progression = True
            return Has("Disable Spikes")
        if token == "TS":
            if not self.world.options.star_timer_disable_item:
                return False_()
            self.world.timed_star_progression = True
            return Has("Disable Star Timers")
        if token.startswith("X"):
            expert_level = int(token[1:])
            if self.world.using_ut and self.world.options.expert_level < expert_level:
                return Has(self.world.glitches_item_name, expert_level - self.world.options.expert_level)
            if self.world.options.expert_level >= expert_level:
                return True_()
            return False_()

        raise Exception(f"Invalid token: '{token}'")
