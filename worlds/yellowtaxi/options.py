from dataclasses import dataclass

from Options import (Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, DeathLink, FreeText,
                     StartInventoryPool)


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
    """
    display_name = "Goal"

    option_bombeach_boss = 0
    option_tosla_offices_boss = 1
    #option_moon_boss = 2
    #option_backrooms = 3
    #option_macguffin = 4

    default = option_tosla_offices_boss
    #alias_final_boss = option_moon_boss

class GoalPortalGearPercentage(Range):
    """
    Percentage of Gear items needed to access the goal portal.
    """
    display_name = "Goal Portal Gear Percentage"
    range_start = 40
    range_end = 90
    default = 60

class RemoveGoalPortalLocations(Toggle):
    """
    If true, removes locations from within the goal portal from the pool.
    """

    display_name = "Remove Goal Portal Locations"

class RemovePostGoalPortals(Toggle):
    """
    If true, removes portals that are after your current goal portal.

    Note that the game does not currently support any portals after Tosla's Offices, so these will always be removed.
    """

    display_name = "Remove Post-Goal Portals"

class ExpertLevel(Range):
    """
    Difficulty level for location access. Higher level means more difficult locations will get in logic earlier.

    Universal Tracker will by default display 1 expert level above your own as "glitched logic".
    You can increase the level shown by using "/manually_collect Additional Expert Logic Level".
    """
    display_name = "Expert Level"
    range_start = 0
    range_end = 3
    default = 0

class ExtraDemoCollectables(Toggle):
    """
    Adds demo-exclusive locations. Adds 5 additional gears and 2 additional bunnies.
    The corresponding Rocket level will require all available Morio's Lab Bunnies.
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
    Locks Morio's Lab and adds a "Lab Key" item into the multiworld. Adds a location for talking to Morio in Morio's Room.

    If "Open Granny's Island" is on, you will start outside the locked lab, and if it's off you will start inside the locked lab.
    """
    display_name = "Locked Morio's Lab"

class LockedMoriosWardrobe(Toggle):
    """
    Locks Morio's Wardrobe and adds a "Morio's Wardrobe" item into the multiworld.
    Adds a location for talking to the Mori-O-Tron in Morio's Wardrobe.

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
    Shuffle Gym Membership: Gym Gears entrance will be unlocked after receiving "Gym Membership" from the multiworld. Adds a purchasable location from the Ultra Chad in Gym Gears.
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
    Shuffle Doggo: The house in Granny's Island will be unlocked after receiving "Doggo" from the multiworld. Adds a location for talking to Doggo in Morio's Lab.
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
    Shuffle Sewer Key: The house in Granny's Island will be unlocked after receiving "Sewer Key" from the multiworld. Adds a location for talking to Michele in Flushed Away.
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

    If goal is Bomboss and Remove Goal Portal locations is enabled, the location will instead be talking to him in Granny's Island.
    """

    display_name = "Shuffle Gela-Toni"

class ShufflePizzaKing(DefaultOnToggle):
    """
    Adds the unlock for the Pizza Oven Entrance in Granny's Island into the item pool and adds a location for completing Pizza King's quest in Pizza Time.

    If Pizza Time is not an included level, the location will instead be talking to him in Granny's Island.
    """

    display_name = "Shuffle Pizza King"

class ShuffleOrangeSwitch(DefaultOnToggle):
    """
    Adds the Orange Switch into the item pool and adds a location for pressing the Orange Switch in Crash Test Industries.

    If Crash Test Industries is not an included level, talking to Ocra Taxi at the end of Crash again will be the location instead.
    """

    display_name = "Shuffle Orange Switch"

class ShuffleMoriosPassword(Toggle):
    """
    Adds Morio's Password into the item pool and adds a location for obtaining the key in Morio's Mind.

    If Morio's Mind is not an included level, talking to Morio in the Dream Machine in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Morio's Password"

class ShuffleRocket(Toggle):
    """
    Adds the unlock for Mosk's Rocket to appear in Granny's Island into the item pool and adds a location for defeating the final boss on the Moon.

    If the Moon is not an included level, or is the goal and Remove Goal Portal locations is enabled, talking to Alien Mosk in Granny's Island will be the location instead.
    """

    display_name = "Shuffle Mosk's Rocket"

class ShuffleFullGame(DefaultOnToggle):
    """
    Starts the game in "Demo" mode, locking areas of Morio's Lab until a "Full Game Unlock" item is received.
    Adds a location for hitting the true demo wall in Morio's Lab.
    If the Full Game Unlock item is received, passing through where the wall used to be will send the location.

    The mod does not work in the actual demo, you are still required to purchase the full game to play!
    """

    display_name = "Shuffle Full Game Unlock"

class DemoPortalMode(Choice):
    """
    When the game is in the Demo state, which portals should appear. Has no effect if Shuffle Full Game is off.

    Basic: Matches current Steam demo, only containing the first two portals.
    Next Fest: Matches the Next Fest demo, which includes the first three portals.
    Influencers: Matches the demo given to certain influencers, containing the first four portals.
    Open: Portals will not be removed while in demo mode and will solely require gears to unlock.
    """

    display_name = "Demo Portal Mode"

    option_basic = 2
    option_next_fest = 3
    option_influencers = 4
    option_open = -1

    default = option_basic
    alias_vanilla = option_basic
    alias_default = option_basic
    alias_extra = option_next_fest
    alias_extra_influencers = option_influencers

class ShufflePsychoTaxi(Toggle):
    """
    Adds the Psycho Taxi Cartridge into the item pool and adds a location for picking up the Cartridge in Arcade Panik.

    If Arcade Panik is not an included level, talking to the Psycho Taxi Arcade Machine will be the location instead.
    """

    display_name = "Shuffle Psycho Taxi"

class Bunnysanity(Toggle):
    """
    Adds Golden Bunnies as items and locations. These bunnies are filler items unless Mosk's Rocket is shuffled.
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
    Adds checkpoints as locations.
    """

    display_name = "Checkpointsanity"

class Safesanity(Toggle):
    """
    Adds freestanding safes as locations.
    """

    display_name = "Safesanity"

class Chestsanity(Toggle):
    """
    Adds freestanding chests as locations.
    """

    display_name = "Chestsanity"

class ChestsanityPercent(Range):
    """
    What percentage of individual chests will be made into locations if Chestsanity is enabled.
    """
    display_name = "Chestsanity Percent"
    range_start = 1
    range_end = 100
    default = 100

class Coinbagsanity(Toggle):
    """
    Adds freestanding coin bags as locations.
    """

    display_name = "Coinbagsanity"

class CoinbagsanityPercent(Range):
    """
    What percentage of individual coin bags will be made into locations if Coinbagsanity is enabled.
    """
    display_name = "Coinbagsanity Percent"
    range_start = 1
    range_end = 100
    default = 50

class Coinsanity(Toggle):
    """
    Adds freestanding individual coins as locations.
    """

    display_name = "Coinsanity"

class CoinsanityPercent(Range):
    """
    What percentage of individual coins will be made into locations if Coinsanity is enabled.

    In a multiworld, the following restriction is in place:
    If the value is higher than the "multiworld_coinsanity_percentage_cap" in the host.yaml (default: 100), it will be lowered to that value.
    """
    display_name = "Coinsanity Percent"
    range_start = 1
    range_end = 100
    default = 10

class CoinsanityNonFillerCap(Range):
    """
    What percentage of total available coins will be able to be anything other than filler items.

    If your Coinsanity Percent is set to 10 and this is set to 5, half of your rolled coin locations will be forced filler.
    If your Coinsanity Percent is lower than this number, all coins could potentially be progression.

    In a multiworld, the following restriction is in place:
    If the value is higher than the "multiworld_coinsanity_percentage_non_filler_cap" in the host.yaml (default: 5), it will be lowered to that value.
    """
    display_name = "Coinsanity Non-Filler Cap Percentage"
    range_start = 0
    range_end = 100
    default = 5

class Cheesesanity(Toggle):
    """
    Adds cheeses as locations.
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

    This item is currently only logically required in Expert Level 3. As such, it will be classified as "Useful" for lower difficulties.
    """

    display_name = "Shuffle Glide"

class EarlyMove(Toggle):
    """
    If Flip O' Will Shuffle is enabled, forces either a Progressive Boost or Progressive Jump to local sphere 0.

    Prevents an early BK depending on settings.
    """

    display_name = "Early Move"

class ShuffleGoldenSpring(DefaultOnToggle):
    """
    Shuffles the Golden Spring into the item pool and adds a new location for defeating the Tosla's Offices boss.

    If Tosla's Offices is not an included level, talking to Morio near the Tosla's Offices Portal will be the location instead.
    """
    display_name = "Shuffle Golden Spring"

class ShuffleGoldenPropeller(DefaultOnToggle):
    """
    Shuffles the Golden Propeller into the item pool and adds a new location for talking to Morio in Ruined Observatory.

    If Ruined Observatory is not an included level, talking to Nick-O-Will near the top of Granny's Island will be the location instead.
    """
    display_name = "Shuffle Golden Propeller"

class ShuffleRat(Toggle):
    """
    Adds Michele the Rat into the item pool and adds a location for talking to Michele in Pizza Time.

    If Pizza Time is not an included level, Michele will instead be found in Granny's Island.
    """

    display_name = "Shuffle Michele the Rat"

class PizzaWheels(Choice):
    """
    Shuffles Pizza Wheels into the item pool and adds a new location for talking to MacPizza in Pizza Time.
    If Pizza Time is not an included level, talking to Chef Pepe in Morio's Lab will be the location instead.

    Pizza Wheels have three modes, corresponding to different item classifications:
    Progression: The cheese on the pizza protects your tires from spikes, allowing you to drive across them safely.
    Useful: Pizza Wheels can only protect you from spikes after receiving the Golden Spring Blueprints. No logic implications.
    Filler: Pizza Wheels are purely cosmetic, and have no effect on gameplay.
    """
    display_name = "Pizza Wheels"

    option_off = 0
    option_progression = 3
    option_useful = 2
    option_filler = 1
    default = option_off
    alias_disabled = option_off

class FunnyFaces(FreeText):
    """
    In your installation folder for Yellow Taxi Goes Vroom, there exists an "Extras" folder containing a "FunnyFaces" subfolder.

    Setting this option will load an image from this folder for both the TV Hat and coins, if available.
    If this is set to anything other than a blank string, you will start with the TV Hat.
    If Hatsanity is set to Shopsanity, a "No Hat" item will replace the TV Hat in the pool, and hats cannot be fully unequipped unless this is found.
    """
    display_name = "Funny Faces"
    default = ""

class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink.
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 5
    default = 1

class RingLink(Toggle):
    """
    Whether your coin gain/loss is linked to other players.
    """
    display_name = "Ring Link"

class PurchaseRebatePercent(Range):
    """
    When you die, the coins you lose are added to a secret number that causes coin bags, chests, and safes to give more money until you are reimbursed.

    This setting allows any in-game purchases to also increment this number by a % of the cost, allowing you to more easily regain spent coins.
    Note that this value is saved per-session, restarting the game will result in it being reset to 0!
    """
    display_name = "Purchase Rebate %"
    range_start = 0
    range_end = 100
    default = 0

class EasyAlienMosk(Toggle):
    """
    When fighting Alien Mosk in Tosla's Offices, there are 4 different positions at which a Golden Spring will spawn.
    In all phases except the first, the fight will spawn one Golden Spring at the furthest position from the player.

    When this option is enabled, all four golden springs will spawn on all boss phases instead.
    """

    display_name = "Easy Alien Mosk"

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class YellowTaxiOptions(PerGameCommonOptions):
    goal: Goal
    goal_portal_gear_percentage: GoalPortalGearPercentage
    remove_goal_portal_locations : RemoveGoalPortalLocations
    remove_post_goal_portals : RemovePostGoalPortals
    expert_level: ExpertLevel
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    ring_link: RingLink
    purchase_rebate_percent: PurchaseRebatePercent
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
    chestsanity_percent: ChestsanityPercent
    coinbagsanity: Coinbagsanity
    coinbagsanity_percent: CoinbagsanityPercent
    coinsanity: Coinsanity
    coinsanity_percent: CoinsanityPercent
    coinsanity_non_filler_cap: CoinsanityNonFillerCap
    cheesesanity: Cheesesanity
    shuffle_flip_o_will: ShuffleFlipOWill
    shuffle_glide: ShuffleGlide
    early_move: EarlyMove
    shuffle_golden_spring: ShuffleGoldenSpring
    shuffle_golden_propeller: ShuffleGoldenPropeller
    pizza_wheels: PizzaWheels
    extra_demo_collectables: ExtraDemoCollectables
    time_trial_gears: TimeTrialGears
    funny_faces: FunnyFaces
    easy_alien_mosk: EasyAlienMosk
    start_inventory_from_pool: StartInventoryPool

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
            ChestsanityPercent,
            Coinbagsanity,
            CoinbagsanityPercent,
            Coinsanity,
            CoinsanityPercent,
            Cheesesanity,
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
        ],
    ),
    OptionGroup(
        "Ability Randomizer Options",
        [
            ShuffleFlipOWill,
            ShuffleGlide,
            EarlyMove,
            ShuffleGoldenSpring,
            ShuffleGoldenPropeller,
            PizzaWheels,
            ShuffleRat,
        ],
    ),
    OptionGroup(
        "Quality of Life Options",
        [
            PurchaseRebatePercent,
            EasyAlienMosk,
        ],
    ),
    OptionGroup(
        "Cosmetic Options",
        [
            FunnyFaces,
        ],
    ),
    OptionGroup(
        "Advanced Options",
        [
            CoinsanityNonFillerCap,
        ],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    # TODO: Make option presets
}
