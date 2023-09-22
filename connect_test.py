import requests
import json
import sys
import time

from hyperliquid.info import Info
from hyperliquid.utils import constants
addy = '0x40574F1bcA0C9054C3617c117cE9A13D6aFb882F'
info = Info(constants.TESTNET_API_URL, skip_ws=True)
user_state = info.user_state(addy)["assetPositions"][9]

# print(info.open_orders(addy))
print(user_state)
# info.send_order()
