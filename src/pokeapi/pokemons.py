#!/usr/bin/env python
from typing import Union, Optional

from .base_operation_group import BaseOperationGroup
from .models import Pokemon, NamedAPIResourceList
from .models.operations import GetPokemonResponse, GetPokemonRequest, ListPokemonResponse, ListPokemonRequest
from .sdk_configuration import SDKConfiguration


class Pokemons(BaseOperationGroup):

  def __init__(self, sdk_configuration: SDKConfiguration):
    BaseOperationGroup.__init__(self, sdk_configuration)

  def get_pokemon(self, id_or_name: Union[int, str]) -> GetPokemonResponse:
    return self._call_and_parse(
      GetPokemonRequest(id_or_name=id_or_name),
      GetPokemonResponse,
      Pokemon,
    )

  def list_pokemon(self, limit: Optional[int] = None, offset: Optional[int] = None) -> ListPokemonResponse:
    return self._call_and_parse(
      ListPokemonRequest(limit=limit, offset=offset),
      ListPokemonResponse,
      NamedAPIResourceList,
    )
