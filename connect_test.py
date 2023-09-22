# This is an end to end example of a very basic adding strategy.
import json
import logging
import threading
import time

import eth_account
import utils
# from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.utils.types import (
    SIDES,
    Dict,
    L2BookMsg,
    L2BookSubscription,
    Literal,
    Optional,
    Side,
    TypedDict,
    Union,
    UserEventsMsg,
)
addy = '0x40574F1bcA0C9054C3617c117cE9A13D6aFb882F'
info = Info(constants.TESTNET_API_URL, skip_ws=True)
user_state = info.user_state(addy)["assetPositions"][9]

# print(info.open_orders(addy))
print(user_state)
# info.send_order()


def main():
    # Setting this to logging.DEBUG can be helpful for debugging websocket callback issues
    logging.basicConfig(level=logging.ERROR)
    config = utils.get_config()
    account = eth_account.Account.from_key(config["secret_key"])
    print("Running with account address:", account.address)
    # BasicAdder(account, constants.TESTNET_API_URL)


if __name__ == "__main__":
    main()

