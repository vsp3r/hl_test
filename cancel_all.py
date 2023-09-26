import json
import time
import requests
import sys

import eth_account
import utils
from eth_account.signers.local import LocalAccount

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

COIN = 'SNX'

InFlightOrder = TypedDict("InFlightOrder", {"type": Literal["in_flight_order"], "time": int})
Resting = TypedDict("Resting", {"type": Literal["resting"], "px": float, "oid": int})
Cancelled = TypedDict("Cancelled", {"type": Literal["cancelled"]})
ProvideState = Union[InFlightOrder, Resting, Cancelled]


class Canceller:
    def __init__(self, wallet: LocalAccount, api_url: str, user: str):
        self.info = Info(api_url)
        self.exchange = Exchange(wallet, api_url)
        self.positions = {}
        self.user = user
        self.api_url = api_url
        
        self.start_cancelling()

    def start_cancelling(self):
        all_orders = self.get_orders()
        for order in all_orders:
            self.cancel_order(order['oid'])

        position = self.get_positions()
        print(float(position['szi']))
        while position['entryPx'] != None:
            self.cancel_position(position)
            time.sleep(5)
            position = self.get_positions()
            print(float(position['szi']))
            time.sleep(3)
            print(float(position['szi']))

        print(f'Orders: {self.get_orders()}')
        print(f'Positions: {self.get_positions()}')
        sys.exit("cancelled all orders and positions")

    def get_orders(self):
        endpoint = self.api_url + '/info'
        msg = {
            "type":"openOrders",
            "user":self.user
        }
        response = requests.post(endpoint, json=msg)
        if response.status_code == 200:
            print('Get order request submitted successfully')
        else:
            print(f'Failed to submit get_orders data. Status code: {response.status_code}')
        return response.json()
        
    def cancel_order(self, oid: int):
        response = self.exchange.cancel(COIN, oid)
        if response["status"] == "ok":
            print(f'Successfully cancelled order {oid} on {COIN}')
        else:
            print(f"Failed to cancel order {oid} on {COIN}")

    def get_positions(self):
        endpoint = self.api_url + '/info'
        msg = {
            "type":"clearinghouseState",
            "user":self.user
        }
        response = requests.post(endpoint, json=msg)
        if response.status_code == 200:
            print('Get positions request submitted successfully')
        else:
            print(f'Failed to submit get_positions data. Status code: {response.status_code}')
        response = response.json()
        for position in response['assetPositions']:
            if position['position']['coin'] == COIN:
                return position['position']
        
    def cancel_position(self, position):
        
        size = float(position['szi'])
        print(f'Current position: {size}')
        side = size < 0 # true(buy) when inventory negative
        entry = float(position['entryPx'])
        px = entry + 0.2 * entry if side else entry - 0.2 * entry
        px = float(f"{px:.5g}")  # prices should have at most 5 significant digits
        size = abs(size)
        response = self.exchange.order(COIN, side, size, px, {"limit": {"tif": "Ioc"}})
        print("SENT POSITION CANCELLING MARKET ORDERS")
        print(response)
        # if response["status"] == "ok":
        #     status = response["response"]["data"]["statuses"][0]
        #     if "resting" in status:
        #         self.provide_state[side] = {"type": "resting", "px": px, "oid": status["resting"]["oid"]}
        #     else:
        #         print("Unexpected response from placing order. Setting position to None.", response)
        #         self.provide_state[side] = {"type": "cancelled"}

    
    def get_timestamp_ms(self) -> int:
        return int(time.time() * 1000)


def main():
    # repeat cancel requests for like 5 seconds or until in no pos/orders
    # then print when all cancels are confirmed, and userpositions / orders are both empty
    config = utils.get_config()
    account = eth_account.Account.from_key(config['secret_key'])
    canc = Canceller(account, constants.TESTNET_API_URL, config['account'])





if __name__ == '__main__':
    main()
