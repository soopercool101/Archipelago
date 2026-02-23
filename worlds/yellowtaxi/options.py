from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, DeathLink


# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


class Goal(Choice):
    display_name = "Goal"

    option_bombeach_boss = 0
    #option_tosla_offices_boss = 1
    #option_moon_boss = 2
    #option_backrooms = 3
    #option_macguffin = 4

    default = option_bombeach_boss
    #alias_final_boss = option_moon_boss

class GoalPortalGearPercentage(Range):
    """
    Percentage of Gear items needed to access the portal
    """
    display_name = "Goal Portal Gear Percentage"
    range_start = 20
    range_end = 90
    default = 75



class ExcludeGoalPortalChecks(DefaultOnToggle):
    """
    If true, removes items from within the goal portal from the pool.

    Note that if false, Goal Portal Gear Percentage may be capped at a lower value.
    """

    display_name = "Exclude Goal Portal Checks"

class ExpertLevel(Range):
    """
    Difficulty level for expected checks. Higher level means more difficult checks will get in logic earlier.
    """
    display_name = "Expert Level"
    range_start = 0
    range_end = 2
    default = 0

class ExtraDemoCollectables(Toggle):
    """
    Adds demo-exclusive locations. Adds 5 additional gears and 2 additional bunnies.
    The corresponding Rocket level will require all 5 Morio's Lab Bunnies to access when active.
    """

    display_name = "Add Extra Demo Collectables"

class ShuffleGelaToni(DefaultOnToggle):
    """
    Adds the unlock for the Ice Cream Truck Entrance in Granny's Island into the item pool and adds a location for defeating BomBoss in Bombeach.
    """

    display_name = "Shuffle Gela-Toni"

class ShufflePizzaKing(DefaultOnToggle):
    """
    Adds the unlock for the Pizza Oven Entrance in Granny's Island into the item pool and adds a location for completing Pizza King's quest in Pizza Time.

    If BomBoss is the goal, the location check for Pizza King will instead be obtained by talking to him in Granny's Island.
    """

    display_name = "Shuffle Pizza King"

class ShuffleDoggo(DefaultOnToggle):
    """
    Adds the unlock for Fecal Matters' Entrance in Granny's Island into the item pool and adds a location for talking to Doggo in Morio's Lab.

    Depending on settings, Doggo may instead be found in Granny's Island, if you would not be able to reach him in Morio's Lab
    """

    display_name = "Shuffle Doggo"

class ShuffleOrangeSwitch(DefaultOnToggle):
    """
    Adds the Orange Switch into the item pool and adds a location for pressing the Orange Switch in Crash Test Industries.

    If goal is BomBoss or Tosla HQ, a PICI in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Orange Switch"

class ShuffleMoriosPassword(DefaultOnToggle):
    """
    Adds Morio's Password into the item pool and adds a location for obtaining the key in Morio's Mind.

    If goal is BomBoss or Tosla HQ, talking to Morio in the Dream Machine in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Morio's Password"

class ShuffleRocket(Toggle):
    """
    Adds the unlock for Mosk's Rocket to appear in Granny's Island into the item pool and adds a location for defeating the final boss on the Moon.

    If goal is BomBoss or Tosla HQ, talking to Alien Mosk in Granny's Island will be the location instead.
    """

    display_name = "Shuffle Mosk's Rocket"

class ShuffleFullGame(Toggle):
    """
    Starts the game in "Demo" mode, locking areas of the hub until a "Full Game Unlock" item is received.
    Adds a location for hitting the true demo wall in the hub.
    If the Full Game Unlock item is received, passing through where the wall used to be will send the check.

    The mod does not work in the actual demo, you are still required to purchase the full game to play!
    """

    display_name = "Shuffle Full Game Unlock"

class ShufflePsychoTaxi(Toggle):
    """
    Adds the Psycho Taxi Cartridge into the item pool and adds a location for picking up the Cartridge in Arcade Panik.

    If goal is BomBoss, talking to the Psycho Taxi Arcade Machine will be the location instead.
    """

    display_name = "Shuffle Psycho Taxi"

class ShuffleRat(Toggle):
    """
    Adds Michele the Rat into the item pool and adds a location for talking to Michele in Pizza Time.

    If goal is BomBoss, Michele will instead be found somewhere in Granny's Island, depending on settings.
    """

    display_name = "Shuffle Michele the Rat"

class Bunnysanity(Toggle):
    """
    Adds Golden Bunnies as checks and locations. These bunnies are filler unless Mosk's Rocket is shuffled.
    """

    display_name = "Bunnysanity"

class Checkpointsanity(Toggle):
    """
    Adds checkpoints as location checks.
    """

    display_name = "Checkpointsanity"

class Safesanity(Toggle):
    """
    Adds safes as location checks.
    """

    display_name = "Safesanity"

class Chestsanity(Toggle):
    """
    Adds chests as location checks.
    """

    display_name = "Chestsanity"

class Coinbagsanity(Toggle):
    """
    Adds coin bags as location checks.

    Not recommended for most multiworlds! Adds a lot of filler.
    """

    display_name = "Coinbagsanity"

class Coinsanity(Toggle):
    """
    Adds coins as location checks.

    Not recommended for most multiworlds! Adds a lot of filler.
    """

    display_name = "Coinsanity"

class Cheesesanity(Toggle):
    """
    Adds cheeses as location checks.
    """

    display_name = "Cheesesanity"

class ShuffleFlipOWill(Choice):
    """
    Shuffles the Flip O' Will into the item pool as 2 Progressive Boosts, 2 Progressive Jumps, and 1 Spin Attack.
    Adds 5 corresponding locations by talking to NPCs, 4 PICIs in Morio's Lab and Morio in Morio's Island.
    """

    display_name = "Flip O' Will Shuffle"

    option_off = 0
    #option_shuffle = 1
    #option_split = 2
    option_on = 3
    default = option_off
    alias_none = option_off
    alias_progressive_split = option_on # TODO: Swap alias with main option if adding more options

class ShuffleGlide(Toggle):
    """
    Shuffles the ability to stall in midair by tapping the gas button into the item pool and adds a new location for talking to a PICI in Morio's Lab.

    This item is not logically required for any locations at this time, and as such will be considered "useful"
    """

    display_name = "Shuffle Glide"

class ShuffleGoldenSpring(DefaultOnToggle):
    """
    Shuffles the Golden Spring into the item pool and adds a new location for defeating the Tosla HQ boss.

    If goal is BomBoss, talking to Morio outside of the Tosla HQ Portal will be the location instead.
    """
    display_name = "Shuffle Golden Spring"

class ShuffleGoldenPropeller(DefaultOnToggle):
    """
    Shuffles the Golden Propeller into the item pool and adds a new location for talking to Morio in Ruined Observatory.

    If goal is BomBoss or Tosla HQ, talking to Nick-O-Will near the top of Granny's Island will be the location instead.
    """
    display_name = "Shuffle Golden Propeller"

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class YellowTaxiOptions(PerGameCommonOptions):
    goal: Goal
    goal_portal_gear_percentage: GoalPortalGearPercentage
    exclude_goal_portal_checks : ExcludeGoalPortalChecks
    expert_level: ExpertLevel
    death_link: DeathLink
    shuffle_gela_toni: ShuffleGelaToni
    shuffle_pizza_king: ShufflePizzaKing
    shuffle_doggo: ShuffleDoggo
    shuffle_orange_switch: ShuffleOrangeSwitch
    shuffle_morios_password: ShuffleMoriosPassword
    shuffle_rocket: ShuffleRocket
    shuffle_full_game: ShuffleFullGame
    shuffle_psycho_taxi: ShufflePsychoTaxi
    shuffle_rat: ShuffleRat
    bunnysanity: Bunnysanity
    checkpointsanity: Checkpointsanity
    safesanity: Safesanity
    chestsanity: Chestsanity
    coinbagsanity: Coinbagsanity
    coinsanity: Coinsanity
    cheesesanity: Cheesesanity
    shuffle_flip_o_will: ShuffleFlipOWill
    shuffle_glide: ShuffleGlide
    shuffle_golden_spring: ShuffleGoldenSpring
    shuffle_golden_propeller: ShuffleGoldenPropeller
    extra_demo_collectables: ExtraDemoCollectables

# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Location Options",
        [ExtraDemoCollectables, Bunnysanity, Checkpointsanity, Safesanity, Chestsanity, Coinbagsanity, Coinsanity, Cheesesanity],
    ),
    OptionGroup(
        "World Options",
        [ShuffleGelaToni, ShufflePizzaKing, ShuffleDoggo, ShuffleOrangeSwitch, ShuffleMoriosPassword, ShuffleRocket, ShuffleFullGame, ShufflePsychoTaxi, ShuffleRat],
    ),
    OptionGroup(
        "Ability Randomizer Options",
        [ShuffleFlipOWill, ShuffleGlide, ShuffleGoldenSpring, ShuffleGoldenPropeller],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    # TODO: Make option presets
}
