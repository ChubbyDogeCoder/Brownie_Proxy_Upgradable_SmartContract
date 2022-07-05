from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, Contract, ProxyAdmin, TransparentUpgradeableProxy


def test_proxy_delegation():
    account = get_account()
    _Box = Box.deploy({"from": account})
    _ProxyAdmin = ProxyAdmin.deploy({"from": account})
    Box_encoded_initi_fn = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        _Box.address,
        _ProxyAdmin.address,
        Box_encoded_initi_fn,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_Box = Contract.from_abi("Box", proxy.address, _Box.abi)
    assert proxy_Box.retrieve() == 0
    proxy_Box.store(1, {"from": account})
