import unittest

from pokeapi.models.operations import BaseOperationResponse


def assert_response(test: unittest.TestCase, response: BaseOperationResponse):
  test.assertTrue(response.is_success())
  test.assertEqual(200, response.status_code)
  test.assertEqual("application/json; charset=utf-8", response.content_type)
