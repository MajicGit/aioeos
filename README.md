# aioeosabi
Updated version of aioeos to no longer rely on API calls to serialize data. Integrates https://github.com/stuckatsixpm/antelopy to serialize instead.
Should be usable as a drop-in replacement for the original aioeos.

For Documentation: See the original aioeos Docs. Only difference is that `sign_and_push_transaction` now lets you specify if you want to use a stored ABI or fetch a new one. Also two new helper functions. 

- smart_sign_and_push_transaction: Signs and pushes a transaction using the cached ABI, refetching the ABI if the first try fails.

- push_actions: Pushed out a transaction, trying out various endpoints until one succeeds. 

[![Documentation Status](https://readthedocs.org/projects/aioeos/badge/?version=latest)](http://aioeos.readthedocs.io/en/latest/?badge=latest)  ![Python package](https://github.com/ulamlabs/aioeos/workflows/Python%20package/badge.svg) ![Upload Python Package](https://github.com/ulamlabs/aioeos/workflows/Upload%20Python%20Package/badge.svg)

Async Python library for interacting with EOS.io blockchain. 

## Features

1. Async JSON-RPC client.
2. Signing and verifying transactions using private and public keys.
3. Serializer for basic EOS.io blockchain ABI types.
4. Helpers which provide an easy way to generate common actions, such as token
   transfer.

## Installation

Library is available on PyPi, you can simply install it using `pip`.
```shell
$ pip install aioeosabi
```

## Usage

### Importing a private key

```python
from aioeosabi import EosAccount

account = EosAccount(private_key='your key')
```

### Transferring funds

```python
from aioeosabi import EosJsonRpc, EosTransaction
from aioeosabi.contracts import eosio_token


rpc = EosJsonRpc(url='http://127.0.0.1:8888')
block = await rpc.get_head_block()

transaction = EosTransaction(
   ref_block_num=block['block_num'] & 65535,
   ref_block_prefix=block['ref_block_prefix'],
   actions=[
      eosio_token.transfer(
         from_addr=account.name,
         to_addr='mysecondacc1',
         quantity='1.0000 EOS',
         authorization=[account.authorization('active')]
      )
   ]
)
await rpc.sign_and_push_transaction(transaction, keys=[account.key])
```

### Creating a new account

```python
from aioeosabi import EosJsonRpc, EosTransaction, EosAuthority
from aioeosabi.contracts import eosio


main_account = EosAccount(name='mainaccount1', private_key='private key')
new_account = EosAccount(name='mysecondacc1')
owner = EosAuthority(
   threshold=1,
   keys=[new_account.key.to_key_weight(1)]
)

rpc = EosJsonRpc(url='http://127.0.0.1:8888')
block = await rpc.get_head_block()

await rpc.sign_and_push_transaction(
   EosTransaction(
      ref_block_num=block['block_num'] & 65535,
      ref_block_prefix=block['ref_block_prefix'],
      actions=[
            eosio.newaccount(
               main_account.name,
               new_account.name,
               owner=owner,
               authorization=[main_account.authorization('active')]
            ),
            eosio.buyrambytes(
               main_account.name,
               new_account.name,
               2048,
               authorization=[main_account.authorization('active')]
            )
      ],
   ),
   keys=[main_account.key]
)
```

## Documentation

Docs and usage examples are available [here](https://aioeos.readthedocs.io/en/latest).

## Unit testing

To run unit tests, you need to bootstrap an EOS testnet node first. Use the provided `ensure_eosio.sh` script.

```shell
$ ./ensure_eosio.sh
```
