from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import CutTheRopeWorld

BOX_ITEMS = [
    "Cardboard Box",
    "Fabric Box",
    "Foil Box",
    "Magic Box",
    "Valentine Box",
    "Toy Box",
    "Gift Box",
    "Cosmic Box",
    "Toolbox",
    "Buzz Box",
    "DJ Box",
]

ITEM_NAME_TO_ID = {
    # Star MacGuffins
    "Star": 1,
    # Filler (Boring)
    "Nothing": 2,
    # Filler (Thematic)
    "Tasty Candy": 3,
    # Puzzle Elements
    "Tutorials": 1_00,
    "Bubbles": 1_01,
    "Automatic Ropes": 1_02,
    "Air Cushions": 1_03,
    "Sliders": 1_04,
    "Electric Gates": 1_05,
    "Hats": 1_06,
    "Bouncers": 1_07,
    "Wheels": 1_08,
    "Gravity Buttons": 1_09,
    "Blades": 1_10,
    "Bees": 1_11,
    "Records": 1_12,
    "Disable Spikes": 2_00,
    "Disable Star Timers": 2_01,
    "Progressive Electric Gates": 2_05,
    "Progressive Blades": 2_10,
    
    # Boxes
    "Cardboard Box": 10_01, # Probably unused unless I do a "starting box"
    "Fabric Box": 10_02,
    "Foil Box": 10_03,
    "Magic Box": 10_04,
    "Valentine Box": 10_05,
    "Toy Box": 10_06,
    "Gift Box": 10_07,
    "Cosmic Box": 10_08,
    "Toolbox": 10_09,
    "Buzz Box": 10_10,
    "DJ Box": 10_11, # Probably unused unless I make goal box selectable while still having more boxes
}

class CutTheRopeItem(Item):
    game = "Cut the Rope"


def get_random_filler_item_name(world: CutTheRopeWorld) -> str:
    return "Nothing"


def create_item_with_correct_classification(world: CutTheRopeWorld, name: str) -> CutTheRopeItem:
    # Majority of this game's items are progression, so make that the default
    classification : ItemClassification = ItemClassification.progression

    # MacGuffin, deprioritize and skip balancing
    if name == "Star":
        classification = ItemClassification.progression_deprioritized_skip_balancing

    # Filler
    if name in ["Tutorials", "Nothing", "Tasty Candy"]:
        classification = ItemClassification.filler

    # Possibly useful
    if name == "Disable Spikes" and not world.spikes_progression:
        classification = ItemClassification.useful
    if name == "Star Timer Disable" and not world.timed_star_progression:
        classification = ItemClassification.useful

    return CutTheRopeItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: CutTheRopeWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = []

    if world.has_bubble:
        itempool.append(world.create_item("Bubbles"))
    if world.has_autograb:
        itempool.append(world.create_item("Automatic Ropes"))
    if world.has_air_cushion:
        itempool.append(world.create_item("Air Cushions"))
    if world.has_slider:
        itempool.append(world.create_item("Sliders"))
    if world.has_electric_gates:
        if world.options.progressive_electric_sparks:
            itempool += [world.create_item("Progressive Electric Gates") for _ in range(2)]
        else:
            itempool.append(world.create_item("Electric Gates"))
    if world.has_hat:
        itempool.append(world.create_item("Hats"))
    if world.has_bouncer:
        itempool.append(world.create_item("Bouncer"))
    if world.has_wheel:
        itempool.append(world.create_item("Wheels"))
    if world.has_gravity_button:
        itempool.append(world.create_item("Gravity Buttons"))
    if world.has_blade:
        if world.options.progressive_blades:
            itempool += [world.create_item("Progressive Blades") for _ in range(2)]
        else:
            itempool.append(world.create_item("Blades"))
    if world.has_bee:
        itempool.append(world.create_item("Bees"))
    if world.has_record:
        itempool.append(world.create_item("Records"))

    if world.options.disable_spikes_item:
        itempool.append(world.create_item("Disable Spikes"))

    if world.options.star_timer_disable_item:
        itempool.append(world.create_item("Disable Star Timers"))

    if world.options.tutorials_item:
        itempool.append(world.create_item("Tutorials"))

    # Make goal-required stars
    itempool += [world.create_item("Star") for _ in range(world.options.goal_box_star_requirement)]

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Make extra stars
    max_extra_stars = number_of_unfilled_locations - len(itempool)
    if max_extra_stars > 0 and world.options.extra_stars.value > 0:
        itempool += [world.create_item("Star") for _ in range(min(max_extra_stars, world.options.extra_stars.value))]

    # Make filler
    needed_number_of_filler_items = number_of_unfilled_locations - len(itempool)

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
