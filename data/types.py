from enum import Enum, unique


URL = str


@unique
class Rarity(Enum):
    NORMAL = 'normal'
    MAGIC = 'magic'
    RARE = 'rare'
    UNIQUE = 'unique'


@unique
class NinjaCategory(Enum):
    # General
    CURRENCY = 'Currency'
    FRAGMENTS = 'Fragments'
    TATTOOS = 'Tattoos'
    OMENS = 'Omens'
    DIVINATION_CARDS = 'Divination Cards'
    ARTIFACTS = 'Artifacts'
    OILS = 'Oils'
    INCUBATORS = 'Incubators'
    # Equipment & Gems
    UNIQUE_WEAPONS = 'Unique Weapons'
    UNIQUE_ARMOURS = 'Unique Armours'
    UNIQUE_ACCESSORIES = 'Unique Accessories'
    UNIQUE_FLASKS = 'Unique Flasks'
    UNIQUE_JEWELS = 'Unique Jewels'
    UNIQUE_RELICS = 'Unique Relics'
    SKILL_GEMS = 'Skill Gems'
    CLUSTER_JEWELS = 'Cluster Jewels'
    # Atlas
    MAPS = 'Maps'
    BLIGHTED_MAPS = 'Blighted Maps'
    BLIGHT_RAVAGED_MAPS = 'Blight-ravaged Maps'
    SCOURGED_MAPS = 'Scourged Maps'
    UNIQUE_MAPS = 'Unique Maps'
    DELIRIUM_ORBS = 'Delirium Orbs'
    INVITATIONS = 'Invitations'
    SCARABS = 'Scarabs'
    MEMORIES = 'Memories'
    # Crafting
    BASE_TYPES = 'Base Types'
    FOSSILS = 'Fossils'
    RESONATORS = 'Resonators'
    HELMET_ENCHANTS = 'Helmet Enchants'
    BEASTS = 'Beasts'
    ESSENCES = 'Essences'
    VIALS = 'Vials'
