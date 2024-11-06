import requests


class SDKError(Exception):
  """Represents an error returned by the API."""
  message: str
  status_code: int
  body: str
  raw_response: requests.Response

  def __init__(self, message: str, raw_response: requests.Response):
    self.message = message
    self.raw_response = raw_response
    self.status_code = raw_response.status_code
    self.body = raw_response.text

  def __str__(self):
    body = ''
    if len(self.body) > 0:
      body = f'\n{self.body}'

    return f'{self.message}: Status {self.status_code}{body}'
