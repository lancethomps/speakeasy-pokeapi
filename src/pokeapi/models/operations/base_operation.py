#!/usr/bin/env python
import dataclasses

import requests


@dataclasses.dataclass
class BaseOperationRequest:

  def get_method(self) -> str:
    raise TypeError("Must be implemented by child class")

  def get_path(self) -> str:
    raise TypeError("Must be implemented by child class")


@dataclasses.dataclass
class BaseOperationResponse:
  content_type: str = dataclasses.field()
  r"""HTTP response content type for this operation"""
  status_code: int = dataclasses.field()
  r"""HTTP response status code for this operation"""
  raw_response: requests.Response = dataclasses.field()
  r"""Raw HTTP response; suitable for custom response parsing"""

  def is_success(self) -> bool:
    return self.status_code == 200
