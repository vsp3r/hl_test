import json
import time
import requests
import logging
import sys

import utils
from eth_account import Account
from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

COIN = 'BLZ'

class Canceller:
    def __init__(self, wallet: LocalAccount, api_url: str, user: str):
        self.logger = logging.getLogger(__class__.__name__)
        self.info = Info(api_url)
        self.exchange = Exchange(wallet, api_url)
        self.user = user
        self.api_url = api_url
    
    def run(self):
        try:
            self.cancel_all_orders()
            self.cancel_open_positions()
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
        finally:
            sys.exit(0)
        

    def cancel_all_orders(self):
        orders = self.get_open_orders()
        for order in orders:
            self.cancel_order(order['oid'])

    def get_open_orders(self):
        endpoint = f"{self.api_url}/info"
        msg = {
            "type": "openOrders",
            "user": self.user
        }
        response = requests.post(endpoint, json=msg)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def cancel_order(self, oid: int):
        response = self.exchange.cancel(COIN, oid)
        if response["status"] == "ok":
            self.logger.info(f'Successfully cancelled order {oid} on {COIN}')
        else:
            self.logger.warning(f"Failed to cancel order {oid} on {COIN}")

    def cancel_open_positions(self):
        position = self.get_positions()
        while position['entryPx'] is not None:
            self.cancel_position(position)
            time.sleep(3)
            position = self.get_positions()
        self.logger.info(f'Orders: {self.get_open_orders()}')
        self.logger.info(f'Positions: {self.get_positions()}')

    def get_positions(self):
        endpoint = f"{self.api_url}/info"
        msg = {
            "type": "clearinghouseState",
            "user": self.user
        }
        response = requests.post(endpoint, json=msg)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        for position in response_data['assetPositions']:
            if position['position']['coin'] == COIN:
                return position['position']

    def cancel_position(self, position):
        size = float(position['szi'])
        side = size < 0
        entry = float(position['entryPx'])
        px = entry + 0.2 * entry if side else entry - 0.2 * entry
        px = round(px, 5)  # might be able to generalize further w/ per coin sig fig rounding
        size = abs(size)
        response = self.exchange.order(COIN, side, size, px, {"limit": {"tif": "Ioc"}})
        self.logger.info("SENT POSITION CANCELLING MARKET ORDERS")
        self.logger.debug(response)

def main():
    # repeat cancel requests for like 5 seconds or until in no pos/orders
    # then print when all cancels are confirmed, and userpositions / orders are both empty
    logging.basicConfig(level=logging.INFO)
    config = utils.get_config()
    account = Account.from_key(config['secret_key'])
    canceller = Canceller(account, constants.TESTNET_API_URL, config['account'])
    canceller.run()

if __name__== '__main__':
    main()



