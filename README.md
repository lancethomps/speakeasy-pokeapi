# PokéAPI Python SDK

[![Build](https://github.com/lancethomps/speakeasy-pokeapi/actions/workflows/build.yml/badge.svg)](https://github.com/lancethomps/speakeasy-pokeapi/actions/workflows/build.yml)

A Python wrapper to access the following endpoints for [PokéAPI](https://pokeapi.co)

- `https://pokeapi.co/api/v2/generation/{id or name}/`
- `https://pokeapi.co/api/v2/pokemon/{id or name}/`

## Installation

Using the Makefile target

```bash
make install
```

Using pip directly

```bash
pip install .
```

## Usage

```python
from pokeapi import PokeApi

# initialize SDK
sdk = PokeApi()

# get pokemon by name
response = sdk.pokemons.get_pokemon("charmander")
if not response.is_success():
  raise Exception("Failed request: " + str(response.status_code))

pokemon = response.data
print(pokemon.moves[0].move.name)

# get pokemon by id
sdk.pokemons.get_pokemon(4)
```

Using a custom server URL

```python
from pokeapi import PokeApi

sdk = PokeApi(server_url="https://test.pokeapi.co")
```

## Local Development

Clone the repository and run `make init` to get started. Some other common tasks are below:

Show Makefile target descriptions

```bash
make help
```

Linting

```bash
make lint
```

Testing

```bash
make test
```

Run all checks locally

```bash
make check
```

_Additionally, GitHub actions have been configured to build & test the SDK._

## Design decisions

Due to the simplistic nature of the PokeAPI and these specific endpoints, I leaned toward keeping things relatively simple.

### Request / Response Base Classes

For requests, I opted to force all operations to implement `BaseOperationRequest`, which includes `get_method` and `get_path` methods that must be overwritten.
This allows for common handling of HTTP request creation.

All response classes extend `BaseOperationResponse`, which contains common fields and methods for processing responses.
This also allows for common handling of HTTP response deserialization. 

### Models

Simple, concise model definitions with easy deserialization / serialization using `@dataclass` and `@dataclass_json`

```python
@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Pokemon:
  base_experience: int
  height: int
  id: int
  is_default: bool
  location_area_encounters: str
  name: str
  order: int
  weight: int
```

### Error Handling

I could not find any documentation on the API site detailing out the different error responses and how to handle them. Through my own testing, I was able to include support for `404 (NOT FOUND)` errors.
There is a `is_success` method on all responses to determine if the resource wasn't found - all responses outside of `200` and `404` throw an `SDKError`.

### Retries

I considered implementing retry logic within the SDK, but ended up opting for skipping that functionality due to the simplistic nature of the APIs. I kept some of the code in the project, and could look to implement it in the future.
Due to the nature of the specific endpoints being supported, the primary case that would be handled by the retry logic is network errors on the client side and API server downtime (it would be unreasonable to expect `404` errors to change on retry).

### Pagination

I opted to enable simple retrieval of additional pages in the `list_pokemon` operation via direct retrieval of API responses by custom URLs. See `pokeapi.models.operations.list_pokemon.ListPokemonResponse.get_next`.
This is easily extendable to other paginated APIs.

## Potential Improvements

- Add hooks into the SDK in order to allow for custom instrumentation, common request/response modifications, etc.
- Implement retries
- Allow for direct retrieval of `NamedAPIResource` by `url`, including knowing how to deserialize responses correctly.
