import random

import pytest

from aioeosabi import EosAccount, EosJsonRpc, EosTransaction, EosAuthority
from aioeosabi.contracts import eosio


@pytest.fixture
def rpc():
    return EosJsonRpc(url='http://127.0.0.1:8888')


@pytest.fixture
def main_account():
    return EosAccount(
        name='eostest12345',
        private_key='5JeaxignXEg3mGwvgmwxG6w6wHcRp9ooPw81KjrP2ah6TWSECDN'
    )


@pytest.fixture
async def second_account(loop, main_account, rpc):
    name = ''.join(
        random.choice('12345abcdefghijklmnopqrstuvwxyz')
        for i in range(12)
    )
    account = EosAccount(name=name)
    block = await rpc.get_head_block()

    owner = EosAuthority(
        threshold=1,
        keys=[account.key.to_key_weight(1)]
    )

    await rpc.sign_and_push_transaction(
        EosTransaction(
            ref_block_num=block['block_num'] & 65535,
            ref_block_prefix=block['ref_block_prefix'],
            actions=[
                eosio.newaccount(
                    main_account.name,
                    account.name,
                    owner=owner,
                    authorization=[main_account.authorization('active')]
                ),
                eosio.buyrambytes(
                    main_account.name,
                    account.name,
                    2048,
                    authorization=[main_account.authorization('active')]
                )
            ],
        ),
        keys=[main_account.key]
    )
    return account
