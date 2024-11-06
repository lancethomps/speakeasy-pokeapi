#!/usr/bin/env python
import unittest

from pokeapi.models.operations import GetPokemonResponse, GetGenerationResponse
from pokeapi import PokeApi


class TestGames(unittest.TestCase):

  def setUp(self):
    self.sdk = PokeApi()

  def test_get_generation_by_id(self):
    response = self.sdk.games.get_generation(1)
    self.assert_generation(response, 1, "generation-i")

  def test_get_generation_by_name(self):
    response = self.sdk.games.get_generation("generation-ii")
    self.assert_generation(response, 2, "generation-ii")

  def assert_generation(self, response: GetGenerationResponse, id: int, name: str):
    self.assertTrue(response.is_success())
    self.assertEqual(200, response.status_code)
    self.assertEqual("application/json; charset=utf-8", response.content_type)

    generation = response.data
    self.assertEqual(id, generation.id)
    self.assertEqual(name, generation.name)


if __name__ == '__main__':
  unittest.main()
