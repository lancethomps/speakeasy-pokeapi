#!/usr/bin/env python
import dataclasses
from typing import Optional

import requests

from .models.errors import SDKError
from .models.operations import BaseOperationRequest
from .utils import utils
from .utils.retries import RetryConfig

DEFAULT_SERVER = 'https://pokeapi.co'


@dataclasses.dataclass
class SDKConfiguration:
  client: requests.Session
  server_url: Optional[str] = None
  retry_config: Optional[RetryConfig] = None

  def get_server_url(self) -> str:
    if self.server_url:
      return self.server_url.removesuffix('/')

    return DEFAULT_SERVER

  def create_request(
    self,
    request: BaseOperationRequest,
    custom_url: Optional[str] = None,
  ) -> requests.PreparedRequest:
    headers = {}
    headers["Accept"] = "application/json"
    if custom_url is not None:
      return self.client.prepare_request(requests.Request(request.get_method(), custom_url, headers=headers))

    url = utils.generate_url(type(request), self.get_server_url(), request.get_path(), request)
    query_params = utils.get_query_params(type(request), request)
    return self.client.prepare_request(requests.Request(request.get_method(), url, headers=headers, params=query_params))

  def make_request(
    self,
    request: BaseOperationRequest,
    custom_url: Optional[str] = None,
  ) -> requests.Response:
    req = self.create_request(request, custom_url)
    response = self.client.send(req)
    if response.status_code not in [200, 404]:
      raise SDKError("API error occurred", response)

    return response
