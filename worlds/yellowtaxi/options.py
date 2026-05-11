from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, DeathLink, FreeText


# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


class Goal(Choice):
    """
    Which boss is your victory condition.

    Currently only Bomboss is supported.
    """
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
    Percentage of Gear items needed to access the goal portal.
    """
    display_name = "Goal Portal Gear Percentage"
    range_start = 50
    range_end = 90
    default = 75

class ExcludeGoalPortalChecks(DefaultOnToggle):
    """
    If true, removes items from within the goal portal from the pool.

    Note that if false, Goal Portal Gear Percentage may be capped at a lower value to prevent generation failures.
    """

    display_name = "Exclude Goal Portal Checks"

class ExpertLevel(Range):
    """
    Difficulty level for expected checks. Higher level means more difficult checks will get in logic earlier.
    """
    display_name = "Expert Level"
    range_start = 0
    range_end = 3
    default = 0

class ExtraDemoCollectables(Toggle):
    """
    Adds demo-exclusive locations. Adds 5 additional gears and 2 additional bunnies.
    The corresponding Rocket level will require all 5 Morio's Lab Bunnies to access when active.
    """

    display_name = "Add Extra Demo Collectables"

class TimeTrialGears(Toggle):
    """
    Adds each individual gear in Time Trials as a location, and adds the corresponding amount of gears to the pool.
    """

    display_name = "Add Time Trial Gears"

class OpenGrannysIsland(Toggle):
    """
    Opens up Granny's Island so that the main part of the island is available moveless.
    """
    display_name = "Open Granny's Island"

class LockedMoriosLab(Toggle):
    """
    Locks Morio's Lab and adds a "Lab Key" item into the multiworld. Adds a check for talking to Morio in Morio's Room.

    If "Open Granny's Island" is on, you will start outside the locked lab, and if it's off you will start inside the locked lab.
    """
    display_name = "Locked Morio's Lab"

class LockedMoriosWardrobe(Toggle):
    """
    Locks Morio's Wardrobe and adds a "Morio's Wardrobe" item into the multiworld. Adds a check for talking to the Mori-O-Tron in Morio's Wardrobe.

    If "Hatsanity" is not disabled, you will require logical access to the wardrobe in order to use hats.
    """
    display_name = "Locked Morio's Wardrobe"

class HatWorldMembership(Toggle):
    """
    Adds a "Hat World Membership" item needed to purchase any hats from Hat World
    """
    display_name = "Hat World Membership"

class GymGearsUnlockCondition(Choice):
    """
    How Gym Gears is unlocked.

    Open: Gym Gears entrance is always available in Granny's Island.
    Full Game: Gym Gears entrance will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Gym Membership: Gym Gears entrance will be unlocked after receiving "Gym Membership" from the multiworld. Adds a purchasable check from the Ultra Chad in Gym Gears.
    Exclude: Gym Gears entrance is always closed and Gym Gears will not be accessible
    """
    display_name = "Gym Gears Unlock Condition"

    option_open = 0
    option_full_game = 1
    option_shuffle_gym_membership = 2
    option_exclude = 3

    default = option_open
    alias_vanilla = option_open
    alias_unlocked = option_open

class FecalMattersUnlockCondition(Choice):
    """
    How Fecal Matters is unlocked.

    Vanilla: Talk to Doggo in Morio's Lab to unlock the house in Granny's Island.
    Open: The house in Granny's Island is always open.
    Full Game: The house in Granny's Island will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Doggo: The house in Granny's Island will be unlocked after receiving "Doggo" from the multiworld. Adds a check for talking to Doggo in Morio's Lab.
    Exclude: The house in Granny's Island is always closed and Fecal Matters will not be accessible
    """
    display_name = "Fecal Matters Unlock Condition"

    option_vanilla = -1
    option_open = 0
    option_full_game = 1
    option_shuffle_doggo = 2
    option_exclude = 3

    default = option_vanilla
    alias_unlocked = option_open

class FlushedAwayUnlockCondition(Choice):
    """
    How Flushed Away is unlocked.
    If set to anything other than "Default" or "Exclude", an NPC will be added who will take you to the Sewer Island if you have no possible logical path to it.

    Default: Same as Full Game if there is logical access to the Sewer Island, Exclude if there isn't.
    Open: The Sewer Entrance in Granny's Island is always open.
    Full Game: The Sewer Entrance in Granny's Island will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Sewer Key: The house in Granny's Island will be unlocked after receiving "Sewer Key" from the multiworld. Adds a check for talking to Michele in Flushed Away.
    Exclude: The Sewer Entrance in Granny's Island is always closed and Flushed Away will not be accessible
    """
    display_name = "Flushed Away Unlock Condition"

    option_default = -1
    option_open = 0
    option_full_game = 1
    option_shuffle_sewer_key = 2
    option_exclude = 3

    default = option_default
    alias_vanilla = option_default
    alias_unlocked = option_open

class LockedTimeTrials(Choice):
    """
    Whether Time Trials are locked behind an item. If set to anything but Open, will add locations for completing each Time Trial.

    Open: Time Trials TVs can always be accessed
    Single Item: Adds a "Time Trial Remote" item that is needed to access Time Trial TVs
    Split Items: Adds three specific Time Trial Remote items, each corresponding to an individual Time Trial.
    Progressive Items: Adds three "Progressive Time Trial Remote" items, each one allowing access to the next sequential Time Trial.
    """
    display_name = "Locked Time Trials"

    option_open = 0
    option_single_item = 1
    option_split_items = 2
    option_progressive_items = 3

    default = option_open
    alias_vanilla = option_open
    alias_unlocked = option_open
    alias_disabled = option_open
    alias_off = option_open
    alias_enabled = option_single_item
    alias_on = option_single_item

class ShuffleGelaToni(DefaultOnToggle):
    """
    Adds the unlock for the Ice Cream Truck Entrance in Granny's Island into the item pool and adds a location for defeating Bomboss in Bombeach.
    """

    display_name = "Shuffle Gela-Toni"

class ShufflePizzaKing(Toggle):
    """
    Adds the unlock for the Pizza Oven Entrance in Granny's Island into the item pool and adds a location for completing Pizza King's quest in Pizza Time.

    If Bomboss is the goal, the location check for Pizza King will instead be obtained by talking to him in Granny's Island.
    """

    display_name = "Shuffle Pizza King"

class ShuffleOrangeSwitch(DefaultOnToggle):
    """
    Adds the Orange Switch into the item pool and adds a location for pressing the Orange Switch in Crash Test Industries.

    If goal is Bomboss or Tosla HQ, a PICI in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Orange Switch"

class ShuffleMoriosPassword(Toggle):
    """
    Adds Morio's Password into the item pool and adds a location for obtaining the key in Morio's Mind.

    If goal is Bomboss or Tosla HQ, talking to Morio in the Dream Machine in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Morio's Password"

class ShuffleRocket(Toggle):
    """
    Adds the unlock for Mosk's Rocket to appear in Granny's Island into the item pool and adds a location for defeating the final boss on the Moon.

    If goal is Bomboss or Tosla HQ, talking to Alien Mosk in Granny's Island will be the location instead.
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

class DemoPortalMode(Choice):
    """
    When the game is in the Demo state, which portals should appear. Has no effect if Shuffle Full Game is off.

    Basic: Matches current Steam demo, only containing the Morio's Home and Bombeach portals.
    Next Fest: Matches the Next Fest demo, which includes the Arcade Panik portal and the above.
    Influencers: Matches the demo given to certain influencers, containing the Pizza Time portal and all of the above.
    Open: Portals will not be removed while in demo mode and will solely require gears to unlock.
    """

    display_name = "Demo Portal Mode"

    option_basic = 1
    option_next_fest = 2
    option_influencers = 3
    option_open = 0

    default = option_basic
    alias_vanilla = option_basic
    alias_default = option_basic
    alias_extra = option_next_fest
    alias_extra_influencers = option_influencers

class ShufflePsychoTaxi(Toggle):
    """
    Adds the Psycho Taxi Cartridge into the item pool and adds a location for picking up the Cartridge in Arcade Panik.

    If goal is Bomboss, talking to the Psycho Taxi Arcade Machine will be the location instead.
    """

    display_name = "Shuffle Psycho Taxi"

class ShuffleRat(Toggle):
    """
    Adds Michele the Rat into the item pool and adds a location for talking to Michele in Pizza Time.

    If goal is Bomboss, Michele will instead be found in Granny's Island.
    """

    display_name = "Shuffle Michele the Rat"

class Bunnysanity(Toggle):
    """
    Adds Golden Bunnies as checks and locations. These bunnies are filler unless Mosk's Rocket is shuffled.
    """

    display_name = "Bunnysanity"

class Hatsanity(Choice):
    """
    Shuffles Hats into the pool.

    Hatsanity makes one check per purchasable hat.
    Shopsanity makes any individual place a hat can be purchased into a check, including duplicates and "no hat" locations.
    In Shopsanity, extra hats will be added to the pool to compensate for the extra hat slots, regardless of the "Hatsanity Filler Hats" setting
    """
    display_name = "Hatsanity"

    option_disabled = 0
    option_hatsanity = 1
    option_shopsanity = 2

    alias_off = 0

class HatsanityFillerHats(DefaultOnToggle):
    """
    If Hatsanity is not set to disabled, add as many not-available hats as possible to the filler pool before doing random fill.
    """
    display_name = "Hatsanity Filler Hats"

class Checkpointsanity(Toggle):
    """
    Adds checkpoints as location checks.
    """

    display_name = "Checkpointsanity"

class Safesanity(Toggle):
    """
    Adds freestanding safes as location checks.
    """

    display_name = "Safesanity"

class Chestsanity(Toggle):
    """
    Adds freestanding chests as location checks.
    """

    display_name = "Chestsanity"

class Coinbagsanity(Toggle):
    """
    Adds freestanding coin bags as location checks.
    """

    display_name = "Coinbagsanity"

class Coinsanity(Toggle):
    """
    Adds freestanding individual coins as location checks.
    """

    display_name = "Coinsanity"

class CoinsanityPercent(Range):
    """
    What percentage of individual coins will be made into location checks if Coinsanity is enabled.

    In a multiworld, the following restrictions are in place:
    If the value is higher than the "multiworld_coinsanity_percentage_cap" in the host.yaml, it will be lowered to that value.
    If the value is higher than the "multiworld_coinsanity_percentage_non_filler_cap" in the host.yaml, any coin checks past that threshold will be forced excluded.
    """
    display_name = "Coinsanity Percent"
    range_start = 1
    range_end = 100
    default = 10

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
    default = option_on
    alias_none = option_off
    alias_progressive_split = option_on # TODO: Swap alias with main option if adding more options

class ShuffleGlide(Toggle):
    """
    Shuffles the ability to stall in midair by tapping the gas button into the item pool and adds a new location for talking to a PICI in Morio's Lab.

    This item is not logically required for any locations at this time, and as such will be considered "useful"
    """

    display_name = "Shuffle Glide"

class EarlyMove(Toggle):
    """
    If Flip O' Will Shuffle is enabled, forces either a Progressive Boost or Progressive Jump to the first local few checks.

    Prevents an early BK as only 3 gears are accessible moveless.
    """

    display_name = "Early Move"

class ShuffleGoldenSpring(DefaultOnToggle):
    """
    Shuffles the Golden Spring into the item pool and adds a new location for defeating the Tosla HQ boss.

    If goal is Bomboss, talking to Morio outside of the Tosla HQ Portal will be the location instead.
    """
    display_name = "Shuffle Golden Spring"

class ShuffleGoldenPropeller(DefaultOnToggle):
    """
    Shuffles the Golden Propeller into the item pool and adds a new location for talking to Morio in Ruined Observatory.

    If goal is Bomboss or Tosla HQ, talking to Nick-O-Will near the top of Granny's Island will be the location instead.
    """
    display_name = "Shuffle Golden Propeller"

class FunnyFaces(FreeText):
    """
    In your installation folder for Yellow Taxi Goes Vroom, there exists an "Extras" folder containing a "FunnyFaces" subfolder.

    Setting this option will load an image from this folder for both the TV Hat and coins, if available.
    If this is set to anything other than a blank string, you will start with the TV Hat.
    If Hatsanity is set to Shopsanity, a "No Hat" item will replace the TV Hat in the pool, and hats cannot be fully unequipped unless this is found.
    """
    display_name = "Funny Faces"
    default = ""

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class YellowTaxiOptions(PerGameCommonOptions):
    goal: Goal
    goal_portal_gear_percentage: GoalPortalGearPercentage
    exclude_goal_portal_checks : ExcludeGoalPortalChecks
    expert_level: ExpertLevel
    death_link: DeathLink
    open_grannys_island: OpenGrannysIsland
    locked_morios_lab: LockedMoriosLab
    locked_morios_wardrobe: LockedMoriosWardrobe
    locked_time_trials: LockedTimeTrials
    gym_gears_unlock_condition: GymGearsUnlockCondition
    fecal_matters_unlock_condition: FecalMattersUnlockCondition
    flushed_away_unlock_condition: FlushedAwayUnlockCondition
    shuffle_gela_toni: ShuffleGelaToni
    shuffle_pizza_king: ShufflePizzaKing
    shuffle_orange_switch: ShuffleOrangeSwitch
    shuffle_morios_password: ShuffleMoriosPassword
    shuffle_rocket: ShuffleRocket
    shuffle_full_game: ShuffleFullGame
    demo_portal_mode: DemoPortalMode
    shuffle_psycho_taxi: ShufflePsychoTaxi
    shuffle_rat: ShuffleRat
    bunnysanity: Bunnysanity
    hatsanity: Hatsanity
    hatsanity_filler_hats: HatsanityFillerHats
    checkpointsanity: Checkpointsanity
    safesanity: Safesanity
    chestsanity: Chestsanity
    coinbagsanity: Coinbagsanity
    coinsanity: Coinsanity
    coinsanity_percent: CoinsanityPercent
    cheesesanity: Cheesesanity
    shuffle_flip_o_will: ShuffleFlipOWill
    shuffle_glide: ShuffleGlide
    early_move: EarlyMove
    shuffle_golden_spring: ShuffleGoldenSpring
    shuffle_golden_propeller: ShuffleGoldenPropeller
    extra_demo_collectables: ExtraDemoCollectables
    time_trial_gears: TimeTrialGears
    funny_faces: FunnyFaces

# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Location Options",
        [
            ExtraDemoCollectables,
            TimeTrialGears,
            Bunnysanity,
            Hatsanity,
            HatsanityFillerHats,
            Checkpointsanity,
            Safesanity,
            Chestsanity,
            Coinbagsanity,
            Coinsanity,
            CoinsanityPercent,
            Cheesesanity
        ],
    ),
    OptionGroup(
        "World Options",
        [
            OpenGrannysIsland,
            LockedMoriosLab,
            LockedMoriosWardrobe,
            LockedTimeTrials,
            GymGearsUnlockCondition,
            FecalMattersUnlockCondition,
            FlushedAwayUnlockCondition,
            ShuffleGelaToni,
            ShufflePizzaKing,
            ShuffleOrangeSwitch,
            ShuffleMoriosPassword,
            ShuffleRocket,
            ShuffleFullGame,
            DemoPortalMode,
            ShufflePsychoTaxi,
            ShuffleRat,
        ],
    ),
    OptionGroup(
        "Ability Randomizer Options",
        [
            ShuffleFlipOWill,
            ShuffleGlide,
            EarlyMove,
            ShuffleGoldenSpring,
            ShuffleGoldenPropeller
        ],
    ),
    OptionGroup(
        "Cosmetic Options",
        [
            FunnyFaces
        ],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    # TODO: Make option presets
}
