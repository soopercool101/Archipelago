from typing import TYPE_CHECKING, Dict, List, Tuple

from random import Random

from . import data_loader
from .data_loader import (original_portal_level_order, alternative_portal_level_order, grannys_island_level_order,
                          miscellaneous_level_order, unfinished_levels)
from .options import YellowTaxiOptions

def get_level_order(options: YellowTaxiOptions, random: Random, goal_portal : str) -> List[str]:
    goal_portal_index : int = -1
    num_portals : int = 0
    level_order : List[str] = []

    if options.portal_order.value == options.portal_order.option_internal:
        portal_levels = alternative_portal_level_order

    if options.use_separate_entrance_pools or True:
        perform_pooled_randomization(options, random, goal_portal)

    return level_order

def perform_pooled_randomization(options: YellowTaxiOptions, random: Random, goal_portal : str) -> List[str]:
    shuffle_pools : Dict[str, List[str]] = {}
    level_order : List[str] = []

    portal_order : List[str] = []
    if options.portal_order.value == options.portal_order.option_shuffle:
        num_portals : int
        valid_portals : List[str]
        num_portals, valid_portals = get_portal_randomization_count_and_pool(options, goal_portal)
        random.shuffle(valid_portals)
        goal_portal_index : int = original_portal_level_order.index(goal_portal)
        valid_portals.insert(goal_portal_index, goal_portal)
        for i in range(0, len(original_portal_level_order)):
            if i < num_portals:
                portal_order += [valid_portals[i]]
            else:
                portal_order += ["Excluded"]
    else:
        base_portal_order : List[str]
        if options.portal_order.value == options.portal_order.option_internal:
            base_portal_order = alternative_portal_level_order
        else:
            base_portal_order = list(original_portal_level_order)

        skip_remaining : bool = False
        for portal in base_portal_order:
            if portal == goal_portal and options.remove_post_goal_portals:
                skip_remaining = True
            elif skip_remaining:
                portal_order += ["Excluded"]
                continue
            portal_order += [portal]

    grannys_order : List[str] = []
    if options.shuffle_grannys_levels:
        valid_grannys : List[str] = []
        if (options.allow_shuffling_removed_levels.value >=
                options.allow_shuffling_removed_levels.option_main_levels_only):
            valid_grannys = ["Gym Gears", "Fecal Matters", "Flushed Away"]
        else:
            if options.gym_gears_unlock_condition.value != options.gym_gears_unlock_condition.option_exclude:
                valid_grannys += ["Gym Gears"]
            if options.fecal_matters_unlock_condition.value != options.fecal_matters_unlock_condition.option_exclude:
                valid_grannys += ["Fecal Matters"]
            # Limitation: Logical access to sewer island isn't considered here.
            # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
            if options.flushed_away_unlock_condition.value != options.flushed_away_unlock_condition.option_exclude:
                valid_grannys += ["Flushed Away"]

        random.shuffle(valid_grannys)

        grannys_index : int = 0

        if options.gym_gears_unlock_condition.value != options.gym_gears_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]
        if options.fecal_matters_unlock_condition.value != options.fecal_matters_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]
        # Limitation: Logical access to sewer island isn't considered here.
        # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
        if options.flushed_away_unlock_condition.value != options.flushed_away_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]
    else:
        grannys_order = list(grannys_island_level_order)

        if options.gym_gears_unlock_condition.value == options.gym_gears_unlock_condition.option_exclude:
            grannys_order[0] = "Excluded"
        if options.fecal_matters_unlock_condition.value == options.fecal_matters_unlock_condition.option_exclude:
            grannys_order[1] = "Excluded"
        # Limitation: Logical access to sewer island isn't considered here.
        # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
        if options.flushed_away_unlock_condition.value == options.flushed_away_unlock_condition.option_exclude:
            grannys_order[2] = "Excluded"


    misc_order : List[str] = []
    valid_misc : List[str] = []
    shuffle_any_misc : bool = False
    if (options.shuffle_rocket_entrance and options.rocket_unlock_condition.value !=
            options.rocket_unlock_condition.option_exclude):
        valid_misc += [miscellaneous_level_order[0]]
    if options.shuffle_time_trial_entrances:
        valid_misc += list(miscellaneous_level_order[1:4])
    if (options.shuffle_psycho_taxi_entrance and
            options.psycho_taxi_unlock_condition.value != options.psycho_taxi_unlock_condition.option_exclude):
        valid_misc += [miscellaneous_level_order[4]]

    random.shuffle(valid_misc)

    misc_index : int = 0

    if options.rocket_unlock_condition.value == options.rocket_unlock_condition.option_exclude:
        misc_order += ["Excluded"]
    elif options.shuffle_rocket_entrance:
        misc_order += [valid_misc[misc_index]]
        misc_index += 1
    else:
        misc_order += [str(miscellaneous_level_order[0])]

    # Time trials don't get excluded in the same way as other levels
    if options.shuffle_time_trial_entrances:
        misc_order += list(valid_misc[misc_index:misc_index+3])
        misc_index += 3
    else:
        misc_order += list(miscellaneous_level_order[1:3])

    if options.psycho_taxi_unlock_condition.value == options.psycho_taxi_unlock_condition.option_exclude:
        misc_order += ["Excluded"]
    elif options.shuffle_psycho_taxi_entrance:
        misc_order += [valid_misc[misc_index]]
    else:
        misc_order += [str(miscellaneous_level_order[4])]

    return portal_order + grannys_order + misc_order

def get_portal_randomization_count_and_pool(options: YellowTaxiOptions, goal_portal : str) -> Tuple[int, List[str]]:
    num_portals : int = 0
    valid_portals : List[str] = []
    past_goal : bool = False
    no_extras_in_pool : bool = (options.allow_shuffling_removed_levels.value ==
                                options.allow_shuffling_removed_levels.option_none)
    goal_portal_index : int = -1
    for portal in original_portal_level_order:
        if portal in unfinished_levels:
            continue
        if portal == goal_portal:
            past_goal = True
            num_portals += 1
            continue

        if past_goal and options.remove_post_goal_portals:
            if no_extras_in_pool:
                break
            else:
                continue
        else:
            valid_portals += [portal]
        num_portals += 1

    return num_portals, valid_portals