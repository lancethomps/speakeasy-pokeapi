#!/usr/bin/env python
import dataclasses
from typing import List, Optional

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from .common import NamedAPIResource, VersionGameIndex


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonAbility:
  ability: NamedAPIResource
  is_hidden: bool
  slot: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonCries:
  latest: str
  legacy: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonHeldItemVersion:
  rarity: int
  version: NamedAPIResource


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonHeldItem:
  item: NamedAPIResource
  version_details: List[PokemonHeldItemVersion]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonMoveVersion:
  move_learn_method: NamedAPIResource
  version_group: NamedAPIResource
  level_learned_at: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonMove:
  move: NamedAPIResource
  version_group_details: List[PokemonMoveVersion]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonSprites:
  back_default: str
  back_female: Optional[str]
  back_shiny: Optional[str]
  back_shiny_female: Optional[str]
  front_default: str
  front_female: Optional[str]
  front_shiny: Optional[str]
  front_shiny_female: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonStat:
  base_stat: int
  effort: int
  stat: NamedAPIResource


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonType:
  slot: int
  type: NamedAPIResource


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class PokemonTypePast:
  generation: NamedAPIResource
  types: List[PokemonType]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Pokemon(DataClassJsonMixin):
  abilities: List[PokemonAbility]
  base_experience: int
  cries: PokemonCries
  forms: List[NamedAPIResource]
  game_indices: List[VersionGameIndex]
  height: int
  held_items: List[PokemonHeldItem]
  id: int
  is_default: bool
  location_area_encounters: str
  moves: List[PokemonMove]
  name: str
  order: int
  past_types: List[PokemonTypePast]
  species: NamedAPIResource
  sprites: PokemonSprites
  stats: List[PokemonStat]
  types: List[PokemonType]
  weight: int
