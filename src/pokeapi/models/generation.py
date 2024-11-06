#!/usr/bin/env python
import dataclasses
from typing import List

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from .common import Name, NamedAPIResource


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Generation(DataClassJsonMixin):
  abilities: List[NamedAPIResource]
  id: int
  main_region: NamedAPIResource
  moves: List[NamedAPIResource]
  name: str
  names: List[Name]
  pokemon_species: List[NamedAPIResource]
  types: List[NamedAPIResource]
  version_groups: List[NamedAPIResource]
