#!/usr/bin/env python
import unittest

from pokeapi.models.errors import SDKError
from pokeapi.models.operations import GetPokemonResponse, GetPokemonRequest
from pokeapi import PokeApi
import helpers


class TestPokemons(unittest.TestCase):

  def setUp(self):
    self.sdk = PokeApi()

  def test_get_pokemon_request_url(self):
    req = self.sdk.pokemons._create_request(GetPokemonRequest(1))
    self.assertEqual("https://pokeapi.co/api/v2/pokemon/1/", req.url)

  def test_get_pokemon_by_id(self):
    response = self.sdk.pokemons.get_pokemon(1)
    self.assert_pokemon(response, 1, "bulbasaur")

  def test_get_pokemon_by_name(self):
    response = self.sdk.pokemons.get_pokemon("charmander")
    self.assert_pokemon(response, 4, "charmander")

  def test_get_pokemon_not_found(self):
    response = self.sdk.pokemons.get_pokemon(-1)
    self.assertFalse(response.is_success())
    self.assertEqual(404, response.status_code)

  def test_get_pokemon_sdk_error(self):
    sdk = PokeApi(server_url="https://fake.co")
    with self.assertRaises(SDKError) as cm:
      sdk.pokemons.get_pokemon(1)

    err = cm.exception
    self.assertEqual(SDKError, type(err))

  def test_list_pokemon(self):
    response = self.sdk.pokemons.list_pokemon(limit=1, offset=1)
    helpers.assert_response(self, response)
    self.assertTrue(response.data.has_more())

    next_response = response.get_next(self.sdk)
    helpers.assert_response(self, next_response)
    self.assertTrue(next_response.data.has_more())

  def test_list_pokemon_end(self):
    response = self.sdk.pokemons.list_pokemon(limit=1, offset=20_000)
    helpers.assert_response(self, response)
    self.assertFalse(response.data.has_more())

  def assert_pokemon(self, response: GetPokemonResponse, id: int, name: str):
    helpers.assert_response(self, response)

    pokemon = response.data
    self.assertEqual(id, pokemon.id)
    self.assertEqual(name, pokemon.name)
    self.assertIsNotNone(pokemon.is_default)


if __name__ == '__main__':
  unittest.main()
