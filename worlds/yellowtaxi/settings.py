import settings
from typing import Union

class YellowTaxiSettings(settings.Group):
    class EnableMultiworldCoinsanity(settings.Bool):
        """When true, allows Coinsanity to be enabled for Multiworld games.
        This adds thousands of extra locations, and is not recommended for most games!"""
        description = "Yellow Taxi Goes Vroom Enable Coinsanity in Multiworld"

    enable_multiworld_coinsanity: Union[EnableMultiworldCoinsanity, bool] = False