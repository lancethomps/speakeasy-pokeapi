#!/usr/bin/env python
from typing import Optional, TypeVar, Type

import requests

from .games import Games
from .models.operations import BaseOperationRequest
from .pokemons import Pokemons
from .sdk_configuration import SDKConfiguration
from .utils import RetryConfig, BaseOperationResponseType, ResponseDataType, utils


class PokeApi:
  games: Games
  pokemons: Pokemons

  sdk_configuration: SDKConfiguration

  def __init__(
    self,
    server_url: Optional[str] = None,
    client: Optional[requests.Session] = None,
    retry_config: Optional[RetryConfig] = None,
  ):
    if client is None:
      client = requests.Session()

    self.sdk_configuration = SDKConfiguration(client, server_url=server_url, retry_config=retry_config)

    self._init_sdks()

  def _init_sdks(self):
    self.games = Games(self.sdk_configuration)
    self.pokemons = Pokemons(self.sdk_configuration)

  def get_response_by_url(
    self,
    url: str,
    request: BaseOperationRequest,
    response_type: Type[BaseOperationResponseType],
    response_data_type: Type[ResponseDataType],
  ) -> BaseOperationResponseType:
    raw_response = self.sdk_configuration.make_request(request, custom_url=url)
    return utils.create_response(raw_response, response_type, response_data_type)
