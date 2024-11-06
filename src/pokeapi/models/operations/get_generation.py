#!/usr/bin/env python
import dataclasses
from typing import Optional, Union

import requests

from .base_operation import BaseOperationRequest, BaseOperationResponse
from ...models.generation import Generation


@dataclasses.dataclass
class GetGenerationRequest(BaseOperationRequest):
  id_or_name: Union[int, str] = dataclasses.field(metadata={'path_param': {'field_name': 'id_or_name'}})

  def get_method(self) -> str:
    return "GET"

  def get_path(self) -> str:
    return '/api/v2/generation/{id_or_name}/'


@dataclasses.dataclass
class GetGenerationResponse(BaseOperationResponse):
  data: Optional[Generation] = dataclasses.field(default=None)
  r"""A generation."""
