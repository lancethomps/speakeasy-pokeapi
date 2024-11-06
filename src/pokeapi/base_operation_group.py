#!/usr/bin/env python
from typing import Type

import requests

from .models.operations import BaseOperationRequest
from .sdk_configuration import SDKConfiguration
from .utils import BaseOperationResponseType, ResponseDataType, utils


class BaseOperationGroup:
  sdk_configuration: SDKConfiguration

  def __init__(self, sdk_configuration: SDKConfiguration):
    self.sdk_configuration = sdk_configuration

  def _create_request(self, request: BaseOperationRequest) -> requests.PreparedRequest:
    return self.sdk_configuration.create_request(request)

  def _make_request(self, request: BaseOperationRequest) -> requests.Response:
    return self.sdk_configuration.make_request(request)

  def _call_and_parse(
    self,
    request: BaseOperationRequest,
    response_type: Type[BaseOperationResponseType],
    response_data_type: Type[ResponseDataType],
  ) -> BaseOperationResponseType:
    return utils.create_response(self._make_request(request), response_type, response_data_type)
