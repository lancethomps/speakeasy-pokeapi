from dataclasses import Field, fields
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Any, Dict, Tuple, List, TypeVar, Type

import requests
from dataclasses_json import DataClassJsonMixin

from ..models.operations import BaseOperationResponse

BaseOperationResponseType = TypeVar('BaseOperationResponseType', bound=BaseOperationResponse)
ResponseDataType = TypeVar('ResponseDataType', bound=DataClassJsonMixin)


def create_response(
  raw_response: requests.Response,
  response_type: Type[BaseOperationResponseType],
  response_data_type: Type[ResponseDataType],
) -> BaseOperationResponseType:
  response: BaseOperationResponseType = response_type(status_code=raw_response.status_code, content_type=raw_response.headers.get('Content-Type') or '', raw_response=raw_response)
  if response.is_success():
    data = response_data_type.from_json(raw_response.text)
    setattr(response, 'data', data)

  return response


def generate_url(clazz: type, server_url: str, path: str, path_params: Any) -> str:
  path_param_fields: Tuple[Field, ...] = fields(clazz)
  for field in path_param_fields:
    request_metadata = field.metadata.get('request')
    if request_metadata is not None:
      continue

    param_metadata = field.metadata.get('path_param')
    if param_metadata is None:
      continue

    param = getattr(path_params, field.name) if path_params is not None else None

    if param is None:
      continue

    if param_metadata.get('style', 'simple') == 'simple':
      if isinstance(param, List):
        pp_vals: List[str] = []
        for pp_val in param:
          if pp_val is None:
            continue
          pp_vals.append(_val_to_string(pp_val))
        path = path.replace('{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
      elif isinstance(param, Dict):
        pp_vals: List[str] = []
        for pp_key in param:
          if param[pp_key] is None:
            continue
          if param_metadata.get('explode'):
            pp_vals.append(f"{pp_key}={_val_to_string(param[pp_key])}")
          else:
            pp_vals.append(f"{pp_key},{_val_to_string(param[pp_key])}")
        path = path.replace('{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
      elif not isinstance(param, (str, int, float, complex, bool, Decimal)):
        pp_vals: List[str] = []
        param_fields: Tuple[Field, ...] = fields(param)
        for param_field in param_fields:
          param_value_metadata = param_field.metadata.get('path_param')
          if not param_value_metadata:
            continue

          parm_name = param_value_metadata.get('field_name', field.name)

          param_field_val = getattr(param, param_field.name)
          if param_field_val is None:
            continue
          if param_metadata.get('explode'):
            pp_vals.append(f"{parm_name}={_val_to_string(param_field_val)}")
          else:
            pp_vals.append(f"{parm_name},{_val_to_string(param_field_val)}")
        path = path.replace('{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
      else:
        path = path.replace('{' + param_metadata.get('field_name', field.name) + '}', _val_to_string(param), 1)

  return server_url.removesuffix('/') + path


def get_query_params(clazz: type, query_params: Any) -> Dict[str, List[str]]:
  params: Dict[str, List[str]] = {}

  param_fields: Tuple[Field, ...] = fields(clazz)
  for field in param_fields:
    request_metadata = field.metadata.get('request')
    if request_metadata is not None:
      continue

    metadata = field.metadata.get('query_param')
    if not metadata:
      continue

    param_name = field.name
    value = getattr(query_params, param_name) if query_params is not None else None
    if value is None:
      continue

    f_name = metadata.get("field_name")
    params[f_name] = [_val_to_string(value)]

  return params


def _val_to_string(val) -> str:
  if isinstance(val, bool):
    return str(val).lower()
  if isinstance(val, datetime):
    return str(val.isoformat().replace('+00:00', 'Z'))
  if isinstance(val, Enum):
    return str(val.value)

  return str(val)
