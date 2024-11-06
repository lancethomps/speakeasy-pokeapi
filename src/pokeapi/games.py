#!/usr/bin/env python
from typing import Union

from .base_operation_group import BaseOperationGroup
from .models import Generation
from .models.operations import GetGenerationResponse, GetGenerationRequest
from .sdk_configuration import SDKConfiguration


class Games(BaseOperationGroup):

  def __init__(self, sdk_configuration: SDKConfiguration):
    BaseOperationGroup.__init__(self, sdk_configuration)

  def get_generation(self, id_or_name: Union[int, str]) -> GetGenerationResponse:
    return self._call_and_parse(
      GetGenerationRequest(id_or_name=id_or_name),
      GetGenerationResponse,
      Generation,
    )
