import websocket
import json
import requests
import sys
import logging
import platform

if platform.system() == 'Linux':
    sys.path.append('~/algotrading_infra/')
else:
    sys.path.append('/Users/sanket/algotrading/infra')

print(platform.system())
print(sys.path)

from src.orderbook import Order, Orderbook, Halfbook
from src.types import Exchange, Side, Lifespan

print(Orderbook)


ws_url = 'wss://fstream.binance.com'
base_url = 'https://fapi.binance.com'

# open stream and buffer events
# get max limit depth snapshot through rest api
# drop any event where u < lastupdateid
# firs processed event should have U <= lastupdateid and u >= lastupdateid
# while listening to stream, each new event's `pu` should be equiv to last 'u'
#   otherwise get depth snapshot again
# data in each event is absolute quantity @ price level
# if quantity = 0, remove price level

def get_snapshot(symbol: str, limit : int):
    ep = '/fapi/v1/depth'
    endpoint = base_url + ep
    params = {
        "symbol": symbol,
        "limit":limit
    }
    response = requests.get(endpoint, params=params)
    print(response.status_code)
    return response.json()

def get_exchangeInfo():
    ep = '/fapi/v1/exchangeInfo'
    endpoint = base_url + ep
    response = requests.get(endpoint)
    # print(response)
    return response


# def build_book(symbol: str):
#     book_data = get_snapshot(symbol=symbol, limit=500)


# def main():
#     logging.basicConfig(filename='binance_stream', level=logging.ERROR)


# if __name__ == '__main__':
#     main()



# get_snapshot(symbol= 'BTCUSDT', limit=500)
# print((get_exchangeInfo().json()))


print(get_snapshot(symbol='ETHUSDT', limit=500))




# def on_open(ws):
#     print("opened")

#     auth_data = {
#         'op': 'subscribe',
#         'args': ['instrument:XBTUSD']
#     }
#     ws.send(json.dumps(auth_data))

# def on_message(ws, message):
#     message = json.loads(message)
#     print(message)

# def on_close(ws):
#     print("closed connection")





# ws = websocket.WebSocketApp(socket, 
#                             on_open=on_open, 
#                             on_message=on_message,
#                             on_close=on_close)     
# ws.run_forever()