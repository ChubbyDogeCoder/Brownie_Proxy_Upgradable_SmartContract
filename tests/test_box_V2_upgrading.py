from asyncio import exceptions
from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    BoxV2,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    exceptions,
)
import pytest


def test_proxy_upg():
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

    # DEploying V2

    _BoxV2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, _BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    upgrade(account, proxy, _BoxV2, proxy_admin_contract=_ProxyAdmin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
