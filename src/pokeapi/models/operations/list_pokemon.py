#!/usr/bin/env python
import dataclasses
from typing import Optional

from .base_operation import BaseOperationRequest, BaseOperationResponse
from .. import NamedAPIResourceList


@dataclasses.dataclass
class ListPokemonRequest(BaseOperationRequest):
  limit: Optional[int] = dataclasses.field(default=None, metadata={'query_param': {'field_name': 'limit'}})
  offset: Optional[int] = dataclasses.field(default=None, metadata={'query_param': {'field_name': 'offset'}})

  def get_method(self) -> str:
    return "GET"

  def get_path(self) -> str:
    return '/api/v2/pokemon/'


@dataclasses.dataclass
class ListPokemonResponse(BaseOperationResponse):
  data: Optional[NamedAPIResourceList] = dataclasses.field(default=None)
  r"""A list of pokemon."""

  def get_next(self, sdk: 'PokeApi') -> Optional['ListPokemonResponse']:  # noqa: F821
    if not self.data or not self.data.has_more():
      return None

    return sdk.get_response_by_url(self.data.next, ListPokemonRequest(), ListPokemonResponse, NamedAPIResourceList)
