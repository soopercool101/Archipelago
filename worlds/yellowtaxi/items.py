from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import YellowTaxiWorld

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
    "Gear": 1,
    "Bunny (Morio's Lab)": 2_00,
    "Bunny (Bombeach)": 2_01,
    "Bunny (Pizza Time)": 2_02,
    "Bunny (Morio's Home)": 2_03,
    "Bunny (Arcade Panik)": 2_04,
    "Bunny (Tosla's Offices)": 2_05,
    "Bunny (Gym Gears)": 2_06,
    "Bunny (Fecal Matters)": 2_07,
    "Bunny (Flushed Away)": 2_08,
    "Bunny (Maurizio's City)": 2_09,
    "Bunny (Crash Test Industries)": 2_10,
    # "Bunny (Demo)": 2_11,
    "Bunny (Morio's Mind)": 2_12,
    "Bunny (Ruined Observatory)": 2_13,
    "Bunny (Tosla HQ)": 2_14,
    "Bunny (Moon)": 2_15,
    "1 Coin": 3,
    "10 Coins": 4,
    "25 Coins": 5,
    "100 Coins": 6,
    # Hats reserve 7_00
    "Flip-O-Will": 8_0_0,
    "Progressive Jump": 8_0_1,
    "Progressive Boost": 8_0_2,
    "Spin Attack": 8_0_3,
    "Glide": 8_0_4,
    "Golden Spring Unlock": 8_1_0,
    "Golden Propeller Unlock": 8_2_0,
    "Gela-Toni": 9_01,
    "Pizza King": 9_02,
    "Doggo": 9_07,
    "Orange Switch": 9_10,
    "Full Game Unlock": 9_11,
    "Morio's Password": 9_12,
    "Mosk's Rocket": 9_16,
    "Psycho Taxi Cartridge": 20_01,
    "Michele": 20_02,
    # Traps
    #"Wishlist Trap": 999_001,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    "Gear": ItemClassification.progression_deprioritized_skip_balancing,
    "Bunny (Morio's Lab)": ItemClassification.filler,
    "Bunny (Bombeach)": ItemClassification.filler,
    "Bunny (Pizza Time)": ItemClassification.filler,
    "Bunny (Morio's Home)": ItemClassification.filler,
    "Bunny (Arcade Panik)": ItemClassification.filler,
    "Bunny (Tosla's Offices)": ItemClassification.filler,
    "Bunny (Gym Gears)": ItemClassification.filler,
    "Bunny (Fecal Matters)": ItemClassification.filler,
    "Bunny (Flushed Away)": ItemClassification.filler,
    "Bunny (Maurizio's City)": ItemClassification.filler,
    "Bunny (Crash Test Industries)": ItemClassification.filler,
    # "Bunny (Demo)": ItemClassification.filler,
    "Bunny (Morio's Mind)": ItemClassification.filler,
    "Bunny (Ruined Observatory)": ItemClassification.filler,
    "Bunny (Tosla HQ)": ItemClassification.filler,
    "Bunny (Moon)": ItemClassification.filler,
    "1 Coin": ItemClassification.filler,
    "25 Coins": ItemClassification.filler,
    "50 Coins": ItemClassification.filler,
    "100 Coins": ItemClassification.filler,
    # Hats reserve 7_00
    "Flip-O-Will": ItemClassification.progression | ItemClassification.useful,
    "Progressive Jump": ItemClassification.progression | ItemClassification.useful,
    "Progressive Boost": ItemClassification.progression | ItemClassification.useful,
    "Spin Attack": ItemClassification.progression | ItemClassification.useful,
    "Glide": ItemClassification.useful,
    "Golden Spring Unlock": ItemClassification.progression | ItemClassification.useful,
    "Golden Propeller Unlock": ItemClassification.progression | ItemClassification.useful,
    "Gela-Toni": ItemClassification.progression,
    "Pizza King": ItemClassification.progression,
    "Doggo": ItemClassification.progression,
    "Orange Switch": ItemClassification.progression,
    "Morio's Password": ItemClassification.progression,
    "Mosk's Rocket": ItemClassification.progression,
    "Full Game Unlock": ItemClassification.progression,
    "Psycho Taxi Cartridge": ItemClassification.useful,
    "Michele": ItemClassification.useful,
}


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class YellowTaxiItem(Item):
    game = "Yellow Taxi Goes Vroom"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: YellowTaxiWorld) -> str:
    # TODO: ADD TRAPS
    #if world.random.randint(0, 99) < world.options.trap_chance:

    # TODO: Add weights for different coin quantities
    return "1 Coin"


def create_item_with_correct_classification(world: YellowTaxiWorld, name: str) -> YellowTaxiItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # Rat is progression if Cheesesanity is on
    if name == "Michele" and world.options.cheesesanity:
        classification = ItemClassification.progression

    # Bunnies are progresssion if Mosk's Rocket is shuffled or exclude post-goal locations is off
    if name.startswith("Bunny (") and world.options.shuffle_rocket:
        classification = ItemClassification.progression_deprioritized_skip_balancing

    return YellowTaxiItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: YellowTaxiWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = [world.create_item("Gear") for _ in range(world.num_gears)]

    # Add Bunnies to the pool TODO: Don't add post-goal bunnies for earlier goals
    if world.options.bunnysanity:
        hub_bunnies = 3
        if world.options.extra_demo_collectables:
            hub_bunnies += 2
        if not world.options.shuffle_golden_spring and not world.options.shuffle_orange_switch:
            hub_bunnies -= 2
        elif not world.options.shuffle_morios_password:
            hub_bunnies -= 1
        itempool += [world.create_item("Bunny (Morio's Lab)") for _ in range(hub_bunnies)]
        itempool += [world.create_item("Bunny (Bombeach)") for _ in range(3)]
        itempool += [world.create_item("Bunny (Gym Gears)") for _ in range(3)]
        # itempool += [world.create_item("Bunny (Demo)") for _ in range(3)]
        if world.options.goal > 1 or world.options.shuffle_orange_switch:
            itempool += [world.create_item("Bunny (Flushed Away)") for _ in range(3)]
        if (world.options.goal > 1 or world.options.shuffle_golden_spring or
                world.options.shuffle_orange_switch or world.options.shuffle_doggo):
            itempool += [world.create_item("Bunny (Fecal Matters)") for _ in range(3)]
        if world.options.goal > 0:
            itempool += [world.create_item("Bunny (Pizza Time)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Morio's Home)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Arcade Panik)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Tosla's Offices)") for _ in range(3)]
        if world.options.goal > 1:
            itempool += [world.create_item("Bunny (Maurizio's City)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Crash Test Industries)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Morio's Mind)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Ruined Observatory)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Tosla HQ)") for _ in range(3)]
            itempool += [world.create_item("Bunny (Moon)") for _ in range(3)]

    if world.options.shuffle_gela_toni:
        itempool.append(world.create_item("Gela-Toni"))

    if world.options.shuffle_pizza_king:
        itempool.append(world.create_item("Pizza King"))

    # TODO: Figure out how to handle Doggo for earlier goals
    if world.options.shuffle_doggo:
        itempool.append(world.create_item("Doggo"))

    if world.options.shuffle_morios_password:
        itempool.append(world.create_item("Morio's Password"))

    if world.options.shuffle_rocket:
        itempool.append(world.create_item("Mosk's Rocket"))

    if world.options.shuffle_flip_o_will != 0:
        itempool += [world.create_item("Progressive Boost") for _ in range(2)]
        itempool += [world.create_item("Progressive Jump") for _ in range(2)]
        itempool.append(world.create_item("Spin Attack"))

    if world.options.shuffle_glide:
        itempool.append(world.create_item("Glide"))

    if world.options.shuffle_golden_spring:
        itempool.append(world.create_item("Golden Spring Unlock"))

    if world.options.shuffle_golden_propeller:
        itempool.append(world.create_item("Golden Propeller Unlock"))

    if world.options.shuffle_orange_switch:
        itempool.append(world.create_item("Orange Switch"))

    if world.options.shuffle_full_game:
        itempool.append(world.create_item("Full Game Unlock"))

    if world.options.shuffle_rat:
        itempool.append(world.create_item("Michele"))

    #if world.options.shuffle_psycho_taxi:
    #    itempool.append(world.create_item("Psycho Taxi Cartridge"))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    # Sometimes, you might want the player to start with certain items already in their inventory.
    # These items are called "precollected items".
    # They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
    # Players can add precollected items themselves via the generic "start_inventory" option.
    # If you want to add your own precollected items, you can do so via world.push_precollected().
    #if world.options.start_with_one_confetti_cannon:
        # We're adding a filler item, but you can also add progression items to the player's precollected inventory.
        #starting_confetti_cannon = world.create_item("Confetti Cannon")
        #world.push_precollected(starting_confetti_cannon)
