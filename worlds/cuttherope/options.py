from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, DeathLink

class GoalBox(Range):
    """
    Which box will be your goal box? No boxes past the goal box will be included in the seed.
    """
    display_name = "Goal Box"
    range_start = 2
    range_end = 11
    default = 8

class GoalBoxStarRequirement(Range):
    """
    How many stars are required to open the goal box.
    Will be capped at 75 multiplied by the number of non-goal boxes.
    """
    display_name = "Goal Box Star Requirement"
    range_start = 10
    range_end = 750

    default = 100

class ExtraStars(Range):
    """
    How many extra star items will be added to the pool beyond those needed to goal?
    Will be capped if higher than the number of free locations.
    """
    display_name = "Extra Stars"
    range_start = 0
    range_end = 100
    default = 20

class BoxLockingMode(Choice):
    """
    How boxes are unlocked.

    Open World: Each non-goal box starts unlocked.
    Box Items: Specific items are needed to unlock a given non-goal box.
    Box Items With Skips: Same as above, but all levels are always accessible in an unlocked non-goal box.
    """
    display_name = "Box Locking Mode"
    option_open_world = 0
    option_box_items = 1
    option_box_items_with_skips = 2
    default = option_box_items

    alias_open = 0
    alias_items = 1
    alias_skips = 2

class RandomStartingBox(Toggle):
    """
    If enabled, you will start with a random box rather than Cardboard Box.
    Has no effect when Box Locking Mode is set to Open World.
    """
    display_name = "Random Starting Box"

class StarsanityMode(Choice):
    """
    How star locations work.

    Per-level count: When completing a level, up to 3 locations are sent based on the number of stars obtained.
    Individual: Grabbing a star will instantly send a corresponding location, without needing to beat the level.
    """
    display_name = "Starsanity Mode"
    #option_disabled = 0 # TODO: Figure out if this is even fun and worth implementing
    option_per_level_count = 1
    option_individual = 2
    default = 1

class ExpertLevel(Range):
    """
    Difficulty level for location access. Higher level means more difficult locations will get in logic earlier.

    Universal Tracker will by default display 1 expert level above your own as "glitched logic".
    You can increase the level shown by using "/manually_collect Additional Expert Logic Level".
    """
    display_name = "Expert Level"
    range_start = 0
    range_end = 2
    default = 0

class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink.
    Note that some levels will kill you instantly without items, it is highly recommended to have this higher than 1!
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 5

class TutorialsItem(Toggle):
    """
    Adds a filler item needed to make tutorial text appear.
    If disabled, tutorial text will always appear.
    """
    display_name = "Tutorials Item"

class DisableSpikesItem(DefaultOnToggle):
    """
    Adds an item that disables the collision for Spikes. Accounted for in logic.
    """
    display_name = "Disable Spikes Item"

class ProgressiveElectricSparks(DefaultOnToggle):
    """
    Adds a second Electric Sparks item. Having both fully disables electric sparks. Accounted for in logic.
    """
    display_name = "Progressive Electric Sparks"

class ProgressiveBlades(DefaultOnToggle):
    """
    Adds a second Blades item. Having both fully disables blades. Accounted for in logic.
    """
    display_name = "Progressive Blades"

class StarTimerDisableItem(DefaultOnToggle):
    """
    Adds an item that removes the timer for timed stars. Accounted for in logic.
    """
    display_name = "Star Timer Disable Item"

@dataclass
class CutTheRopeOptions(PerGameCommonOptions):
    goal_box: GoalBox
    goal_box_star_requirement: GoalBoxStarRequirement
    extra_stars: ExtraStars
    box_locking_mode: BoxLockingMode
    random_starting_box: RandomStartingBox
    starsanity_mode: StarsanityMode
    expert_level: ExpertLevel
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    tutorials_item: TutorialsItem
    disable_spikes_item: DisableSpikesItem
    progressive_electric_sparks: ProgressiveElectricSparks
    progressive_blades: ProgressiveBlades
    star_timer_disable_item: StarTimerDisableItem

option_groups = [
    OptionGroup(
        "Item Options",
        [
            TutorialsItem,
            DisableSpikesItem,
            ProgressiveElectricSparks,
            ProgressiveBlades,
            StarTimerDisableItem,
        ]
    ),
]

option_presets = {
    # TODO: Option presets
}
