#!/usr/bin/env python
import dataclasses
from typing import Optional, List

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class NamedAPIResource:
  name: str
  url: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class NamedAPIResourceList(DataClassJsonMixin):
  count: int
  next: Optional[str]
  previous: Optional[str]
  results: List[NamedAPIResource]

  def has_more(self) -> bool:
    return self.next is not None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Name:
  language: NamedAPIResource
  name: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class VersionGameIndex:
  game_index: int
  version: NamedAPIResource
