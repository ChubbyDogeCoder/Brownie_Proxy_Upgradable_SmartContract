from brownie import (
    network,
    config,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from claripy import true
from scripts.helpful_scripts import (
    get_account,
    encode_function_data,
    upgrade,
)


def main():
    account = get_account()
    print(f" DEploying the contract {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f" ๐ฅฐ This is the result {box.retrieve()}")

    ## Extra@dev_Task: Make multi_Sig Prox Admin from Github
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    # Task 2: initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )
    print(
        f" ๐ณ Ze Proxy has been deployed to {proxy}, you can now Upgrade to V2 and be a real @Dev ๐คช๐คช"
    )
    proxxy_box = Contract.from_abi(
        "box",
        proxy.address,
        box.abi,
    )
    proxxy_box.store(1, {"from": account, "gas_limit": 1000000})
    print(f"\n๐ค๐ค Retrievening .... {proxxy_box.retrieve()}\n")

    # Upgrading the SmC

    _BoxV2 = BoxV2.deploy({"from": account}, publish_source=True)
    uup_txxx = upgrade(
        account,
        proxy,
        _BoxV2.address,
        proxy_admin_contract=proxy_admin,
    )

    print("\nProxy has been Upgraded!! ๐๐๐\n")
    proxxy_box = Contract.from_abi(
        "_BoxV2",
        proxy.address,
        _BoxV2.abi,
    )
    proxxy_box.increment({"from": account})
    print(f"๐ฃ๐ฃ\n๐ฎThis is the prox_box.retrieve(): {proxxy_box.retrieve()}")
