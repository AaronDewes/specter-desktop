import logging
import os

from cryptoadvance.specter.process_controller.node_controller import (
    fetch_wallet_addresses_for_mining,
)
from cryptoadvance.specter.process_controller.bitcoind_controller import (
    BitcoindPlainController,
)
from cryptoadvance.specter.process_controller.node_controller import NodePlainController
from cryptoadvance.specter.util.shell import which


def test_node_running(caplog, docker, request):
    # TODO: Refactor this to use conftest.instantiate_bitcoind_controller
    # to reduce redundant code?
    caplog.set_level(logging.INFO)
    caplog.set_level(logging.DEBUG, logger="cryptoadvance.specter")
    requested_version = request.config.getoption("--bitcoind-version")
    if docker:
        # The NodeController is not available on docker
        pass
    else:
        my_bitcoind = NodePlainController(
            node_path=find_node_executable(),
            rpcport=18123,  # Non-standardport to not interfer
        )

    rpcconn = my_bitcoind.start_node(cleanup_at_exit=True, cleanup_hard=True)
    requested_version = request.config.getoption("--bitcoind-version")
    assert my_bitcoind.version() == requested_version
    assert rpcconn.get_rpc() != None
    assert rpcconn.get_rpc().ipaddress != None
    bci = rpcconn.get_rpc().getblockchaininfo()
    assert bci["blocks"] == 100
    # you can use the testcoin_faucet:
    random_address = "mruae2834buqxk77oaVpephnA5ZAxNNJ1r"
    my_bitcoind.testcoin_faucet(random_address, amount=25, mine_tx=True)
    my_bitcoind.stop_node()


def test_fetch_wallet_addresses_for_mining(caplog, wallets_filled_data_folder):
    caplog.set_level(logging.INFO)
    caplog.set_level(logging.DEBUG, logger="cryptoadvance.specter")
    # Todo: instantiate a specter-testwallet
    addresses = fetch_wallet_addresses_for_mining(wallets_filled_data_folder)
    assert addresses  # make more sense out of this test


def find_node_executable(node_impl="bitcoin"):
    if os.path.isfile(f"tests/${node_impl}/src/${node_impl}d"):
        # copied from conftest.py
        # always prefer the self-compiled bitcoind if existing
        return f"tests/${node_impl}/src/${node_impl}d"
    elif os.path.isfile("tests/${node_impl}/bin/${node_impl}d"):
        return f"tests/${node_impl}/bin/${node_impl}d"
        # next take the self-installed binary if existing
    else:
        return which("${node_impl}d")
